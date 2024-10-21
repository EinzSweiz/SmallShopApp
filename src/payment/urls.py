from django.urls import path
from . import views

urlpatterns = [
    path('shipping/', views.payment_shipping_view, name='payment_shipping'),
    path('checkout/', views.payment_checkout_view, name='payment_checkout'),
    path('complete-order/', views.payment_complete_view, name='payment_complete'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
    path('payment-fail/', views.payment_fail_view, name='payment_fail'),

]