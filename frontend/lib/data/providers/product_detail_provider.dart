import 'package:flutter/material.dart';
import '../models/product_model.dart';
import '../services/api_service.dart';

class ProductDetailProvider extends ChangeNotifier {
  Product? _productDetail;  // 商品详情数据
  bool _isLoading = false;  // 加载状态
  String? _errorMessage;    // 错误信息

  Product? get productDetail => _productDetail;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  // * ApiService实例
  final ApiService _apiService = ApiService();

  Future<void> loadProductDetail(int productId) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();  // 通知监听器开始加载

    try {
      final productData = await _apiService.getProductDetail(productId);
      _productDetail = Product.fromJson(productData);
    } catch (error) {
      _errorMessage = 'Failed to load product detail. Please try again.';
      print('Error loading product detail: $error');
      // TODO 可以根据具体的错误类型，设置不同的错误信息
    } finally {
      _isLoading = false;
      notifyListeners();  // 通知监听器加载完成
    }
  }

  // TODO 添加更多商品详情页相关的状态管理方法：加入购物车，收藏商品
}