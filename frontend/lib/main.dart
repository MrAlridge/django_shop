// main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'data/providers/cart_provider.dart';
import 'data/providers/product_provider.dart'; // 导入 ProductProvider
import 'config/routes.dart'; // 导入路由配置

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartProvider()),
        ChangeNotifierProvider(create: (_) => ProductProvider()), // 注册 ProductProvider
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Your App Name',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const ProductListPage(), //  将 MyHomePage 替换为 ProductListPage
    );
  }
}

class MyHomePage extends StatelessWidget { //  MyHomePage 可以删除，或者作为其他页面的模板
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Home Page')),
      body: const Center(child: Text('This is my home page')),
    );
  }
}