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
    ORDER_STATUS_CHOICES = [    # 订单状态 choices
        ('pending_payment', '待支付'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
    ]
    PAYMENT_METHOD_CHOICES = [  # 支付方式 choices
        # TODO:后期还要接入其他支付方式，所以暂时先写这些
        ('theteller', 'theteller'),
        ('DPO', 'DPO'),
        ('expressPay', 'expressPay'),
        ('MTN_Mobile_Money', 'MTN_Mobile_Money'),
        ('cash_on_delivery', '货到付款'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending_payment', '待支付'),
        ('paid', '已支付'),
        ('payment_failed', '支付失败'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
    ]

    order_number = models.CharField(max_length=150, unique=True, default=uuid.uuid4) # 订单编号，使用 UUID 默认值
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders') #  关联 User 模型
    order_date = models.DateTimeField(auto_now_add=True) # 下单日期，自动添加
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # 订单总金额
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 运费，允许为空
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending_payment') # 订单状态，默认待支付
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='alipay') # 支付方式，默认支付宝
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending_payment') # 支付状态，默认待支付
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.CASCADE, related_name='orders') # 关联 ShippingAddress 模型
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.CASCADE, related_name='orders', blank=True, null=True) # 关联 BillingAddress 模型，允许为空
    note = models.TextField(blank=True) # 订单备注，允许为空
    # * 订单日期相关
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"
    
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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # 关联 Order 模型
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items') # 关联 Product 模型，注意 product 应用的模型需要使用 'product.Product' 引用
    quantity = models.IntegerField(default=1) # 购买数量，默认 1
    price = models.DecimalField(max_digits=10, decimal_places=2) # 商品单价
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False) # 订单项总价，不可编辑，自动计算

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        # ? 这里的总价并没有计算优惠，优惠是通过别的方式计算的
        self.total_price = self.quantity * self.price
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
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address_detail') #  一对一关联 Order 模型
    name = models.CharField(max_length=100) # 收货人姓名
    phone_number = models.CharField(max_length=20) # 收货人手机号
    province = models.CharField(max_length=100) # 省份
    city = models.CharField(max_length=100) # 城市
    district = models.CharField(max_length=100, blank=True) # 区/县，允许为空
    address_detail = models.CharField(max_length=255) # 详细地址
    postal_code = models.CharField(max_length=20, blank=True, null=True) # 邮政编码，允许为空

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping Address for Order #{self.order.order_number}"
    
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
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='billing_address_detail') #  一对一关联 Order 模型
    name = models.CharField(max_length=100) # 账单人姓名
    phone_number = models.CharField(max_length=20) # 账单人手机号
    province = models.CharField(max_length=100) # 省份
    city = models.CharField(max_length=100) # 城市
    district = models.CharField(max_length=100, blank=True) # 区/县，允许为空
    address_detail = models.CharField(max_length=255) # 详细地址
    postal_code = models.CharField(max_length=20, blank=True, null=True) # 邮政编码，允许为空

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Billing Addrress for Order #{self.order.order_number}"
    
class Payment(models.Model):
    """支付信息模型，存储订单的支付相关信息。

    :integer id: 支付 ID (自动生成)
    :Order order: 所属订单 (ForeignKey，关联到 Order 模型，一对一关系 OneToOneField)
    :string payment_id: 支付平台交易 ID (CharField, 例如支付宝交易号、微信支付订单号，用于查询支付状态)
    :DateTime payment_date: 支付时间 (DateTimeField, 记录支付成功时间)
    :Demical payment_amount: 支付金额 (DecimalField, 实际支付金额，可能与订单总金额有差异，例如使用了优惠券、积分等)
    :string payment_method: 支付方式 (CharField, 与 Order.payment_method 字段重复，可以冗余存储，方便查询)
    :string payment_status: 支付状态 (CharField, 与 Order.payment_status 字段重复，可以冗余存储，方便查询)
    :string raw_response: 支付平台原始响应数据 (TextField, 可选，存储支付平台返回的原始 JSON 或 XML 数据，用于排查问题)
    :DateTime created_at: 创建时间 (DateTimeField)
    :DateTime updated_at: 更新时间 (DateTimeField)
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_detail') #  一对一关联 Order 模型
    payment_id = models.CharField(max_length=200, blank=True) # 支付平台交易 ID，允许为空，例如货到付款可能没有交易ID
    payment_date = models.DateTimeField(blank=True, null=True) # 支付时间，允许为空
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # 支付金额
    payment_method = models.CharField(max_length=50, choices=Order.PAYMENT_METHOD_CHOICES, blank=True) # 支付方式，允许为空
    payment_status = models.CharField(max_length=50, choices=Order.PAYMENT_STATUS_CHOICES, default='pending_payment') # 支付状态，默认待支付
    raw_response = models.TextField(blank=True) # 支付平台原始响应数据，允许为空

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.order_number}"