from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend   # * 用于过滤
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.shop import order
from .models import Order, OrderItem, ShippingAddress, BillingAddress, Payment
from .serializers import OrderSerializer, OrderItemSerializer, ShippingAddressSerializer, BillingAddressSerializer, PaymentSerializer
# TODO 可能还需要在这里导入自定义个管理员权限类

class OrderViewSet(viewsets.ModelViewSet):
    """管理员订单管理"""
    queryset = Order.objects.all().order_by('-order_date')  # 按订单日期排序
    serializer_class = OrderSerializer
    # permission_classes = [IsAdminUserOrOperator] # ! 管理员或运营人员权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # * 可以按订单状态、支付状态、支付方式、用户 筛选
    filterset_fields = ['order_status', 'payment_status', 'payment_method', 'user']
    # * 可以按订单号、备注、用户名、邮箱 搜索
    search_fields = ['order_number', 'note', 'user__username', 'user__email'] 
    # * 可以按订单日期、总价、订单状态、支付状态 排序
    ordering_fields = ['order_date', 'order_total', 'order_status', 'payment_status'] 

    def perform_destory(self, instance):
        return Response({"error": "Order deletion is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CustomerOrderViewSet(viewsets.ModelViewSet):
    """顾客订单管理"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # 需要用户认证

    def get_queryset(self):
        """只返回当前用户的订单"""
        return Order.objects.filter(user=self.request.user).order_by('-order_date')
    
    def perform_create(self, serializer):
        """创建订单时自动关联到当前用户"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['PATCH'])
    def cancel(self, request, pk=None):
        """自定义action,取消订单"""
        order = self.get_object()   # 获取当前订单
        # * 只有在“待支付”或“处理中”状态才能取消
        if order.order_status in ['pending_payment', 'processing']:
            order.order_status = 'canceled'
            order.save()
            return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Order cannot be cancelled in current status."}, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_destroy(self, instance):
        return Response({"error": "Order deletion is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class OrderPaymentView(generics.GenericAPIView):
    """订单支付"""
    # * 需要用户认证
    permission_classes = [permissions.IsAuthenticated]
    # * 可以使用PaymentSerializer,也可以自定义更简单的Serializer
    serializer_class = PaymentSerializer

    def post(self, request, pk=None):
        # * 获取当前订单，需要重写get_object()方法,根据pk和当前用户获取订单
        order = self.get_object()
        payment_method = request.data.get('payment_method') # 获取支付方式
        # TODO 调用支付平台API，生成支付链接或者二维码之类的
        # payment_url_or_qrcode = "https://<payment-gateway>/pay?order_id="+str(order.order_number)
        # return Response({"payment_url": payment_url_or_qrcode, "message": "Payment initiated."}, status=status.HTTP_200_OK)
    
# TODO 支付结果回调View(Webhook) - 后续实现 