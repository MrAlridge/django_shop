from rest_framework import viewsets, permissions
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    商品分类 API 接口
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAdminUser] #  这里先设置只有管理员用户可以操作商品分类数据，后续根据需求调整权限


class ProductViewSet(viewsets.ModelViewSet):
    """
    商品 API 接口
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser] # 这里先设置只有管理员用户可以操作商品数据，后续根据需求调整权限