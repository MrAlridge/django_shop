import 'package:flutter/material.dart';
import '../modules/product/screens/product_list_screen.dart';
import '../modules/product/screens/product_detail_screen.dart';
import '../modules/user/screens/login_screen.dart';
import '../modules/user/screens/register_screen.dart';
import '../modules/user/screens/profile_screen.dart';
// ... 其他页面

class AppRoutes {
  static const String productList = '/products';
  static const String productDetail = '/product_detail';
  static const String login = '/login';
  static const String register = '/register';
  static const String profile = '/profile';
  // ... 其他路由

  static Map<String, WidgetBuilder> routes = {
    productList: (context) => ProductListScreen(),
    productDetail: (context) => ProductDetailScreen(),
    login: (context) => LoginScreen(),
    register: (context) => RegisterScreen(),
    profile: (context) => ProfileScreen(),
    // ... 其他路由页面
  };

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case productList:
        return MaterialPageRoute(builder: (_) => ProductListScreen());
      case productDetail:
        //  可以传递参数到商品详情页
        final productId = settings.arguments as int;
        return MaterialPageRoute(builder: (_) => ProductDetailScreen(productId: productId));
      case login:
        return MaterialPageRoute(builder: (_) => LoginScreen());
      case register:
        return MaterialPageRoute(builder: (_) => RegisterScreen());
      case profile:
        return MaterialPageRoute(builder: (_) => ProfileScreen());
      default:
        return MaterialPageRoute(
            builder: (_) => Scaffold(
                  body: Center(
                    child: Text('No route defined for ${settings.name}'),
                  ),
                ));
    }
  }
}