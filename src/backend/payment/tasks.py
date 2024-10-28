from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order, OrderItem, ShippingAddress


@shared_task()
def send_order_confirmation(order_id):
    try:
        # Retrieve the order using the provided order_id
        order = Order.objects.get(id=order_id)
        
        # Construct the email subject and message
        subject = f"Order Confirmation - Order #{order.id}"
        message = (
            f"Dear {order.user.username},\n\n"
            f"Thank you for your purchase! Your order #{order.id} has been successfully placed.\n"
            f"Order Details:\n"
            f"Amount: ${order.amount}\n"
            f"Shipping Address: {order.shipping_address}\n"
            f"Order Date: {order.created.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"We will notify you once your order is shipped.\n\n"
            f"Best regards,\n"
            f"BigCorp Team"
        )
        
        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        print(f"Order with id {order_id} does not exist.")
    except Exception as e:
        print(f"Error sending email: {e}")