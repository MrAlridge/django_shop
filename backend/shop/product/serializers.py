from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    """序列化 Category 模型。"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_category', 'image', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at'] # Slug, 创建时间和更新时间只读   

class ProductImageSerializer(serializers.ModelSerializer):
   """序列化 Product 模型，需要嵌套 CategorySerializer 和 ProductImageSerializer 来展示分类信息和商品图片。"""
   class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'order']

class ProductSerializer(serializers.ModelSerializer):
    """序列化 ProductImage 模型。"""
    category = CategorySerializer(read_only=True) #  嵌套 CategorySerializer
    images = ProductImageSerializer(many=True, read_only=True) #  嵌套 ProductImageSerializer，一对多关系，many=True
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'short_description', 'price', 'discount_price', 'stock_quantity', 'category', 'brand', 'unit', 'barcode', 'sku', 'is_active', 'created_at', 'updated_at', 'images']
        read_only_fields = ['created_at', 'updated_at', 'images', 'category'] # 创建时间、更新时间、图片、分类字段只读