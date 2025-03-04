from rest_framework import serializers
from .models import ProductCategory, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__' #  使用 '__all__' 包含所有字段，简单起见，可以根据需要显式列出字段


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True) #  嵌套 ProductCategorySerializer，用于展示商品分类的详细信息
    image = serializers.ImageField(required=False) #  ImageField 需要特别声明, required=False 表示图片不是必须的

    class Meta:
        model = Product
        fields = '__all__' # 使用 '__all__' 包含所有字段，简单起见，可以根据需要显式列出字段
        # fields = ['id', 'name', 'description', 'price', 'image', 'stock', 'is_on_sale', 'category'] #  也可以显式列出需要的字段