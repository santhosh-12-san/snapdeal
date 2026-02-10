from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'user__mobile_number', 'user__email')
    inlines = [OrderItemInline] # Shows items inside the order page

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'status', 'refund_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_item__order__order_id',)