import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/product_provider.dart'; // 导入 ProductProvider
import '../providers/cart_provider.dart'; // 导入 CartProvider (为了添加商品到购物车)
import '../models/product_model.dart';


class ProductListPage extends StatelessWidget {
  const ProductListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('商品列表')),
      body: Consumer<ProductProvider>(
        builder: (context, productProvider, child) {
          if (productProvider.isLoading) {
            return const Center(child: CircularProgressIndicator()); // 加载动画
          } else if (productProvider.errorMessage != null) {
            return Center(child: Text('Error: ${productProvider.errorMessage}')); // 错误信息
          } else if (productProvider.productList.isEmpty) {
            return const Center(child: Text('暂无商品')); // 空商品列表提示
          } else {
            return GridView.builder( // 使用 GridView 展示商品列表
              padding: const EdgeInsets.all(10.0),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2, // 每行显示 2 列
                childAspectRatio: 0.7, // 商品卡片宽高比
                crossAxisSpacing: 10.0,
                mainAxisSpacing: 10.0,
              ),
              itemCount: productProvider.productList.length,
              itemBuilder: (context, index) {
                final product = productProvider.productList[index];
                return ProductCard(product: product); // 使用 ProductCard Widget 展示商品信息
              },
            );
          }
        },
      ),
    );
  }
}

class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return Card(
      clipBehavior: Clip.antiAlias, // 裁剪超出 Card 边界的内容
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          AspectRatio( // 保证图片比例
            aspectRatio: 1.2,
            child: Image.network(
              product.images.isNotEmpty ? product.images[0].url : 'fallback_image_url', // 商品主图
              fit: BoxFit.cover, // 图片填充方式
              errorBuilder: (context, error, stackTrace) => const Center(child: Icon(Icons.error)), // 加载错误时显示错误图标
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  product.name,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                  maxLines: 2, // 最多显示 2 行商品名称
                  overflow: TextOverflow.ellipsis, // 超出部分显示省略号
                ),
                const SizedBox(height: 4.0),
                Text(
                  product.shortDescription,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: Colors.grey[600], fontSize: 12.0),
                ),
                const SizedBox(height: 8.0),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('￥${product.price.toStringAsFixed(2)}'), // 商品价格
                    Consumer<CartProvider>( // 使用 Consumer 获取 CartProvider
                      builder: (context, cartProvider, child) {
                        return ElevatedButton(
                          onPressed: () {
                            // 添加商品到购物车
                            cartProvider.addItemToCart(product.id, 1).catchError((error) {
                              // 捕获错误，例如库存不足等
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(cartProvider.errorMessage ?? 'Failed to add item to cart')), // 显示错误提示
                              );
                            });
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('已添加到购物车')), // 显示添加成功提示
                            );
                          },
                          child: const Text('加入购物车'),
                        );
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}