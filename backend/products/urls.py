from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'product-categories', views.ProductCategoryViewSet) #  注册商品分类的路由
router.register(r'products', views.ProductViewSet) # 注册商品的路由

urlpatterns = [
    path('', include(router.urls)),
]