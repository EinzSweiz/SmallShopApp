from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .forms import ShippingAddressForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem, ShippingAddress
from django.contrib import messages



@login_required(login_url='account_login')
def payment_shipping_view(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except:
        shipping_address = None
    form = ShippingAddressForm(instance=shipping_address)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(reverse('payment_shipping'))
        else:
            messages.error(request, 'There was an error updating your profile.')
    return render(request, 'payment/shipping.html', {'form': form})


def payment_checkout_view(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')

def payment_complete_view(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        cart = Cart(request)
        total_price = cart.get_total_price()
        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user = request.user if request.user.is_authenticated else None,
            defaults= {
                'full_name': name,
                'email': email,
                'street_address': street_address,
                'apartament': apartment,
                'country': country,
                'city': city,
                'zip_code': zip_code
            }
        )
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
        else:
            order = Order.objects.create(shipping_address=shipping_address, amount=total_price)

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'])
        return JsonResponse({'success':True})

def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html',{})

def payment_fail_view(request):
    return render(request, 'payment/payment_fail.html', {})