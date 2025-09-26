# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render
from django.conf import settings

from products.models import Product, Wishlist

def home(request):
    products = Product.objects.filter(available=True).order_by('-created')[:20]
    wishlisted_ids = set()
    if request.user.is_authenticated:
        wishlisted_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    for product in products:
        product.averageReview = product.average_review()
    
    print("TEMPLATE DIRS:", settings.TEMPLATES[0]['DIRS'])
    
    context = {
        'products': products,
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'pages/home.html', context)

def contact(request):
    return render(request, 'pages/contact.html')
