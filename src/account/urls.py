from django.shortcuts import render
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

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
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='password/password_reset.html',
            email_template_name='password/password_reset_email.html',
            success_url=reverse_lazy('password_reset_done')
            ), 
        name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html',

    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ), 
        name='password_reset_confirm'
    ),

    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),

]