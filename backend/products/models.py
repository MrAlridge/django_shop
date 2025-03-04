from django.db import models

class ProductCategory(models.Model):
    """
    商品分类
    """
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(null=True, blank=True, verbose_name='分类描述')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    商品
    """
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name='商品分类') # 关联商品分类
    name = models.CharField(max_length=200, verbose_name='商品名称')
    description = models.TextField(null=True, blank=True, verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='商品图片') # 商品图片，上传到 products/ 目录
    stock = models.IntegerField(default=0, verbose_name='商品库存')
    is_on_sale = models.BooleanField(default=False, verbose_name='是否促销')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name