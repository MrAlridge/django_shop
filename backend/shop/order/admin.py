from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, BillingAddress, OrderStatusLog

# 注册 Order 模型并自定义 Admin 界面
class OrderItemInline(admin.TabularInline): # 使用 TabularInline 以表格形式显示 OrderItem
    model = OrderItem
    extra = 1 # 默认显示一个空的表单行用于添加新的 OrderItem
    readonly_fields = ['item_total'] #  OrderItem 总价只读

class OrderStatusLogInline(admin.TabularInline): # 使用 TabularInline 以表格形式显示 OrderStatusLog
    model = OrderStatusLog
    extra = 0 # 默认不显示额外的空表单行
    readonly_fields = ['timestamp'] #  状态日志时间戳只读


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Order 模型 Admin 管理类
    - 自定义订单在 Admin 后台的显示和管理方式
    """
    list_display = ['order_number', 'user', 'order_date', 'order_status', 'final_total', 'payment_method'] #  列表页显示的字段
    list_filter = ['order_status', 'payment_method', 'order_date'] #  列表页可以使用的过滤器
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_address__full_name', 'billing_address__full_name'] #  可以搜索的字段
    ordering = ['-order_date'] #  默认排序方式，按订单日期倒序
    readonly_fields = ['order_number', 'order_date', 'order_total', 'final_total', 'created_at', 'updated_at'] #  只读字段，创建后不可编辑
    # fields = [...] #  自定义表单字段的排列方式 (可选，如果需要更精细的控制)
    fieldsets = ( #  使用 fieldsets 分组显示字段，更清晰
        ('订单信息', {
            'fields': ('order_number', 'order_date', 'user', 'order_status', 'payment_method', 'transaction_id', 'customer_notes')
        }),
        ('金额信息', {
            'fields': ('order_total', 'shipping_fee', 'discount_amount', 'final_total')
        }),
        ('地址信息', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [OrderItemInline, OrderStatusLogInline] #  在 OrderAdmin 页面内嵌显示 OrderItem 和 OrderStatusLog
    actions = ['cancel_orders', 'mark_orders_as_shipped'] #  自定义批量操作 action

    def cancel_orders(self, request, queryset): # 自定义 action: 批量取消订单
        """批量取消订单的 Admin Action"""
        updated_count = queryset.update(order_status='CANCELLED') #  批量更新订单状态为取消
        for order in queryset: #  为每个取消的订单创建状态日志
            OrderStatusLog.objects.create(order=order, status='CANCELLED', notes='Admin后台批量操作取消订单', user=request.user) #  记录状态日志，可以记录操作用户
        self.message_user(request, f"成功取消 {updated_count} 个订单") #  后台消息提示
    cancel_orders.short_description = "批量取消选中的订单" #  Admin Action 描述

    def mark_orders_as_shipped(self, request, queryset): # 自定义 action: 批量标记为已发货
        """批量标记订单为已发货的 Admin Action"""
        updated_count = queryset.update(order_status='SHIPPED') #  批量更新订单状态为已发货
        for order in queryset: #  为每个标记发货的订单创建状态日志
            OrderStatusLog.objects.create(order=order, status='SHIPPED', notes='Admin后台批量操作标记为已发货', user=request.user) # 记录状态日志，可以记录操作用户
        self.message_user(request, f"成功标记 {updated_count} 个订单为已发货") # 后台消息提示
    mark_orders_as_shipped.short_description = "批量标记选中的订单为已发货" # Admin Action 描述


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """OrderItem 模型 Admin 管理类"""
    list_display = ['order', 'product', 'quantity', 'price', 'item_total'] # 列表页显示的字段
    list_filter = ['order__order_status', 'product__category'] #  列表页过滤器
    search_fields = ['order__order_number', 'product__name'] # 搜索字段
    readonly_fields = ['item_total'] # 只读字段


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """ShippingAddress 模型 Admin 管理类"""
    list_display = ['full_name', 'phone_number', 'city', 'country', 'user', 'is_default'] # 列表页显示字段
    list_filter = ['country', 'is_default'] # 过滤器
    search_fields = ['full_name', 'phone_number', 'city', 'state_province', 'postal_code', 'address_line1', 'address_line2', 'user__username', 'user__email'] # 搜索字段


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    """BillingAddress 模型 Admin 管理类"""
    list_display = ['full_name', 'phone_number', 'city', 'country', 'user'] # 列表页显示字段
    list_filter = ['country'] # 过滤器
    search_fields = ['full_name', 'phone_number', 'city', 'state_province', 'postal_code', 'address_line1', 'address_line2', 'user__username', 'user__email'] # 搜索字段


# @admin.register(OrderStatusLog)
# class OrderStatusLogAdmin(admin.ModelAdmin):
#     """OrderStatusLog 模型 Admin 管理类"""
#     list_display = ['order', 'status', 'timestamp', 'user'] # 列表页显示字段
#     list_filter = ['status', 'timestamp'] # 过滤器
#     search_fields = ['order__order_number', 'status', 'notes', 'user__username'] # 搜索字段
#     readonly_fields = ['timestamp', 'order', 'status', 'notes', 'user'] #  全部字段只读，状态日志通常不应该在后台修改

#     def get_user_username(self, obj):
#         """获取关联用户的用户名"""
#         if obj.user:
#             return obj.user.username
#         return None


# ! 以下是简单注册，无需在意，只有特殊情况下会启用
# admin.site.register(Order, OrderAdmin) # 使用自定义的 OrderAdmin
# admin.site.register(OrderItem, OrderItemAdmin) # 使用自定义的 OrderItemAdmin
# admin.site.register(ShippingAddress, ShippingAddressAdmin) # 使用自定义的 ShippingAddressAdmin
# admin.site.register(BillingAddress, BillingAddressAdmin) # 使用自定义的 BillingAddressAdmin
# admin.site.register(OrderStatusLog, OrderStatusLogAdmin) # 使用自定义的 OrderStatusLogAdmin