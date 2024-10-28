import uuid
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .forms import ShippingAddressForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from cart.cart import Cart
from .models import Order, OrderItem, ShippingAddress
from django.contrib import messages
import stripe
from yookassa import Configuration, Payment
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.templatetags.static import static

stripe.api_key = settings.STRIPE_SECRET_KEY

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

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
            return redirect(reverse('payment_checkout'))
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
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')
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

        match payment_type:
            case 'stripe-payment':
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment_fail')),
                    'line_items': []
                }
                if request.user.is_authenticated:
                    order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
                    
                    session_data['line_items'].append({
                        'price_data': {
                            'unit_amount': int(item['price'] * 100),
                            'currency': 'usd',
                            'product_data': {
                                'name': item['product']
                            },
                        },
                        'quantity': item['qty'],
                    })
                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(shipping_address=shipping_address, amount=total_price)

                    session_data['line_items'].append({
                        'price_data': {
                            'unit_amount': int(item['price'] * 100),
                            'currency': 'usd',
                            'product_data': {
                                'name': item['product']
                            },
                        },
                        'quantity': item['qty'],
                    })
                    session['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url)
            case 'yookassa-payment':
                idempotence_key = str(uuid.uuid4())
                currency = 'RUB'
                description = 'Items in Bascket'
                payment = Payment.create({
                    "amount": {
                    "value": str(total_price * 93),
                    "currency": currency
                    },
                    "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri(reverse('payment_success'))
                    },
                    'capture': True,
                    'test': True,
                    "description": description
                }, idempotence_key)

                confirmation_url = payment.confirmation.confirmation_url
                if request.user.is_authenticated:
                    order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
                    return redirect(confirmation_url)
                else:
                    order = Order.objects.create(shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'])

def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html',{})

def payment_fail_view(request):
    return render(request, 'payment/payment_fail.html', {})


@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404('Order was not found')
    html = render_to_string('payment/pdf/pdf_invoice.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    css_path = 'payment/static/css/paid.css'
    css = CSS(css_path)
    HTML(string=html).write_pdf(response, stylesheets=[css])
    return response