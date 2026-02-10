from django.db import models
from django.conf import settings

# --- BANNER MODEL (For Sliders and Ads) ---
class Banner(models.Model):
    SECTION_CHOICES = (
        ('Main Slider', 'Main Slider'),
        ('Mid Strip', 'Mid Strip (Ads)'),
        ('Footer', 'Footer'),
    )
    
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.CharField(max_length=500, blank=True, help_text="URL to redirect when clicked")
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='Main Slider')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1, help_text="Order of display (1 shows first)")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.section})"

# --- CONTACT FORM MODEL ---
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.name} - {self.subject}"

# --- STATIC PAGES (About Us, Terms, etc.) ---
class StaticPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField(help_text="HTML Content allowed")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# --- NOTIFICATIONS MODEL ---
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user}"

