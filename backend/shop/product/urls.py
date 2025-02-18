from django.urls import path, include
from rest_framework.routers import DefaultRouter #  导入 Router
from .views import CategoryViewSet, ProductViewSet, ProductListView, ProductDetailView

router = DefaultRouter() #  创建 Router 实例
router.register(r'categories', CategoryViewSet, basename='category') #  注册 CategoryViewSet，URL 前缀为 categories
router.register(r'products', ProductViewSet, basename='product') #  注册 ProductViewSet，URL 前缀为 products

urlpatterns = [
    path('', include(router.urls)), #  将 Router 中的 URL 包含进来
    path('products/list/', ProductListView.as_view(), name='product-list-customer'), #  顾客端商品列表
    path('products/<int:pk>/detail/', ProductDetailView.as_view(), name='product-detail-customer'), #  顾客端商品详情
]