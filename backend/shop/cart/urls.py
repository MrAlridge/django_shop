from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
# * 购物车管理，URL前缀为 /api/cart/
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)), # 包含 Router 中的URL
]
