import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/cart_model.dart';
import '../models/product_model.dart';

class ApiService {
  // ! 后端api base URL
  final String baseUrl = 'http://<backendapi>';

  Future<List<dynamic>> getProductList() async {  // 返回 List<dynamic>,在Provider中转换为List<Product>
    // * 调用 GET /api/products 接口
    final response = await http.get(Uri.parse('$baseUrl/api/products/'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);   // 后端正常情况下应返回JSON数组
    } else {
      throw Exception('Failed to load products');
    }
  }

}