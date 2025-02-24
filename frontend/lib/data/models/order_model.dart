import 'user_model.dart'; // 导入 UserProfile 模型
import 'product_model.dart'; // 导入 Product 模型

class Order {
  int id;
  String orderNumber;
  UserProfile user;
  DateTime orderDate;
  double orderTotal;
  double? shippingFee;
  String orderStatus;
  String paymentMethod;
  String paymentStatus;
  ShippingAddress shippingAddressDetail;
  BillingAddress? billingAddressDetail; // 账单地址可能为空
  String? note;
  DateTime createdAt;
  DateTime updatedAt;
  List<OrderItem> items;
  Payment? paymentDetail; // 支付信息可能为空

  Order({
    required this.id,
    required this.orderNumber,
    required this.user,
    required this.orderDate,
    required this.orderTotal,
    this.shippingFee,
    required this.orderStatus,
    required this.paymentMethod,
    required this.paymentStatus,
    required this.shippingAddressDetail,
    this.billingAddressDetail,
    this.note,
    required this.createdAt,
    required this.updatedAt,
    required this.items,
    this.paymentDetail,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      orderNumber: json['order_number'],
      user: UserProfile.fromJson(json['user']), // 解析 UserProfile
      orderDate: DateTime.parse(json['order_date']),
      orderTotal: (json['order_total'] as num).toDouble(),
      shippingFee: (json['shipping_fee'] as num?)?.toDouble(),
      orderStatus: json['order_status'],
      paymentMethod: json['payment_method'],
      paymentStatus: json['payment_status'],
      shippingAddressDetail: ShippingAddress.fromJson(json['shipping_address_detail']), // 解析 ShippingAddress
      billingAddressDetail: json['billing_address_detail'] != null ? BillingAddress.fromJson(json['billing_address_detail']) : null, // 解析 BillingAddress，可能为空
      note: json['note'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      items: (json['items'] as List<dynamic>?)?.map((itemJson) => OrderItem.fromJson(itemJson)).toList() ?? [], // 解析 OrderItem 列表
      paymentDetail: json['payment_detail'] != null ? Payment.fromJson(json['payment_detail']) : null, // 解析 Payment，可能为空
    );
  }
}

class OrderItem {
  int id;
  Product product; // 嵌套 Product 模型
  int quantity;
  double price;
  double totalPrice;

  OrderItem({
    required this.id,
    required this.product,
    required this.quantity,
    required this.price,
    required this.totalPrice,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'],
      product: Product.fromJson(json['product']), // 解析 Product
      quantity: json['quantity'],
      price: (json['price'] as num).toDouble(),
      totalPrice: (json['total_price'] as num).toDouble(),
    );
  }
}

class ShippingAddress {
  int id;
  String name;
  String phoneNumber;
  String province;
  String city;
  String? district; // 区/县可能为空
  String addressDetail;
  String? postalCode; // 邮政编码可能为空

  ShippingAddress({
    required this.id,
    required this.name,
    required this.phoneNumber,
    required this.province,
    required this.city,
    this.district,
    required this.addressDetail,
    this.postalCode,
  });

  factory ShippingAddress.fromJson(Map<String, dynamic> json) {
    return ShippingAddress(
      id: json['id'],
      name: json['name'],
      phoneNumber: json['phone_number'],
      province: json['province'],
      city: json['city'],
      district: json['district'],
      addressDetail: json['address_detail'],
      postalCode: json['postal_code'],
    );
  }
}

class BillingAddress {
  // 模型结构与 ShippingAddress 类似，可以根据实际需求调整
  int id;
  String name;
  String phoneNumber;
  String province;
  String city;
  String? district;
  String addressDetail;
  String? postalCode;

  BillingAddress({
    required this.id,
    required this.name,
    required this.phoneNumber,
    required this.province,
    required this.city,
    this.district,
    required this.addressDetail,
    this.postalCode,
  });

  factory BillingAddress.fromJson(Map<String, dynamic> json) {
    return BillingAddress(
      id: json['id'],
      name: json['name'],
      phoneNumber: json['phone_number'],
      province: json['province'],
      city: json['city'],
      district: json['district'],
      addressDetail: json['address_detail'],
      postalCode: json['postal_code'],
    );
  }
}


class Payment {
  int id;
  String? paymentId; // 支付平台交易 ID 可能为空
  DateTime? paymentDate; // 支付时间可能为空
  double paymentAmount;
  String? paymentMethod; // 支付方式可能为空
  String paymentStatus;
  String? rawResponse; // 原始响应数据可能为空

  Payment({
    required this.id,
    this.paymentId,
    this.paymentDate,
    required this.paymentAmount,
    this.paymentMethod,
    required this.paymentStatus,
    this.rawResponse,
  });

  factory Payment.fromJson(Map<String, dynamic> json) {
    return Payment(
      id: json['id'],
      paymentId: json['payment_id'],
      paymentDate: json['payment_date'] != null ? DateTime.parse(json['payment_date']) : null, // 支付时间可能为 null
      paymentAmount: (json['payment_amount'] as num).toDouble(),
      paymentMethod: json['payment_method'],
      paymentStatus: json['payment_status'],
      rawResponse: json['raw_response'],
    );
  }
}