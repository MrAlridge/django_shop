import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte') # ? 最小价格，gte表示大于等于
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte') # ? 最大价格，gte表示小于等于

    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_active', 'min_price', 'max_price'] # * 添加价格筛选字段

