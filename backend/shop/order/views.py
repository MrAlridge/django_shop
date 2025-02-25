# ./order/views.py
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import exceptions

from .models import Order, OrderItem, ShippingAddress, BillingAddress, OrderStatusLog
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
    ShippingAddressSerializer,
    BillingAddressSerializer,
)
from product.models import Product # 假设 product 应用有 Product 模型  * 确保 product 应用的 model 导入正确
# from .permissions import IsAdminOrReadOnly, IsOrderOwnerOrAdmin #  *  可以自定义权限类，例如订单Owner权限，管理员权限 (如果需要更细粒度的权限控制)


class OrderCreateView(generics.CreateAPIView):
    """
    订单创建 API 视图
    - 允许用户创建新的订单
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated] #  *  需要用户认证才能创建订单

    def perform_create(self, serializer):
        """
        重写 perform_create 方法，在订单创建时保存用户和 request 信息到 context 中
        并在 serializer 的 create 方法中获取 user
        """
        serializer.save(user=self.request.user, request=self.request) #  将 request 放入 serializer 的 context 中


class OrderListView(generics.ListAPIView):
    """
    订单列表 API 视图
    - 获取当前用户的订单列表
    - 支持分页和状态筛选
    """
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated] #  *  需要用户认证才能查看订单列表
    filterset_fields = ['order_status'] #  *  允许根据订单状态筛选
    ordering_fields = ['order_date', 'final_total'] # * 允许根据订单日期和总金额排序

    def get_queryset(self):
        """
        重写 get_queryset 方法，只返回当前用户的订单
        """
        return Order.objects.filter(user=self.request.user).order_by('-order_date') #  *  默认按订单日期倒序排列


class OrderDetailView(generics.RetrieveAPIView):
    """
    订单详情 API 视图
    - 获取指定订单 ID 的详细信息
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated] #  *  需要用户认证才能查看订单详情
    lookup_field = 'order_id' #  *  使用 order_id 作为 lookup field
    queryset = Order.objects.all() #  *  queryset 需要包含所有订单，权限控制在 get_object 中

    def get_object(self):
        """
        重写 get_object 方法，确保用户只能访问自己的订单，管理员可以访问所有订单
        """
        queryset = self.filter_queryset(self.get_queryset()) # 应用过滤器 (虽然这里没有用到)
        order_id = self.kwargs.get('order_id') # 获取 URL 中的 order_id
        obj = get_object_or_404(queryset, order_id=order_id) #  根据 order_id 获取订单，不存在则 404

        # *  权限检查：用户只能查看自己的订单，管理员可以查看所有订单
        if obj.user != self.request.user and not self.request.user.is_staff: #  示例权限判断
            raise exceptions.PermissionDenied("您无权查看此订单详情") #  返回 403 Forbidden

        self.check_object_permissions(self.request, obj) #  DRF 默认的对象级别权限检查 (这里没有配置对象级别权限)
        return obj


class OrderStatusUpdateView(generics.UpdateAPIView):
    """
    订单状态更新 API 视图 (管理员或特定角色使用)
    - 更新指定订单 ID 的订单状态
    """
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser] #  *  只有管理员才能更新订单状态  (可以根据实际需求修改权限)
    lookup_field = 'order_id' #  *  使用 order_id 作为 lookup field
    queryset = Order.objects.all() #  *  queryset 需要包含所有订单，管理员可以更新所有订单状态

    def perform_update(self, serializer):
        """
        重写 perform_update 方法，在订单状态更新时记录订单状态日志
        """
        order = self.get_object() # 获取要更新的订单实例
        old_status = order.order_status #  记录更新前的订单状态
        serializer.save() #  更新订单状态

        new_status = serializer.validated_data.get('order_status') # 获取更新后的订单状态
        notes = serializer.validated_data.get('notes') # 获取更新备注
        if old_status != new_status: #  只有状态发生变化时才记录日志
            OrderStatusLog.objects.create(order=order, status=new_status, notes=notes, user=self.request.user) #  *  记录订单状态日志，可以记录操作用户


class ShippingAddressViewSet(viewsets.ModelViewSet):
    """
    配送地址 API 视图集 (CRUD)
    - 提供配送地址的 增删改查 API 接口
    """
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated] #  *  需要用户认证才能管理配送地址

    def get_queryset(self):
        """
        重写 get_queryset 方法，只返回当前用户的配送地址
        """
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-is_default', '-updated_at') # * 默认按照是否默认地址和更新时间排序

    def perform_create(self, serializer):
        """
        重写 perform_create 方法，在创建配送地址时关联当前用户
        并设置新地址为默认地址，取消其他地址的默认设置 (如果需要)
        """
        is_default = serializer.validated_data.get('is_default', False) #  获取是否设置为默认地址
        if is_default: # 如果设置为默认地址，取消其他地址的默认设置 (根据业务需求决定是否需要)
            ShippingAddress.objects.filter(user=self.request.user, is_default=True).update(is_default=False) #  *  取消当前用户其他默认地址
        serializer.save(user=self.request.user) #  关联当前用户

    def perform_update(self, serializer):
        """
        重写 perform_update 方法，在更新配送地址时，如果设置了默认地址，取消其他地址的默认设置 (如果需要)
        """
        is_default = serializer.validated_data.get('is_default', False) #  获取是否设置为默认地址
        if is_default: # 如果设置为默认地址，取消其他地址的默认设置 (根据业务需求决定是否需要)
            ShippingAddress.objects.filter(user=self.request.user, is_default=True).exclude(pk=self.kwargs['pk']).update(is_default=False) #  *  取消当前用户其他默认地址，排除当前更新的地址
        serializer.save()

    @action(detail=True, methods=['POST']) #  *  自定义 action，设置默认地址
    def set_default(self, request, pk=None):
        """
        设置默认配送地址 action
        - POST /api/shipping-addresses/{shipping_address_id}/set_default/
        """
        shipping_address = self.get_object() # 获取当前配送地址实例
        if shipping_address.user != request.user: # *  权限校验，只能设置自己的地址为默认地址
            return Response({"error": "您无权操作此地址"}, status=status.HTTP_403_FORBIDDEN)

        ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False) #  取消当前用户其他默认地址
        shipping_address.is_default = True #  设置当前地址为默认地址
        shipping_address.save()
        return Response({"message": "默认地址设置成功"}, status=status.HTTP_200_OK)


class BillingAddressViewSet(viewsets.ModelViewSet):
    """
    账单地址 API 视图集 (CRUD) -  *  初期可以和配送地址ViewSet复用逻辑，或者简化实现
    - 提供账单地址的 增删改查 API 接口， 可以根据实际需求调整功能
    """
    serializer_class = BillingAddressSerializer
    permission_classes = [permissions.IsAuthenticated] #  *  需要用户认证才能管理账单地址

    def get_queryset(self):
        """
        重写 get_queryset 方法，只返回当前用户的账单地址
        """
        return BillingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        重写 perform_create 方法，在创建账单地址时关联当前用户
        """
        serializer.save(user=self.request.user)