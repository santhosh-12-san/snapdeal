from django.db import models
from django.conf import settings
from apps.products.models import Product

# Simple link between User and Product
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Prevent duplicate adds

    def __str__(self):
        return f"{self.user} - {self.product}"