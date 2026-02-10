from django.db import models
from django.conf import settings
from apps.products.models import Product
from apps.users.models import Address

# ==========================
# 1. SHOPPING CART MODELS
# ==========================
from django.db import models
from django.conf import settings
from apps.products.models import Product

class Cart(models.Model):
    # Nullable User + Session ID allows Guest Checkout
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- THIS IS THE MISSING METHOD CAUSING YOUR ERROR ---
    def get_total_price(self):
        # Calculates total bill: sum of (price * quantity) for all items
        return sum(item.product.selling_price * item.quantity for item in self.items.all())

    def __str__(self):
        if self.user:
            return f"Cart for User: {self.user.username}"
        return f"Cart for Session: {self.session_id}"

class CartItem(models.Model):
    # related_name='items' is CRITICAL for cart.items.all() to work
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Store variations
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
# ==========================
# 2. ORDER MODELS
# ==========================

class Order(models.Model):
    STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('UPI', 'UPI'),
        ('Card', 'Credit/Debit Card'),
        ('Wallet', 'Wallet'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=20, unique=True) # "33539076711"
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id}"
    
    # --- THIS IS THE UPDATED FUNCTION YOU REQUESTED ---
    @property
    def get_progress_percentage(self):
        status = str(self.status)
        if status == 'Delivered':
            return "100%"
        elif status == 'Cancelled':
            return "100%"
        elif status == 'Shipped' or status == 'Out for Delivery':
            return "50%"
        else:
            return "10%"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at purchase
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ('Requested', 'Return Requested'),
        ('Approved', 'Approved'),
        ('Pickup Scheduled', 'Pickup Scheduled'),
        ('Refunded', 'Refunded'),
        ('Rejected', 'Rejected'),
    )
    
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='return_request')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for {self.order_item.product.name}"