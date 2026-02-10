from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, PhoneOTP

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('mobile_number', 'email', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mobile_number', 'email', 'is_verified')}),
    )
    search_fields = ('mobile_number', 'email')
    ordering = ('mobile_number',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'state', 'pincode', 'address_type')
    search_fields = ('user__mobile_number', 'name', 'pincode')
    list_filter = ('address_type', 'state')

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'otp', 'count', 'validated', 'created_at')
    search_fields = ('mobile_number',)
    list_filter = ('validated',)