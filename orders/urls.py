from django.urls import path

from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order-complete/', views.order_complete, name='order_success'),
    
    # M-Pesa endpoints
    path('mpesa/initiate/', views.initiate_mpesa_payment, name='initiate_mpesa'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('mpesa/verify/', views.verify_mpesa_payment, name='verify_mpesa'),
]