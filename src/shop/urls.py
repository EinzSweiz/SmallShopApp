from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.categories_list, name='category_list')
]