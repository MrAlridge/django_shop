from django.db import models
from django.conf import settings

class Cart(models.Model):
    """
    购物车主模型，每个用户对应一个购物车。

    :integer id: 购物车 ID (自动生成)
    :User user: 所属用户 (ForeignKey，关联到 User 模型，一对一关系 OneToOneField 更合适，每个用户只有一个购物车)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTime updated_at: 更新时间 (DateTimeField)
    """
    # ! 一对一关联 User 模型，每个用户只有一个购物车
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for user {self.user.username}"
    
    @property
    def total_items(self):  # ? 计算购物车商品总数
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):  # ? 计算购物车总价
        return sum(item.total_price for item in self.items.all())
    
class CartItem(models.Model):
    """
    购物车项模型，存储购物车中每个商品的详细信息。

    :integer id: 购物车项 ID (自动生成)
    :Cart cart: 所属购物车 (ForeignKey，关联到 Cart 模型)
    :Product product: 购物车中的商品 (ForeignKey，关联到 Product 模型)
    :integer quantity: 商品数量 (IntegerField, 默认为 1)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTime updated_at: 更新时间 (DateTimeField)
    """
    # * 关联Cart模型
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # * 关联 Product 模型，注意 product 应用的模型需要使用 'product.Product' 引用
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='cart_items')
    # * 商品数量，默认为1
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ! 同一购物车中，商品不能重复添加，使用 unique_together 约束
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart #{self.cart.id}"
    
    @property
    def total_price(self):  # * 计算购物车商品总价
        # ! 注意这里使用商品当前价格，购物车价格可能随商品价格变动而变动
        return self.quantity * self.product.price