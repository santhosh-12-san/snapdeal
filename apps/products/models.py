from django.db import models
from django.conf import settings
from django.db.models import Avg
from apps.vendors.models import Vendor # Ensure you have the 'vendors' app created 
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        original_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    # --- RELATIONSHIPS ---
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    # --- BASIC INFO ---
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    
    # --- PRICING ---
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # --- INVENTORY & RATING (Missing in your previous code!) ---
    stock = models.PositiveIntegerField(default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # --- DEAL FIELDS ---
    is_deal_of_day = models.BooleanField(default=False)
    discount_label = models.CharField(max_length=50, blank=True, help_text="e.g. 'UNDER 499'")

    is_new_arrival = models.BooleanField(default=False, help_text="Check this to show in 'New Arrivals' section")
    
    # --- META ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        """Calculates percentage off"""
        if self.original_price > 0:
            return int(((self.original_price - self.selling_price) / self.original_price) * 100)
        return 0

    def update_rating(self):
        """Recalculates average rating"""
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = round(average, 1) if average else 0.0
        self.review_count = self.reviews.count()
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        original_slug = self.slug
        counter = 1
        while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

# --- SUPPORTING MODELS ---

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=10) 
    stock = models.PositiveIntegerField(default=10) 

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50) 
    color_code = models.CharField(max_length=20, blank=True, null=True) 
    image = models.ImageField(upload_to='products/colors/', blank=True, null=True) 

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=100) 
    value = models.CharField(max_length=255) 

# --- REVIEWS ---

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)]) 
    title = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

# --- HISTORY ---

class ProductVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.product.name} viewed at {self.timestamp}"
# --- ATTRIBUTES (Dynamic Specs like RAM, Material, etc.) ---
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)  # e.g., "Screen Size"
    value = models.CharField(max_length=100) # e.g., "6.5 inches"

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"