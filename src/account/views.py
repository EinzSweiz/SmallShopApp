from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email
from .forms import UserCreateForm, UserLoginForm

User = get_user_model()


def register_user_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(
                username=user_username,
                email=user_email,
                password=user_password
            )
            user.is_active = False
            if not user.is_active:
                send_email(user)
                return redirect('email_verification')
            

            login(request, user=user)
            return redirect('account_login')
    form = UserCreateForm()
    return render(request, 'account/register.html', {'form':form})


def user_login_view(request):

    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('product_list')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect('account_login')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout_view(request):
    logout(request)
    return redirect('account_login')
