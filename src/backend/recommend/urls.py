from django.urls import path
from . import views


urlpatterns = [
    path('create-review/<int:product_id>/', views.create_review_view, name='create_review'),
]