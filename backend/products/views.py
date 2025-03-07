from rest_framework import viewsets, permissions, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    商品分类 API 接口
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    # permission_classes = [permissions.IsAdminUser] #  这里先设置只有管理员用户可以操作商品分类数据，后续根据需求调整权限

class ProductPagination(pagination.PageNumberPagination):
    """商品列表分页器"""
    page_size = 10  # 默认每页显示数量
    page_size_query_param = 'page_size' # * 允许客户端通过`page_size`参数自定义每页数量
    max_page_size = 100 # 客户端可设置的最大每页数量

class ProductViewSet(viewsets.ModelViewSet):
    """
    商品 API 接口
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser] # 这里先设置只有管理员用户可以操作商品数据，后续根据需求调整权限
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'is_on_sale', 'price']  # 指定可以用于筛选的字段
    ordering_fields = ['price', 'created_at', 'updated_at'] # 指定可以用于排序的字段
    ordering = ['-created_at']      # 默认排序字段，这里默认按照创建时间倒序排列
    pagination_class = ProductPagination