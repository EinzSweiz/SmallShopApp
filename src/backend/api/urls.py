from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title='BigCorp API',
        default_version='v1',
        description='BigCorp API Description',
        terms_of_service='https://example.com/terms/',
        contact=openapi.Contact(email='admin@bigcorp.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
)

urlpatterns = [
    path('products/', views.ProductListApiView.as_view(), name='product-list'),
    path('product-detail/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('review-create/<int:id>/', views.ReviewCreateApiView.as_view(), name='review_create'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
