from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action # 自定义action
from rest_framework.response import Response
from .models import Cart, CartItem
from product.models import Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):    # * 使用ViewSet，自定义增删改查逻辑
    permission_classes = [permissions.IsAuthenticated]  # ! 需要用户认证

    def retrieve(self, request):
        # ? 获取或创建当前用户的购物车
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # * 添加商品到购物车 action，URL: /api/cart/items/
    @action(detail=False, methods=['POST'], url_path=['items'])
    def add_item(self, request):
        """添加到购物车"""
        # ? 获取或创建当前用户的购物车
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # 默认数量为1

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(pk=product_id, is_active=True)    # ? 获取商品并检查商品是否上架
        except Product.DoesNotExist:
            return Response({"error": "Product not found or is not active."}, status=status.HTTP_404_NOT_FOUND)
        # ? 检查库存是否充足
        if product.stock_quantity < int(quantity):
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 尝试获取已存在的购物车项
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += int(quantity) # 如果已存在就增加数量
            cart_item.save()
        except CartItem.DoesNotExist:
            # 如果不存在这个购物车项就创建一个
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # * 更新购物车商品项数量 action，URL: /api/cart/items/{item_id}/
    @action(detail=False, methods=['PATCH'], url_path='items/(?P<item_id>\d+)')
    def update_item(self, request, item_id=None):
        try:
            cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        quantity = request.data.get('quantity')
        if not quantity:
            return Response({"error": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if cart_item.product.stock_quantity < int(quantity):
            # ? 再次检查库存是否充足
            return Response({"error": "Insufficient stock."}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # * 删除购物车商品项 action，URL: /api/cart/items/{item_id}/
    @action(detail=False, methods=['DELETE'], url_path='items/(?<item_id>\d+)')
    def remove_item(self, request, item_id=None):
        try:
            cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        # ! 204 No Content，表示请求成功，但没有返回内容
        return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    # * 清空购物车 action，URL: /api/cart/clear/
    @action(detail=False, methods=['DELETE'], url_path='clear')
    def clear(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()   # ! 删除购物车中的所有商品项
        return Response({"message": "Cart cleared successfully."}, status=status.HTTP_204_NO_CONTENT)