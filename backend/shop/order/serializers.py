from rest_framework import serializers
from .models import OrderItem, ShippingAddress, BillingAddress, Payment, Order
from usermgmt.serializers import UserProfileSerializer
# * 导入自身模块的Serializer
from .serializers import OrderItemSerializer, ShippingAddressSerializer, BillingAddressSerializer, PaymentSerializer
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    # * 嵌套ProductSerializer，只展示部分字段
    product = ProductSerializer(read_only=True, fields=['id', 'name', 'short_description', 'price', 'images'])

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']
        read_only_fields = ['total_price'] # 订单项总价只读

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'name', 'phone_number', 'province', 'city', 'district', 'address_detail', 'postal_code']

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id', 'name', 'phone_number', 'province', 'city', 'district', 'address_detail', 'postal_code']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_id', 'payment_date', 'payment_amount', 'payment_method', 'payment_status', 'raw_response']
        read_only_fields = ['payment_date']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # 嵌套 OrderItemSerializer
    shipping_address_detail = ShippingAddressSerializer(read_only=True) # 嵌套 ShippingAddressSerializer
    billing_address_detail = BillingAddressSerializer(read_only=True) # 嵌套 BillingAddressSerializer
    payment_detail = PaymentSerializer(read_only=True) # 嵌套 PaymentSerializer
    user = UserProfileSerializer(read_only=True, fields=['id', 'username', 'email']) # 嵌套 UserProfileSerializer，只展示部分字段

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'order_date', 'order_total', 'shipping_fee', 'order_status', 'payment_method', 'payment_status', 'shipping_address_detail', 'billing_address_detail', 'note', 'created_at', 'updated_at', 'items', 'payment_detail']
        read_only_fields = ['order_number', 'order_date', 'order_total', 'created_at', 'updated_at', 'items', 'payment_detail', 'shipping_address_detail', 'billing_address_detail', 'user'] #  订单编号、日期、总价、创建/更新时间、订单项、支付信息、地址信息只读

