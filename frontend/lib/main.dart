import 'package:flutter/material.dart';
import 'pages/register_page.dart';
import 'pages/home_page.dart';
import 'pages/login_page.dart';
import 'pages/product_list_page.dart';
import 'pages/product_detail_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Demo',
      theme: ThemeData(
        primarySwatch: Colors.red,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        // colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginPage(),
        '/register': (context) => const RegisterPage(),
        '/home': (context) => const HomePage(),
        '/products': (context) => const ProductListPage(),
        '/product_detail': (context) => ProductDetailPage(productId: -1),
      },
      // home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

