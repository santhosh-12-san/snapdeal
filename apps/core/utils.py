from django.core.mail import send_mail
from django.conf import settings
import threading
from twilio.rest import Client
# --- 1. Email Logic (Using Django's Built-in Email) ---
class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )

def send_order_email(user, order):
    """Sends an order confirmation email in the background"""
    subject = f"Snapdeal Order Confirmed: #{order.order_id}"
    message = f"Hi {user.username},\n\nYour order has been placed successfully!\nOrder ID: {order.order_id}\nTotal Amount: Rs. {order.total_amount}\n\nThank you for shopping with us."
    
    # Run in a separate thread so it doesn't slow down the website
    EmailThread(subject, message, [user.email]).start()



