from rest_framework import viewsets, generics, permissions, filters
# TODO: 这个依赖可能是Gemini生成出问题了？
# from django_filters import DjangoFilterBackend #  用于过滤
from rest_framework.decorators import action #  自定义 action
from rest_framework.response import Response
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer

class CategoryViewSet(viewsets.ModelViewSet): #  ModelViewSet 提供 CRUD 功能
    """使用 `ModelViewSet` 提供商品分类的 CRUD API。

    *   `list`:  获取商品分类列表 (`GET /api/categories/`)
    *   `create`:  创建商品分类 (`POST /api/categories/`)
    *   `retrieve`:  获取单个商品分类详情 (`GET /api/categories/{id}/`)
    *   `update`:  更新商品分类 (`PUT /api/categories/{id}/` 或 `PATCH /api/categories/{id}/`)
    *   `destroy`:  删除商品分类 (`DELETE /api/categories/{id}/`)
    *   **权限控制:**  只有管理员角色可以进行 CRUD 操作。
    """
    queryset = Category.objects.all().order_by('name') #  按名称排序
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser] #  只有管理员可以操作分类

class ProductViewSet(viewsets.ModelViewSet): #  ModelViewSet 提供 CRUD 功能
    """**`ProductViewSet` (商品管理):**  使用 `ModelViewSet` 提供商品的 CRUD API。

    *   `list`:  获取商品列表 (`GET /api/products/`)，支持分页、搜索、筛选、排序。
    *   `create`:  创建商品 (`POST /api/products/`)
    *   `retrieve`:  获取单个商品详情 (`GET /api/products/{id}/`)
    *   `update`:  更新商品 (`PUT /api/products/{id}/` 或 `PATCH /api/products/{id}/`)
    *   `destroy`:  删除商品 (`DELETE /api/products/{id}/`)
    *   **权限控制:**  只有管理员角色可以进行 CRUD 操作。
    """
    queryset = Product.objects.all().order_by('-created_at') #  按创建时间倒序排序，默认显示最新的商品
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser] #  只有管理员可以操作商品
    # TODO: 依赖修复完成要添加上DjangoFilterBackend
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] #  添加过滤、搜索、排序后端
    filterset_fields = ['category', 'brand', 'is_active'] #  可以按分类、品牌、是否上架 过滤
    search_fields = ['name', 'description', 'short_description', 'brand'] #  可以按商品名称、描述、品牌搜索
    ordering_fields = ['price', 'created_at', 'stock_quantity'] #  可以按价格、创建时间、库存排序

    @action(detail=True, methods=['POST']) #  自定义 action，用于上传商品图片，detail=True 表示作用于单个商品
    def upload_image(self, request, pk=None):
        product = self.get_object() #  获取当前商品
        serializer = ProductImageSerializer(data=request.data) #  使用 ProductImageSerializer 验证数据
        if serializer.is_valid():
            serializer.save(product=product) #  保存图片，关联到当前商品
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ProductListView(generics.ListAPIView): #  ListAPIView 只提供列表获取功能
    """**`ProductListView` (商品列表 - 顾客端):**  提供顾客端商品列表接口，用于 APP 首页、商品列表页展示。

    *   `get`:  获取商品列表 (`GET /api/products/list/`)，支持分页、分类筛选、关键词搜索、排序 (例如按价格、销量、新品)。
    *   **权限控制:**  公开接口，无需认证。
    """
    queryset = Product.objects.filter(is_active=True).order_by('-created_at') #  只显示上架商品，并按创建时间倒序
    serializer_class = ProductSerializer
    # TODO: 依赖修复完成要添加上DjangoFilterBackend
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand'] #  顾客端可以按分类、品牌 筛选
    search_fields = ['name', 'description', 'short_description'] #  顾客端可以按商品名称、描述、简短描述搜索
    ordering_fields = ['price', 'created_at', 'discount_price', 'name'] #  顾客端可以按价格、创建时间、折扣价、名称 排序
    #  TODO:  添加分页类，例如 PageNumberPagination 或 LimitOffsetPagination
    # pagination_class = 


class ProductDetailView(generics.RetrieveAPIView): #  RetrieveAPIView 只提供详情获取功能
    """**`ProductDetailView` (商品详情 - 顾客端):**  提供顾客端商品详情接口。

    *   `get`:  获取单个商品详情 (`GET /api/products/{id}/detail/`)
    *   **权限控制:**  公开接口，无需认证。
    """
    queryset = Product.objects.filter(is_active=True) #  只显示上架商品
    serializer_class = ProductSerializer