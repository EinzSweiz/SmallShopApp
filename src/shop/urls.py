from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('search_products/', views.search_products, name='search_products'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.categories_list, name='category_list')
]