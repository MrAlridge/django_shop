from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress, BillingAddress, OrderStatusLog
from product.models import Product
from product.serializers import ProductSerializer # 假设 product 应用有 ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品项 Serializer (用于订单创建)"""
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product') #  接收 product_id, 关联 Product 模型

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity'] #  只需要 product_id 和 quantity 字段

    def validate_quantity(self, value):
        """验证商品数量"""
        if value <= 0:
            raise serializers.ValidationError("商品数量必须大于0")
        return value


class ShippingAddressSerializer(serializers.ModelSerializer):
    """配送地址 Serializer (可用于订单创建和地址管理)"""
    class Meta:
        model = ShippingAddress
        fields = ['shipping_address_id', 'full_name', 'phone_number', 'address_line1', 'address_line2', 'city', 'state_province', 'postal_code', 'country', 'is_default']
        read_only_fields = ['shipping_address_id', 'user'] # shipping_address_id 自动生成，user 在 view 中设置


class BillingAddressSerializer(serializers.ModelSerializer):
    """账单地址 Serializer (可用于订单创建和地址管理,  初期和 ShippingAddressSerializer 字段相同)"""
    class Meta:
        model = BillingAddress
        fields = ['billing_address_id', 'full_name', 'phone_number', 'address_line1', 'address_line2', 'city', 'state_province', 'postal_code', 'country']
        read_only_fields = ['billing_address_id', 'user'] # billing_address_id 自动生成，user 在 view 中设置


class OrderCreateSerializer(serializers.ModelSerializer):
    """订单创建 Serializer"""
    items = OrderItemSerializer(many=True, write_only=True) #  嵌套 OrderItemSerializer，接收商品项列表
    shipping_address = ShippingAddressSerializer(write_only=True) # 嵌套配送地址 Serializer
    billing_address = BillingAddressSerializer(write_only=True) # 嵌套账单地址 Serializer
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES) # 支付方式选择

    class Meta:
        model = Order
        fields = ['items', 'shipping_address', 'billing_address', 'payment_method', 'customer_notes']

    def validate_items(self, value):
        """验证订单商品项列表"""
        if not value or len(value) == 0:
            raise serializers.ValidationError("订单商品不能为空")
        return value

    def validate(self, data):
        """ 额外的字段验证，例如库存检查，地址有效性等 """
        items_data = data.get('items')
        if items_data:
            for item_data in items_data:
                product = item_data['product'] #  OrderItemSerializer 中已经关联了 Product 模型
                quantity = item_data['quantity']
                if product.stock_quantity < quantity:
                    raise serializers.ValidationError(f"商品 {product.name} 库存不足，仅剩 {product.stock_quantity} 件")
        return data

    def create(self, validated_data):
        """创建订单，包括订单项、地址等"""
        items_data = validated_data.pop('items') #  pop 出 items 数据
        shipping_address_data = validated_data.pop('shipping_address') # pop 出配送地址数据
        billing_address_data = validated_data.pop('billing_address') # pop 出账单地址数据

        # 创建配送地址和账单地址
        shipping_address = ShippingAddress.objects.create(user=self.context['request'].user, **shipping_address_data) #  user 从 context 中获取
        billing_address = BillingAddress.objects.create(user=self.context['request'].user, **billing_address_data) # user 从 context 中获取

        # 创建订单
        order = Order.objects.create(
            user=self.context['request'].user, # user 从 context 中获取
            shipping_address=shipping_address,
            billing_address=billing_address,
            **validated_data # validated_data 包含 payment_method, customer_notes 等订单基本信息
        )

        order_total = 0 #  初始化订单总金额
        # 创建订单商品项
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price, # *  注意使用商品下单时的价格
            )
            order_total += product.price * quantity #  累加订单总金额

        order.order_total = order_total #  设置订单总金额
        order.final_total = order_total + order.shipping_fee - order.discount_amount # 计算最终支付金额 (这里运费和优惠金额暂时为 0, 后续需要完善)
        order.save() #  保存订单

        return order


class OrderListSerializer(serializers.ModelSerializer):
    """订单列表 Serializer (用于订单列表 API)"""
    class Meta:
        model = Order
        fields = ['order_id', 'order_number', 'order_date', 'order_status', 'final_total', 'payment_method'] #  列表页展示的字段


class ProductSimpleSerializer(serializers.ModelSerializer): #  *  商品简略信息 Serializer，用于订单详情展示商品信息
    """商品简略信息 Serializer，用于订单详情展示商品信息，避免循环嵌套"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images'] #  *  包含 images 字段


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """订单商品项 Serializer (用于订单详情)"""
    product = ProductSimpleSerializer(read_only=True) #  嵌套 ProductSimpleSerializer，展示商品简略信息

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'product', 'quantity', 'price', 'item_total']


class OrderStatusLogSerializer(serializers.ModelSerializer):
    """订单状态日志 Serializer (用于订单详情)"""
    class Meta:
        model = OrderStatusLog
        fields = ['status_log_id', 'status', 'timestamp', 'notes']


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情 Serializer"""
    items = OrderItemDetailSerializer(many=True, read_only=True) #  嵌套 OrderItemDetailSerializer 列表
    shipping_address = ShippingAddressSerializer(read_only=True) # 嵌套配送地址 Serializer
    billing_address = BillingAddressSerializer(read_only=True) # 嵌套账单地址 Serializer
    status_logs = OrderStatusLogSerializer(many=True, read_only=True) # 嵌套订单状态日志 Serializer
    payment_method = serializers.CharField(source='get_payment_method_display', read_only=True) #  显示 choices 的 human-readable 值
    order_status = serializers.CharField(source='get_order_status_display', read_only=True) # 显示 choices 的 human-readable 值

    class Meta:
        model = Order
        fields = ['order_id', 'order_number', 'order_date', 'order_status', 'payment_method', 'transaction_id', 'order_total', 'shipping_fee', 'discount_amount', 'final_total', 'customer_notes', 'items', 'shipping_address', 'billing_address', 'status_logs', 'created_at', 'updated_at']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """订单状态更新 Serializer"""
    order_status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES) #  只允许更新为 choices 中的状态

    class Meta:
        model = Order
        fields = ['order_status', 'notes']