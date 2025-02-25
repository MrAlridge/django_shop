from django.contrib import admin
from .models import Cart, CartItem

# ? 先用表格嵌入表单试试效果怎么样
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)

