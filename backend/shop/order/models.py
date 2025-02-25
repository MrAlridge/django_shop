from django.db import models
from django.conf import settings  # * 导入 settings 获取 User 模型
import uuid # * 用于生成订单编号

# Create your models here.
class Order(models.Model):
    """订单主模型，存储订单的总体信息。

    :integer id: 订单 ID (自动生成)
    :string order_number: 订单编号 (CharField, 可以自动生成，例如使用 UUID 或时间戳 + 随机数，需要保证唯一性)
    :User user: 下单用户 (ForeignKey，关联到 User 模型)
    :DateTime order_date: 下单日期 (DateTimeField, 自动记录下单时间)
    :Decimal order_total: 订单总金额 (DecimalField，计算订单项总价 + 运费)
    :Decimal shipping_fee: 运费 (DecimalField, 可选，根据配送地址和商品计算)
    :string order_status: 订单状态 (CharField, 使用 choices 枚举订单状态，例如 "待支付", "待发货", "已发货", "已完成", "已取消", "退款中", "已退款")
    :string payment_method: 支付方式 (CharField, 使用 choices 枚举支付方式，例如 "支付宝", "微信支付", "银行卡", "货到付款")
    :string payment_status: 支付状态 (CharField, 使用 choices 枚举支付状态，例如 "待支付", "已支付", "支付失败", "退款中", "已退款")
    :ShippingAddress shipping_address: 收货地址 (ForeignKey，关联到 ShippingAddress 模型)
    :BillingAddress billing_address: 账单地址 (ForeignKey，关联到 BillingAddress 模型, 可选，如果账单地址和收货地址不同)
    :string note: 订单备注 (TextField, 可选，用户下单时填写的备注)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTime updated_at: 更新时间 (DateTimeField)
    """
    ORDER_STATUS_CHOICES = [
        ('PENDING_PAYMENT', '待付款'),
        ('PROCESSING', '处理中'),
        ('SHIPPED', '已发货'),
        ('DELIVERED', '已送达'),
        ('COMPLETED', '已完成'), # 订单完成，例如用户确认收货
        ('CANCELLED', '已取消'),
        ('REFUND_REQUESTED', '退款申请中'),
        ('REFUNDED', '已退款'),
        ('PAYMENT_PENDING_MOBILE_MONEY', '待支付 (移动支付)'), #  非洲移动支付可能需要额外的状态
        # ... 可以根据实际业务需求添加更多状态
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('MOBILE_MONEY', '移动支付'), # 例如 M-Pesa, MTN Mobile Money, Airtel Money 等
        ('CREDIT_CARD', '信用卡'),
        ('DEBIT_CARD', '借记卡'),
        ('CASH_ON_DELIVERY', '货到付款'),
        # ...  根据实际集成的支付方式添加
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', '待支付'),
        ('PAID', '已支付'),
        ('FAILED', '支付失败'),
        ('REFUNDING', '退款中'),
        ('REFUNDED', '已退款'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders') # 关联用户模型
    order_number = models.CharField(max_length=100, unique=True, blank=True) # 订单号
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='PENDING_PAYMENT')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True) # 允许为空，因为订单创建时可能未选择支付方式
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, related_name='orders') #  设置为 SET_NULL，避免地址删除影响订单
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, related_name='orders_billing') #  设置为 SET_NULL
    customer_notes = models.TextField(blank=True) # 订单备注，允许为空
    
    # * 订单日期相关
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number: #  自动生成订单号
            self.order_number = f"ORDER-{uuid.uuid4().hex.upper()[:10]}" #  示例订单号生成规则
        super(Order, self).save(*args, **kwargs)
    
class OrderItem(models.Model):
    """订单项模型，存储订单中每个商品的详细信息。

    :integer id: 订单项 ID (自动生成)
    :Order order: 所属订单 (ForeignKey，关联到 Order 模型)
    :Product product: 购买的商品 (ForeignKey，关联到 Product 模型)
    :integer quantity: 购买数量 (IntegerField)
    :Demical price: 商品单价 (DecimalField, 下单时的商品价格，即使商品价格后续变动，订单项的价格也保持不变)
    :Demical total_price: 订单项总价 (DecimalField, quantity * price，可以自动计算)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTime updated_at: 更新时间 (DateTimeField)
    """
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # 关联订单
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items') # 关联商品模型 (product 应用)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 下单时的商品价格
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Item {self.product.name} in Order #{self.order.order_number}"

    def save(self, *args, **kwargs):
        self.item_total = self.quantity * self.price #  自动计算商品项总价
        super(OrderItem, self).save(*args, **kwargs)

class ShippingAddress(models.Model):
    """收货地址模型，存储订单的收货地址信息。  可以考虑复用用户模块的 UserAddress 模型，或者创建独立的 ShippingAddress 模型。  这里我们先创建独立的 ShippingAddress 模型，与订单解耦更彻底。

    :integer id: 地址 ID (自动生成)
    :Order order: 所属订单 (ForeignKey，关联到 Order 模型，一对一关系 OneToOneField 更合适，一个订单只有一个收货地址)
    :string name: 收货人姓名 (CharField)
    :string phone_number: 收货人手机号 (CharField)
    :string province: 省份 (CharField)
    :string city: 城市 (CharField)
    :string district: 区/县 (CharField)
    :string address_detail: 详细地址 (CharField)
    :string postal_code: 邮政编码 (CharField, 可选)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTIme updated_at: 更新时间 (DateTimeField)
    """
    shipping_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True) # 邮政编码可能为空
    country = models.CharField(max_length=100) #  可以使用 django-countries 库

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping Address for {self.user.username} - {self.full_name}, {self.city}"
    
class BillingAddress(models.Model):
    """账单地址模型，存储订单的账单地址信息 (可选，如果需要区分收货地址和账单地址)。  模型结构与 ShippingAddress 类似。  如果账单地址和收货地址相同，可以不创建此模型，或者在 Order 模型中使用一个 Boolean 字段 is_billing_same_as_shipping 来标记是否使用相同的地址。  这里我们先创建独立的 BillingAddress 模型，以支持更灵活的场景。

    :integer id: 地址 ID (自动生成)
    :Order order: 所属订单 (ForeignKey，关联到 Order 模型，一对一关系 OneToOneField 更合适)
    :string name: 账单人姓名 (CharField)
    :string phone_number: 账单人手机号 (CharField)
    :string province: 省份 (CharField)
    :string city: 城市 (CharField)
    :string district: 区/县 (CharField)
    :string address_detail: 详细地址 (CharField)
    :string postal_code: 邮政编码 (CharField, 可选)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTIme updated_at: 更新时间 (DateTimeField)
    """
    billing_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billing_addresses')
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True) # 邮政编码可能为空
    country = models.CharField(max_length=100) #  可以使用 django-countries 库

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Billing Address for {self.user.username} - {self.full_name}, {self.city}"
    
class OrderStatusLog(models.Model):
    """订单状态日志模型"""
    status_log_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_logs')
    status = models.CharField(max_length=50, choices=Order.ORDER_STATUS_CHOICES) #  复用 Order 模型的订单状态 choices
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Status Log for Order #{self.order.order_number} - {self.status} at {self.timestamp}"