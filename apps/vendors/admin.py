from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'vendor_code', 'user', 'rating', 'created_at')
    search_fields = ('store_name', 'vendor_code')
    list_filter = ('rating',)