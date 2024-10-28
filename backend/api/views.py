from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .serializer import ProductSerializer, ProductDetailSerializer, ReviewSerializer
from shop.models import Product
from .permissions import IsAdminOrReadOnly
from .pagination import StandartResultsSetPagination
from recommend.models import Review
from rest_framework import permissions

class ProductListApiView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = StandartResultsSetPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').order_by('id')

class ProductDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.select_related('category')
    lookup_field = 'id'

class ReviewCreateApiView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    lookup_field='id'

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)   
        serializer.save(created_by=self.request.user, product=product)