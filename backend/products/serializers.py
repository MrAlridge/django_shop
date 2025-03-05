from rest_framework import serializers
from .models import ProductCategory, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__' #  使用 '__all__' 包含所有字段，简单起见，可以根据需要显式列出字段


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True) #  嵌套 ProductCategorySerializer，用于展示商品分类的详细信息
    image = serializers.ImageField(required=False) #  ImageField 需要特别声明, required=False 表示图片不是必须的
    related_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__' # 使用 '__all__' 包含所有字段，简单起见，可以根据需要显式列出字段
        # fields = ['id', 'name', 'description', 'price', 'image', 'stock', 'is_on_sale', 'category'] #  也可以显式列出需要的字段

    def get_related_products(self, instance):
        """获取关联商品"""
        # TODO 等具体需求下来再对推荐做细化
        # * 获取同分类下的商品，排除当前商品,最多返回4个
        related = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:4]
        # 序列化关联商品并返回data
        return ProductSerializer(related, many=True, context={'request': self.context.get('request')}).data
