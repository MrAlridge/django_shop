from django.urls import path, include
from rest_framework.routers import DefaultRouter # 导入Router
from .views import OrderViewSet, CustomerOrderViewSet, OrderPaymentView

router = DefaultRouter()
# ! 管理员订单管理,URL前缀为/api/orders/
router.register(r'orders', OrderViewSet, basename='order')
# ? 顾客订单管理,URL前缀为/api/customer/orders/
router.register(r'customer/orders', CustomerOrderViewSet, basename='customer-order')

urlpatterns = [
    # 包含Router中的URL
    path('', include(router.urls)),
    # 订单支付API
    path('customer/orders/<int:pk>/pay/', OrderPaymentView.as_view(), name='order-pay')
    # TODO 支付结果回调URL
]

