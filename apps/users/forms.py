from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'mobile_number') # Add other fields if needed

class CustomAuthenticationForm(AuthenticationForm):
    # This usually works fine, but good to have just in case
    class Meta:
        model = CustomUser
        