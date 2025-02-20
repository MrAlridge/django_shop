import 'package:flutter/material.dart';
import 'config/routes.dart'; // 导入路由配置

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Supermarket App',
      theme: AppTheme.lightTheme, //  使用定义好的主题
      // routes: AppRoutes.routes, //  使用命名路由表 (简单路由)
      onGenerateRoute: AppRoutes.generateRoute, //  使用 onGenerateRoute (更灵活，可以传递参数)
      initialRoute: AppRoutes.productList, //  初始路由
    );
  }
}