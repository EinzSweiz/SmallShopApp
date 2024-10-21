from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user_view, name='account_register'),
    path('email-verification/',
        lambda request: render(request, 'account/email_verification.html'),
        name='email_verification'
        ),
    path('login/', views.user_login_view, name='account_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile-management/', views.profile_management_view, name='profile_management'),
    path('delete-user/<int:id>/', views.user_delete_view, name='user_delete'),

]