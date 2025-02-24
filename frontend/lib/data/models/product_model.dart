
class Product {
  int id;
  String name;
  String shortDescription;
  String description;
  double price;
  double? discountPrice;  // 折扣价可能为空
  int stockQuantity;
  bool isActive;
  Category? category;     // 商品分类
  List<ProductImage> images;
  DateTime createdAt;
  DateTime updatedAt;

  Product({
    required this.id,
    required this.name,
    required this.shortDescription,
    required this.description,
    required this.price,
    this.discountPrice,
    required this.stockQuantity,
    required this.isActive,
    this.category,
    required this.images,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      shortDescription: json['shortDescription'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),   // ! 确保price转换为double
      discountPrice: (json['discount_price'] as num?)?.toDouble(),  // 折扣价可能为Null
      stockQuantity: json['stockQuantity'],
      isActive: json['isActive'],
      // * 解析图片列表，可能为空
      images: (json['images'] as List<dynamic>?)?.map((imageJson) => ProductImage.fromJson(imageJson)).toList() ?? [],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }
}

class Category {
  int id;
  String name;

  Category({required this.id, required this.name});

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      name: json['name']
    );
  }
}

class ProductImage {
  int id;
  String url;
  bool isMain;

  ProductImage({required this.id, required this.url, required this.isMain});

  factory ProductImage.fromJson(Map<String, dynamic> json) {
    return ProductImage(
      id: json['id'],
      url: json['url'],
      isMain: json['isMain'],
    );
  }
}

