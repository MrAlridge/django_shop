import 'package:dio/dio.dart';
import '../models/product.dart'; // 假设 Product 模型定义在 product.dart 中
import '../../constants/api_endpoints.dart'; // 假设 API Endpoints 常量定义在 api_endpoints.dart 中

class ProductApiService {
  final Dio _dio = Dio(); // 创建 Dio 实例

  Future<List<Product>> getProductList() async {
    try {
      final response = await _dio.get(ApiEndpoints.productList); // 使用 API Endpoint 常量
      if (response.statusCode == 200) {
        List<dynamic> data = response.data;
        return data.map((item) => Product.fromJson(item)).toList(); // 将 JSON 数据转换为 Product 模型列表
      } else {
        throw Exception('Failed to load products'); // 处理错误
      }
    } catch (error) {
      print('Error fetching products: $error');
      throw error; // 抛出异常
    }
  }

  Future<Product> getProductDetail(int productId) async {
    try {
      final response = await _dio.get('${ApiEndpoints.productDetail}/$productId/'); // 使用 API Endpoint 常量，拼接商品 ID
      if (response.statusCode == 200) {
        return Product.fromJson(response.data); // 将 JSON 数据转换为 Product 模型
      } else {
        throw Exception('Failed to load product detail'); // 处理错误
      }
    } catch (error) {
      print('Error fetching product detail: $error');
      throw error; // 抛出异常
    }
  }
  //  ... 其他商品相关的 API 请求方法 (例如创建商品、更新商品 - 管理员功能)
}