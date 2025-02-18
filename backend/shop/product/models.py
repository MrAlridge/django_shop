from django.db import models
from django.utils.text import slugify
import decimal

class Category(models.Model):
    """
    模型:  商品分类模型，用于组织商品。
    
    :integer id: 分类 ID (自动生成)
    :string name: 分类名称 (CharField)
    :string description: 分类描述 (TextField, 可选)
    :Category parent_category: 父级分类 (ForeignKey,关联到自身,允许为空,用于创建多级分类，例如 "食品" -> "水果" -> "苹果")
    :string image: 分类图片 (ImageField, 可选，用于展示分类图标)
    :Slug slug: Slug 字段 (SlugField,用于 URL 优化，例如将 "新鲜水果" 转换为 "xin-xian-shui-guo")
    :string created_at: 创建时间 (DateTimeField)
    :string updated_at: 更新时间 (DateTimeField)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE) # 关联自身，父级分类
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True) #  Slug 字段

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories' #  管理后台显示复数形式

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): #  自动生成 Slug
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    """商品模型，存储商品的核心信息。

    :integer id: 商品 ID (自动生成)
    :string name: 商品名称 (CharField)
    :string description: 商品详细描述 (TextField)
    :string short_description: 商品简短描述 (CharField, 可用于列表展示)
    :Decmical price: 商品价格 (DecimalField,使用 decimal.Decimal 类型，精确存储价格)
    :Decmical discount_price: 折扣价 (DecimalField, 可选，用于促销)
    :integer stock_quantity: 库存数量 (IntegerField)
    :Category category: 商品所属分类 (ForeignKey,关联到 Category 模型)
    :string brand: 品牌 (CharField, 可选)
    :string unit: 单位 (CharField, 例如 "个", "公斤", "箱")
    :string barcode: 条形码 (CharField, 可选，唯一性约束)
    :string sku: SKU (Stock Keeping Unit, 商品SKU编码) (CharField, 唯一性约束)
    :boolean is_active: 是否上架 (BooleanField,控制商品是否在 APP 中显示，默认为 True)
    :string created_at: 创建时间 (DateTimeField)
    :string updated_at: 更新时间 (DateTimeField)
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True) # 简短描述
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #  DecimalField 存储价格
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 折扣价
    stock_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') #  关联 Category 模型
    brand = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True) # 条形码，允许为空
    sku = models.CharField(max_length=100, unique=True) #  SKU，唯一
    is_active = models.BooleanField(default=True) #  是否上架，默认上架

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """商品图片模型，一个商品可以有多张图片。

    :integer id: 图片 ID (自动生成)
    :Product product: 关联的商品 (ForeignKey,关联到 Product 模型)
    :string image: 图片文件 (ImageField,存储商品图片)
    :boolean is_main: 是否为主图 (BooleanField,用于标记商品主图,默认为 False,一个商品只能有一张主图)
    :integer order: 图片顺序 (IntegerField,用于控制图片在商品详情页的展示顺序)
    :string created_at: 创建时间 (DateTimeField)
    :string updated_at: 更新时间 (DateTimeField)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images') #  关联 Product 模型
    image = models.ImageField(upload_to='product_images/') #  商品图片上传目录
    is_main = models.BooleanField(default=False) #  是否为主图
    order = models.IntegerField(default=0) #  图片顺序

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"