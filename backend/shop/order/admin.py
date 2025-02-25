from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_date', 'order_total', 'shipping_fee', 'order_status', 'payment_method', 'payment_status', 'shipping_address', 'billing_address', 'note', 'created_at', 'updated_at')
    list_filter = ('user', 'order_date', 'order_status', 'payment_method', 'payment_status')
    search_fields = ('note', 'shipping_address', 'billing_address')
    ordering = ('-created_at', '-order_date', '-order_total')

admin.site.register(Order, OrderAdmin)