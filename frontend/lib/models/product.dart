class ProductCategory {
  final int id;
  final String name;
  final String? description;

  ProductCategory({
    required this.id,
    required this.name,
    this.description,
  });

  factory ProductCategory.fromJson(Map<String, dynamic> json) {
    return ProductCategory(
      id: json['id'],
      name: json['name'],
      description: json['description'],
    );
  }
}

class Product {
  final int id;
  final ProductCategory category;
  final String name;
  final String? description;
  final double price;
  final String? image;  // 图片URL
  final int stock;
  final bool isOnSale;
  final List<Product>? relatedProducts; // 关联商品列表

  Product({
    required this.id,
    required this.category,
    required this.name,
    this.description,
    required this.price,
    this.image,
    required this.stock,
    required this.isOnSale,
    this.relatedProducts,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      category: ProductCategory.fromJson(json['category']),   // 解析category字段为ProductCategory
      name: json['name'],
      price: double.parse(json['price'].toString()),  // 确保price解析为double
      stock: json['stock'],
      isOnSale: json['is_on_sale'],
      // * 解析related_product列表
      relatedProducts: (json['related_products'] as List<dynamic>?)?.map((item) => Product.fromJson(item as Map<String, dynamic>)).toList(),
    );
  }
}