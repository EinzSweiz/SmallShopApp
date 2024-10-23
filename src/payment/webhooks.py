from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from yookassa import Webhook, Configuration
import json
import stripe



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Retrieve the Payment Intent ID from the session
        payment_intent_id = session.get('payment_intent')
        if payment_intent_id:
            # Retrieve the Payment Intent to confirm if the payment was successful
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent.status == 'succeeded':
                try:
                    # Get the order associated with this session
                    order_id = session.get('client_reference_id')
                    order = Order.objects.get(id=order_id)
                    
                    # Update the order as paid
                    order.paid = True
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

    # Return a 200 response to acknowledge receipt of the event
    return HttpResponse(status=200)


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@csrf_exempt
def yookassa_webhook(request):
    try:
        # Ensure the content-type is application/json
        if request.headers.get('Content-Type') == 'application/json':
            # Parse the webhook request body
            webhook_body = json.loads(request.body)

            # Parse the event
            event = Webhook(webhook_body)

            # Check the type of the event
            if event.event == 'payment.succeeded':
                # Extract payment details
                session = event.object

                # This is the payment object from YooKassa
                payment_id = session.get('id')
                amount = session.get('amount').get('value')
                order_id = session.get('metadata', {}).get('order_id')

                # Fetch the order and mark it as paid
                try:
                    order = Order.objects.get(id=order_id)
                    order.paid = True
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

                # Acknowledge the webhook was handled
                return HttpResponse(status=200)

        return HttpResponse(status=400)  # Invalid content type
    except json.JSONDecodeError:
        return HttpResponse(status=400)