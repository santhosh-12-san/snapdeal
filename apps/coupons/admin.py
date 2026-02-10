from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'valid_from', 'valid_to', 'active')
    list_filter = ('active', 'valid_to')
    search_fields = ('code',)