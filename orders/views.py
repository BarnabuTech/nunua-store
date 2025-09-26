# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from requests import get
from carts.models import CartItem
from .forms import OrderForm
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Order, Payment, OrderProduct
from .mpesa import MpesaClient
import json
from products.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

@login_required
def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart is empty, redirect to products
    cart_items = CartItem.objects.filter(user=current_user)
    if not cart_items.exists():
        return redirect('products')

    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    tax = (2 * total) / 100
    shipping_fee = (1 * total) / 100
    grand_total = total + tax + shipping_fee

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.street_address = form.cleaned_data['street_address']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.postal_code = form.cleaned_data['postal_code']
            data.phone = form.cleaned_data['phone']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR', '')
            data.save()
            
            # Generate order number
            current_date = timezone.now().strftime("%Y%m%d")  # Format: YYYYMMDD
            random_string = get_random_string(5).upper()  # Generate a random 5-character string
            order_number = current_date + str(data.id) + random_string
            data.order_number = order_number
            data.save()
            

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'paypal_client_id': settings.PAYPAL_CLIENT_ID,
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'shipping_fee': shipping_fee,
                'quantity': quantity,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

@require_POST
def initiate_mpesa_payment(request):
    try:
        data = json.loads(request.body)
        order = Order.objects.get(
            user=request.user, 
            is_ordered=False, 
            order_number=data['orderID']
        )
        
        mpesa_client = MpesaClient()
        response = mpesa_client.initiate_stk_push(
            phone_number=data['phoneNumber'],
            amount=order.order_total,
            order_ref=order.order_number
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'STK push initiated',
            'checkoutRequestID': response['CheckoutRequestID']
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_ref = request.GET.get('order_ref')
            
            if data['Body']['stkCallback']['ResultCode'] == 0:
                # Payment successful
                order = Order.objects.get(order_number=order_ref, is_ordered=False)
                
                # Create payment record
                payment = Payment.objects.create(
                    user=order.user,
                    payment_id=data['Body']['stkCallback']['CheckoutRequestID'],
                    payment_method='M-Pesa',
                    amount_paid=order.order_total,
                    status='COMPLETED'
                )
                
                # Update order
                order.payment = payment
                order.is_ordered = True
                order.save()
                
                # Move cart items to order products
                cart_items = CartItem.objects.filter(user=order.user)
                for item in cart_items:
                    OrderProduct.objects.create(
                        order=order,
                        payment=payment,
                        user=order.user,
                        product=item.product,
                        quantity=item.quantity,
                        product_price=item.product.price,
                        ordered=True
                    )
                    
                    # Reduce product stock
                    product = item.product
                    product.stock -= item.quantity
                    product.save()
                
                # Clear cart
                cart_items.delete()
                
                # Send email
                mail_subject = 'Thank you for your order!'
                message = render_to_string('orders/order_recieved_email.html', {
                    'user': order.user,
                    'order': order,
                })
                to_email = order.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                
                return JsonResponse({'status': 'success'})
            else:
                # Payment failed
                return JsonResponse({
                    'status': 'error',
                    'message': data['Body']['stkCallback']['ResultDesc']
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def verify_mpesa_payment(request):
    try:
        data = json.loads(request.body)
        mpesa_client = MpesaClient()
        response = mpesa_client.verify_transaction(data['checkoutRequestID'])
        
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
