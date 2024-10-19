from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add-cart/', views.cart_add_view, name='add_to_cart')
]