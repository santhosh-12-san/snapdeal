from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    )

    # Link every payment to a specific Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    
    # The unique ID from the Gateway (e.g., "pay_29384723")
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # How did they pay? (Razorpay, Paytm, Wallet, etc.)
    payment_gateway = models.CharField(max_length=50, default="Razorpay")
    
    # Store the actual amount paid (in case it differs from order total due to charges)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Current status of the transaction
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # [CRITICAL] Store the raw response from the bank for debugging
    # Use TextField to store the JSON response (e.g., {"id": "pay_123", "method": "upi"...})
    raw_response = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_gateway} - {self.transaction_id} ({self.status})"