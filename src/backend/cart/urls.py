from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add-cart/', views.cart_add_view, name='add_to_cart'),
    path('delete-cart/', views.cart_delete_view, name='delete_from_cart'),
    path('update-cart/', views.cart_update_view, name='update_cart')

]