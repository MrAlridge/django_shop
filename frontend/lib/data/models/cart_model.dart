import 'product_model.dart';

class Cart {
  int id;
  int user;
  DateTime createdAt;
  DateTime updatedAt;
  List<CartItem> items;
  int totalItems;
  double totalPrice;

  Cart({
    required this.id,
    required this.user,
    required this.createdAt,
    required this.updatedAt,
    required this.items,
    required this.totalItems,
    required this.totalPrice,
  });

  factory Cart.fromJson(Map<String, dynamic> json) {
    return Cart(
      id: json['id'],
      user: json['user'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
      items: (json['items'] as List<dynamic>?)?.map((itemJson) => CartItem.fromJson(itemJson)).toList() ?? [],
      totalItems: json['totalItems'] ?? 0,
      totalPrice: (json['totalPrice'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

class CartItem {
  int id;
  Product product;  // 嵌套Product模型
  int quantity;
  double totalPrice;

  CartItem({
    required this.id,
    required this.product,
    required this.quantity,
    required this.totalPrice,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'],
      product: Product.fromJson(json['product']), // * 解析嵌套的Product数据
      quantity: json['quantity'],
      totalPrice: (json['totalPrice'] as num?)?.toDouble() ?? 0.0,
    );
  }
}