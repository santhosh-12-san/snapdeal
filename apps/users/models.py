from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# --- 1. CUSTOM USER MODEL ---
class CustomUser(AbstractUser):
    # Validates that the input looks like a phone number
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter valid mobile number")
    
    # The main login field
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, unique=True)
    
    # Secondary field (optional, keeping it since you had it before)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    is_verified = models.BooleanField(default=False) 

    # Tell Django to use 'mobile_number' as the unique identifier for login
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['username', 'email'] 

    def __str__(self):
        return self.mobile_number


# --- 2. ADDRESS MODEL ---
class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    locality = models.CharField(max_length=100)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='Home')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.city}"


# --- 3. OTP MODEL ---
class PhoneOTP(models.Model):
    mobile_number = models.CharField(max_length=17, unique=True)
    otp = models.CharField(max_length=6)
    count = models.IntegerField(default=0, help_text="Number of OTPs sent")
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mobile_number} - {self.otp}"