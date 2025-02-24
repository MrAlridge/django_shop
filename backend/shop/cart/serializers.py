from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # * 嵌套 ProductSerializer，只展示部分字段
    product = ProductSerializer(read_only=True, fields=['id', 'name', 'short_description', 'price', 'images'])
    # * 购物车项，只读
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    # * 嵌套 CartItemSerializer，展示购物车中的商品项列表
    items = CartItemSerializer(many=True, read_only=True)
    # * 购物车商品总数，只读
    total_items = serializers.IntegerField(read_only=True)
    # * 购物车总价，只读
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total_items', 'total_price']
        # ! 用户、创建/更新时间、商品项列表、总数、总价只读
        read_only_fields = ['user', 'created_at', 'updated_at', 'items', 'total_items', 'total_price']