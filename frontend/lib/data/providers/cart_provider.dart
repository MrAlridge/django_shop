import 'package:flutter/material.dart';
import '../models/cart_model.dart';
import '../services/api_service.dart';

class CartProvider extends ChangeNotifier {
  Cart? _cart;  // 购物车数据
  
}