"""
URL configuration for rshome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop import urls as shop_urls
from django.conf import settings
from django.conf.urls.static import static
from cart import urls as cart_urls
from account import urls as account_urls
from payment import urls as payment_urls
from recommend import urls as recommend_urls
from api import urls as api_urls
from django_email_verification import urls as email_urls
from . import views

DEBUG = settings.DEBUG
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include(shop_urls)),
    path('cart/', include(cart_urls)),
    path('account/', include(account_urls)),
    path('email/', include(email_urls)),
    path('payment/', include(payment_urls)),
    path('', views.index, name='home'),
    path('api/v1/', include(api_urls)),
    path('recommend/', include(recommend_urls)),
]

if DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)