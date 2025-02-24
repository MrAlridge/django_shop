import 'package:flutter/material.dart';
import '../models/product_model.dart';
import '../services/api_service.dart';

class ProductProvider extends ChangeNotifier {
  List<Product> _productList = [];  // 商品列表
  bool _isLoading = false;          // 是否处于加载状态
  String? _errorMessage;            // 错误消息

  List<Product> get productList => _productList;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  final ApiService _apiService = ApiService();  // ApiService实例

  ProductProvider() {
    loadProducts();   // Provider创建时自动加载商品列表
  }

  Future<void> loadProducts() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();    // 通知监听器开始加载

    try {
      // * 调用API获取商品列表
      final productListData = await _apiService.getProductList();
      _productList = (productListData as List<dynamic>)   // ? 暂时先假设后端返回的是List
        .map((productJson) => Product.fromJson(productJson))
        .toList();
    } catch (error) {
      _errorMessage = 'Failed to load products. Please try again.';
      print('Error loading products: $error');
      // TODO 根据具体的错误类型，设置不同的错误信息
    } finally {
      _isLoading = false;
      notifyListeners();  // 通知监听器加载完成
    }
  }

  // TODO: 可以添加更多商品列表页相关的状态管理方法，例如：
  //  -  商品搜索
  //  -  商品分类筛选
  //  -  分页加载
}