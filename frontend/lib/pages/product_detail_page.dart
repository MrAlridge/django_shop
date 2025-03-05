import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/product.dart';

class ProductDetailPage extends StatefulWidget {
  final int productId;

  const ProductDetailPage({super.key, required this.productId});

  @override
  ProductDetailPageState createState() => ProductDetailPageState();
}

class ProductDetailPageState extends State<ProductDetailPage> {
  Product? _product;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadProductDetail();
  }

  Future<void> _loadProductDetail() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final product = await ApiService.getProductDetail(productId: widget.productId);

    setState(() {
      _isLoading = false;
      if (product != null) {
        _product = product;
      } else {
        _errorMessage = '加载商品详情失败';
      }
    });
  }

  Widget _buildRelatedProducts() {
    if (_product == null || _product!.relatedProducts == null || _product!.relatedProducts!.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          child: Text('关联商品', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ),
        SizedBox(
          height: 150,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: _product!.relatedProducts!.length,
            itemBuilder: (context, index) {
              final relatedProduct = _product!.relatedProducts![index];
              return Container(
                width: 120,
                margin: const EdgeInsets.symmetric(horizontal: 8.0),
                child: InkWell(
                  onTap: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ProductDetailPage(productId: relatedProduct.id),
                      ),
                    );
                  },
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      AspectRatio(
                        aspectRatio: 1.0,
                        child: relatedProduct.image != null
                          ? Image.network(ApiService.baseUrl + relatedProduct.image!, fit: BoxFit.cover)
                          : const Icon(Icons.image, size: 80),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(
                          relatedProduct.name,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                      Text('\$${relatedProduct.price.toStringAsFixed(2)}'),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_errorMessage != null) {
      return Scaffold(
        appBar: AppBar(title: const Text('商品详情')),
        body: Center(child: Text(_errorMessage!)),
      );
    }

    if (_isLoading || _product == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('商品详情')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text(_product!.name)),
      body: SingleChildScrollView(    // 使用SingleChildScrollView，防止内容超出屏幕
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _product!.image != null
              ? Image.network(ApiService.baseUrl + _product!.image!, fit: BoxFit.cover)
              : const Icon(Icons.image, size: 200),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(_product!.name, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text('分类: ${_product!.category.name}'),
                  const SizedBox(height: 8),
                  Text('价格: \$${_product!.price.toStringAsFixed(2)}', style: const TextStyle(fontSize: 18, color: Colors.green)),
                  const SizedBox(height: 8),
                  Text('库存: ${_product!.stock}'),
                  const SizedBox(height: 16),
                  Text('描述: ${_product!.description ?? '暂无描述'}'),
                ],
              ),
            ),
            _buildRelatedProducts(),
          ],
        ),
      ),
    );
  }
}