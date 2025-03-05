import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/product.dart';
// TODO 完善商品详情页面
import 'product_detail_page.dart';

class ProductListPage extends StatefulWidget {
  const ProductListPage({super.key});

  @override
  ProductListPageState createState() => ProductListPageState();
}

class ProductListPageState extends State<ProductListPage> {
  List<Product> _products = [];
  bool _isLoading = false;
  String _searchKeyword = '';       // 搜索关键词
  int? _selectedCategory;           // 选中的分类ID
  bool _isOnSaleFilter = false;     // 是否促销筛选
  String _ordering = '-created_at'; // 排序字段
  int _page = 1;                    // 当前页码
  int _pageSize = 10;               // 每页数量
  bool _hasMore = true;             // 是否还有更多数据

  // 商品分类列表,用于筛选
  List<ProductCategory> _categories = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadProductCategories();   // 加载商品分类列表
    _loadProducts();            // 加载商品列表
  }

  Future<void> _loadProductCategories() async {
    final categories = await ApiService.getProductCategoryList();
    if (categories != null) {
      setState(() {
        _categories = categories;
      });
    } else {
      setState(() {
        _errorMessage = '加载商品分类失败';
      });
    }
  }

  Future<void> _loadProducts({bool loadMore = false}) async {
    if (_isLoading || (!_hasMore && loadMore)) {
      // 如果正在加载或没有更多数据且是加载更多操作，直接返回
      return;
    }
    setState(() {
      _isLoading = true;
      if (loadMore) {
        _page++;    // 加载更多时页码+1
      } else {
        _page = 1;  // * 刷新或重新搜索/筛选/排序时重置页码为1
        _hasMore = true;
      }
    });

    final products = await ApiService.getProductList(
      search: _searchKeyword,
      categoryId: _selectedCategory,
      isOnSale: _isOnSaleFilter,
      ordering: _ordering,
      page: _page,
      pageSize: _pageSize,
    );

    setState(() {
      _isLoading = false;
      if (products != null) {
        if (loadMore) {
          _products.addAll(products);
          if (products.isEmpty || products.length < _pageSize) {
            _hasMore = false;
          }
        } else {
          _products = products;
          _hasMore = !(products.isEmpty || products.length < _pageSize);
        }
        _errorMessage = null;
      } else {
        _errorMessage = '加载商品列表失败';
      }
    });
  }

  void _onSearchChanged(String value) {
    setState(() {
      _searchKeyword = value;
      _loadProducts();
    });
  }

  void _onCategoryFilterChanged(int? categoryId) {
    setState(() {
      _selectedCategory = categoryId;
      _loadProducts();
    });
  }

  void _onSaleFilterChanged(bool isOnSale) {
    setState(() {
      _isOnSaleFilter = isOnSale;
      _loadProducts();
    });
  }

  void _onOrderingChanged(String? ordering) {
    setState(() {
      _ordering = ordering ?? '-created_at';
      _loadProducts();
    });
  }

  Widget _buildProductList() {
    if (_errorMessage != null) {
      return Center(child: Text(_errorMessage!));
    }
    if (_isLoading && _products.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_products.isEmpty) {
      return const Center(child: Text('没有找到商品'));
    }

    return ListView.builder(
      itemCount: _products.length + (_hasMore ? 1 : 0),
      itemBuilder: (context, index) {
        if (index < _products.length) {
          final product = _products[index];
          return ListTile(
            leading: product.image != null
              ? Image.network(ApiService.baseUrl + product.image!, width: 50, height: 50, fit: BoxFit.cover)
              : const Icon(Icons.image, size: 50),
            title: Text(product.name),
            subtitle: Text('\$${product.price.toStringAsFixed(2)}'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ProductDetailPage(productId: product.id)
                ),
              );
            },
          );
        } else if (_hasMore) {
          return _buildLoadMoreIndicator();
        }
        return null;
      },
    );
  }

  Widget _buildLoadMoreIndicator() {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Center(
        child: _isLoading ? const CircularProgressIndicator() : ElevatedButton(
          onPressed: _loadMoreProducts,
          child: const Text('加载更多'),
        ),
      ),
    );
  }

  Future<void> _loadMoreProducts() async {
    if (!_isLoading && _hasMore) {
      await _loadProducts(loadMore: true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('商品列表')),
      body: Column(
        children: [
          Padding(padding: const EdgeInsets.all(8.0),
          child: TextField(
            decoration: const InputDecoration(
              labelText: '搜索商品',
              prefixIcon: Icon(Icons.search),
            ),
            onChanged: _onSearchChanged,
          ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Row(
              children: [
                DropdownButton<int>(
                  value: _selectedCategory,
                  hint: const Text('全部分类'),
                  items: _categories.map((category) => DropdownMenuItem<int>(
                    value: category.id,
                    child: Text(category.name),
                  )).toList(),
                  onChanged: _onCategoryFilterChanged,
                ),
                const SizedBox(width: 16),
                Row(
                  children: [
                    Checkbox(
                      value: _isOnSaleFilter,
                      onChanged: (value) => _onSaleFilterChanged(value ?? false),
                    ),
                    const Text('促销商品')
                  ],
                ),
                const Spacer(),
                DropdownButton<String>(
                  value: _ordering,
                  items: const [
                    DropdownMenuItem(value: '-created_at', child: Text('默认排序')),
                    DropdownMenuItem(value: 'price', child: Text('价格升序')),
                    DropdownMenuItem(value: '-price', child: Text('价格降序')),
                  ],
                  onChanged: _onOrderingChanged,
                ),
              ],
            ),
          ),
          Expanded(
            child: _buildProductList(),
          ),
        ],
      ),
    );
  }
}