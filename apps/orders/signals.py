from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from apps.products.models import Product

@receiver(post_save, sender=OrderItem)
def decrease_stock_on_order(sender, instance, created, **kwargs):
    """
    When an OrderItem is created, automatically subtract 
    the quantity from the Product's stock.
    """
    if created:
        product = instance.product
        order_qty = instance.quantity
        
        if product.stock >= order_qty:
            product.stock -= order_qty
            product.save()
            print(f"📉 Stock Updated: {product.name} dropped to {product.stock}")
        else:
            # Logic to handle out of stock (Optional: Cancel order or notify admin)
            print(f"⚠️ WARNING: Order placed for {product.name} but stock is low!")