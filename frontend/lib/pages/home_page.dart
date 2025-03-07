import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('主页')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('欢迎来到生活超市APP'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // 跳转到商品列表页
                Navigator.pushNamed(context, '/products');
              },
              child: const Text('查看商品列表')
            ),
          ],
        ),
      ),
    );
  }
}