from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shipping-addresses', views.ShippingAddressViewSet, basename='shipping-address') #  注册配送地址ViewSet
router.register(r'billing-addresses', views.BillingAddressViewSet, basename='billing-address') #  注册账单地址ViewSet

urlpatterns = [
    path('orders/', views.OrderCreateView.as_view(), name='order-create'), # 创建订单
    path('orders/', views.OrderListView.as_view(), name='order-list'), # 订单列表
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'), # 订单详情
    path('orders/<int:order_id>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'), # 订单状态更新

    path('', include(router.urls)), #  包含 ViewSet 的路由
]