
class Order {
  final int orderId;
  final String orderNumber;
  final DateTime orderDate;
  final String orderStatus;
  final double finalTotal;
  final String paymentMethod;

  // ... 其他字段 ...

  Order({
    required this.orderId,
    required this.orderNumber,
    required this.orderDate,
    required this.orderStatus,
    required this.finalTotal,
    required this.paymentMethod,
    // ... 其他字段的初始化 ...
  });

  //  *  工厂方法，用于从 JSON 数据中创建 Order 对象 (反序列化)
  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      orderId: json['order_id'],
      orderNumber: json['order_number'],
      orderDate: DateTime.parse(json['order_date']), //  假设 order_date 是 ISO 8601 格式的字符串
      orderStatus: json['order_status'],
      finalTotal: (json['final_total'] as num).toDouble(), //  确保转换为 double
      paymentMethod: json['payment_method'],
      // ... 其他字段的 JSON 解析 ...
    );
  }

  //  *  方法，用于将 Order 对象转换为 JSON 数据 (序列化，如果需要)
  Map<String, dynamic> toJson() {
    return {
      'order_id': orderId,
      'order_number': orderNumber,
      'order_date': orderDate.toIso8601String(), //  转换为 ISO 8601 格式的字符串
      'order_status': orderStatus,
      'final_total': finalTotal,
      'payment_method': paymentMethod,
      // ... 其他字段的 JSON 转换 ...
    };
  }
}
