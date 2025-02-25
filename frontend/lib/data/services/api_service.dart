import 'dart:convert';
import 'package:http/http.dart' as http;
// * 使用Token认证的话这个库就要用到
import 'package:shared_preferences/shared_preferences.dart';
import '../models/cart_model.dart';
import '../models/product_model.dart';
import '../models/order_model.dart';
import '../models/user_model.dart';

class ApiService {

  // ! 后端api base URL, 开发阶段暂时先用这个
  // TODO 等大部分功能都开发完毕要把baseURL搞到.env里面
  static const String BASE_URL = 'http://127.0.0.1:8000';
  // * 默认请求头
  static const Map<String, String> DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
  }

  // --- Token相关 ---
  static const String AUTH_TOKEN_KEY = 'auth_token';

  /**获取认证TOKEN
   * 
   * 返回Token字符串
   */
  Future<String?> getAuthToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(AUTH_TOKEN_KEY);
  }

  ///设置token key
  ///
  ///参数：
  ///- String [token]：要设置的key
  ///
  Future<void> setAuthToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(AUTH_TOKEN_KEY, token);
  }

  /**
   * 清除设置的Token
   */
  Future<void> clearAuthToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AUTH_TOKEN_KEY);
  }

  // --- 商品相关API ---
  
  /// 发送请求来获取商品列表
  /// - `page`: 页码
  /// - `pagesize`: 每页商品数量
  /// - `keyword`: 搜索关键词
  /// - `categoryId`: 商品分类id
  Future<List<dynamic>> getProductList({int page = 1, int pageSize = 10, String? keyword, int? categoryId}) async {
    Uri uri = Uri.parse('$BASE_URL/api/products');
    // * 添加分页参数
    uri = uri.replace(queryParameters: {
      'page': page.toString(),
      'page_size': pageSize.toString(),
      if (keyword != null && keyword.isNotEmpty) 'search': keyword, // 搜索关键词
      if (categoryId != null) 'category': categoryId.toString(),  // 分类ID
    });

    // 发送请求
    final response = await http.get(uri);
    // 使用统一的错误处理
    return _handleResponse(response, 'Failed to load products');
  }

  /// 根据产品ID获取产品的详细信息。
  ///
  /// 参数:
  /// * `productId`: 产品的唯一标识符，用于指定要查询的产品。
  ///
  /// 返回:
  ///   一个`Future<Map<String, dynamic>>`，包含请求的产品详细信息。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final productDetail = await getProductDetail(123);
  /// print(productDetail);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_handleResponse`函数处理HTTP响应，该函数会检查响应状态码并解析响应体。
  Future<Map<String, dynamic>> getProductDetail(int productId) async {
    final response = await http.get(Uri.parse('$BASE_URL/api/products/$productId/'));
    return _handleResponse(response, 'Failed to load product detail');
  }

  /// 获取所有产品分类的信息。
  ///
  /// 参数:
  /// 无
  ///
  /// 返回:
  ///   一个`Future<List<dynamic>>`，包含所有产品分类的信息。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据列表；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final productCategories = await getProductCategories();
  /// print(productCategories);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_handleResponse`函数处理HTTP响应，该函数会检查响应状态码并解析响应体。
  Future<List<dynamic>> getProductCategories() async {
    final response = await http.get(Uri.parse('$BASE_URL/api/categories/'));
    return _handleResponse(response, 'Failed to load product categories');
  }

  /// 根据关键词搜索产品，并支持分页查询。
  ///
  /// 参数:
  /// * `keyword`: 搜索关键词，用于匹配产品的名称或其他相关信息。
  /// * `page`: （可选）当前请求的页码，默认值为1。用于分页查询。
  /// * `pageSize`: （可选）每页返回的产品数量，默认值为10。用于分页查询。
  ///
  /// 返回:
  ///   一个`Future<List<dynamic>>`，包含与关键词匹配的产品列表。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据列表；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final products = await searchProducts('apple', page: 1, pageSize: 10);
  /// print(products);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_handleResponse`函数处理HTTP响应，该函数会检查响应状态码并解析响应体。
  /// - `queryParameters`被用来构建URL查询字符串，包括`keyword`, `page`, 和 `page_size`。
  Future<List<dynamic>> searchProducts(String keyword, {int page = 1, int pageSize = 10}) async {
    Uri uri = Uri.parse('$BASE_URL/api/products/search/');
    uri = uri.replace(queryParameters: {
      'keyword': keyword,
      'page': page.toString(),
      'page_size': pageSize.toString(),
    });
    final response = await http.get(uri);
    return _handleResponse(response, 'Failed to search products');
  }

  /// 根据分类ID过滤产品，并支持分页查询。
  ///
  /// 参数:
  /// * `categoryId`: 分类的唯一标识符，用于指定要查询的产品分类。
  /// * `page`: （可选）当前请求的页码，默认值为1。用于分页查询。
  /// * `pageSize`: （可选）每页返回的产品数量，默认值为10。用于分页查询。
  ///
  /// 返回:
  ///   一个`Future<List<dynamic>>`，包含与分类ID匹配的产品列表。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据列表；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final products = await filterProductsByCategory(1, page: 1, pageSize: 10);
  /// print(products);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_handleResponse`函数处理HTTP响应，该函数会检查响应状态码并解析响应体。
  /// - `queryParameters`被用来构建URL查询字符串，包括`page`和`page_size`。
  Future<List<dynamic>> filterProductsByCategory(int categoryId, {int page = 1, int pageSize = 10}) async {
    Uri uri = Uri.parse('$BASE_URL/api/categories/$categoryId/products/');
    uri = uri.replace(queryParameters: {
      'page': page.toString(),
      'page_size': pageSize.toString(),
    });
    final response = await http.get(uri);
    return _handleResponse(response, 'Failed to filter products by categories');
  }

  // --- 购物车相关API ---

  /// 获取当前用户的购物车信息。
  ///
  /// 参数:
  /// 无
  ///
  /// 返回:
  ///   一个`Future<Map<String, dynamic>>`，包含当前用户的购物车信息。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final cart = await getCart();
  /// print(cart);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_getAuthHeaders`函数获取包含认证信息的HTTP请求头，确保请求具有适当的权限。
  /// - 使用`_handleResponse`函数处理HTTP响应，该函数会检查响应状态码并解析响应体。
  Future<Map<String, dynamic>> getCart() async {
    final response = await http.get(
      Uri.parse('$BASE_URL/api/cart/'),
      headers: await _getAuthHeaders()
    );
    return _handleResponse(response, 'Failed to load cart');
  }

  /// 向购物车中添加商品。
  ///
  /// 参数:
  /// * `productId`: 商品的唯一标识符，用于指定要添加的商品。
  /// * `quantity`: 要添加的商品数量。
  ///
  /// 返回:
  ///   一个`Future<Map<String, dynamic>>`，包含更新后的购物车信息。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final updatedCart = await addItemToCart(123, 2);
  /// print(updatedCart);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_getAuthHeaders`函数获取包含认证信息的HTTP请求头，确保请求具有适当的权限。
  /// - 使用`jsonEncode`将请求体编码为JSON格式。
  Future<Map<String, dynamic>> addItemToCart(int productId, int quantity) async {
    final response = await http.post(
      Uri.parse('$BASE_URL/api/cart/items/'),
      headers: await _getAuthHeaders(DEFAULT_HEADERS), //  添加认证和默认请求头
      body: jsonEncode({'product_id': productId, 'quantity': quantity}),
    );
    return _handleResponse(response, 'Failed to add item to cart');
  }

  /// 更新购物车中某个商品的数量。
  ///
  /// 参数:
  /// * `itemId`: 购物车项的唯一标识符，用于指定要更新的商品。
  /// * `quantity`: 要更新的商品数量。
  ///
  /// 返回:
  ///   一个`Future<Map<String, dynamic>>`，包含更新后的购物车信息。如果请求成功（状态码在200到300之间），则返回解析后的JSON数据；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// final updatedCart = await updateCartItemQuantity(456, 3);
  /// print(updatedCart);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_getAuthHeaders`函数获取包含认证信息的HTTP请求头，确保请求具有适当的权限。
  /// - 使用`jsonEncode`将请求体编码为JSON格式。
  Future<Map<String, dynamic>> updateCartItemQuantity(int itemId, int quantity) async {
    final response = await http.patch(
      Uri.parse('$BASE_URL/api/cart/items/$itemId/'),
      headers: await _getAuthHeaders(DEFAULT_HEADERS),
      body: jsonEncode({'quantity': quantity}),
    );
    return _handleResponse(response, 'Failed to update cart item quantity');
  }

  /// 从购物车中移除某个商品。
  ///
  /// 参数:
  /// * `itemId`: 购物车项的唯一标识符，用于指定要移除的商品。
  ///
  /// 返回:
  ///   无返回值（`Future<void>`），如果请求成功（状态码在200到300之间），则完成此Future；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// await removeCartItem(789);
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_getAuthHeaders`函数获取包含认证信息的HTTP请求头，确保请求具有适当的权限。
  /// - 使用`_handleVoidResponse`函数处理没有返回内容的HTTP响应。
  Future<void> removeCartItem(int itemId) async {
    final response = await http.delete(
      Uri.parse('$BASE_URL/api/cart/items/$itemId/'),
      headers: await _getAuthHeaders()
    );
    _handleVoidResponse(response, 'Failed to remove item from cart'); //  处理 void 响应
  }

  /// 清空购物车。
  ///
  /// 参数:
  /// 无
  ///
  /// 返回:
  ///   无返回值（`Future<void>`），如果请求成功（状态码在200到300之间），则完成此Future；否则抛出异常。
  ///
  /// 异常:
  ///   `Exception`: 如果HTTP请求失败（状态码不在200到300之间），则抛出异常，异常信息包括自定义的错误消息和状态码。
  ///
  /// 示例:
  /// ```dart
  /// await clearCart();
  /// ```
  ///
  /// 注意:
  /// - 确保`BASE_URL`已正确定义并指向有效的API端点。
  /// - 使用`_getAuthHeaders`函数获取包含认证信息的HTTP请求头，确保请求具有适当的权限。
  /// - 使用`_handleVoidResponse`函数处理没有返回内容的HTTP响应。
  Future<void> clearCart() async {
    final response = await http.delete(
      Uri.parse('$BASE_URL/api/cart/clear/'),
      headers: await _getAuthHeaders()
    );
    _handleVoidResponse(response, 'Failed to clear cart'); //  处理 void 响应
  }

  // --- 订单相关API ---

  Future<Map<String, dynamic>> createOrder(Map<String, dynamic> orderData) async {
    final response = await http.post(
      Uri.parse('$BASE_URL/api/orders/'),
      headers: await _getAuthHeaders(DEFAULT_HEADERS),
      body: jsonEncode(orderData),
    );
    return _handleResponse(response, 'Failed to create order');
  }

  // TODO 添加其他订单相关API方法

  // --- 用户相关API ---


  Future<Map<String, dynamic>> getUserProfile() async {
    final response = await http.get(
      Uri.parse('$BASE_URL/api/usermgmt/profile'),
      headers: await _getAuthHeaders()
    );
    return _handleResponse(response, 'Failed to load user profile');
  }

  // TODO 添加其他用户相关API方法

  // --- 统一的响应处理 ---

  /// 处理HTTP响应，并在成功时返回解析后的JSON数据，失败时抛出异常。
  ///
  /// 参数:
  /// * [response]: HTTP响应对象，包含请求的状态码和响应体。
  /// * [errorMessage]: 当响应状态码不在200-300范围内时，用于描述错误信息的字符串。
  ///
  /// 返回:
  ///   一个`Future<Map<String, dynamic>>`，如果响应成功（状态码在200到300之间），则返回解析后的JSON数据。
  ///
  /// 抛出:
  ///   `Exception`: 如果响应的状态码不在200-300范围内，则抛出异常，异常信息包括自定义的错误消息和状态码。
  // ! Gemini生成的函数类型有点问题，Map<String, dynamic>跟其他类型对不上
  Future<List<dynamic>> _handleResponse(http.Response response, String errorMessage) async {
    // * 成功状态码的范围
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      // 打印详细错误日志
      print('API Error: ${response.statusCode}, Response: ${response.body}');
      // 抛出包含状态码的异常
      throw Exception('$errorMessage. Status Code: ${response.statusCode}');
    }
  }

  /// 处理HTTP响应，针对不需要返回数据的成功响应（如204 No Content），并在失败时抛出异常。
  ///
  /// 参数:
  /// * `response`: HTTP响应对象，包含请求的状态码和响应体。
  /// * `errorMessage`: 当响应状态码不在200-300范围内且不为204时，用于描述错误信息的字符串。
  ///
  /// 返回:
  ///   一个`Future<void>`，如果响应成功（状态码在200到300之间或为204 No Content），则完成此Future而不返回任何值。
  ///
  /// 抛出:
  ///   `Exception`: 如果响应的状态码不在200-300范围内且不为204，则抛出异常，异常信息包括自定义的错误消息和状态码。
  Future<void> _handleVoidResponse(http.Response response, String errorMessage) async {
    // 判断成功状态码的范围，204 No Content 也表示成功
    if (!(response.statusCode >= 200 && response.statusCode < 300) && response.statusCode != 204) {
      // 打印详细错误日志
      print('API Error: ${response.statusCode}, Response: ${response.body}');
      // 抛出包含状态码的异常
      throw Exception('$errorMessage. Status Code: ${response.statusCode}');
    }
  }

  // --- 认证请求头处理 ---

  /// 获取包含认证信息的HTTP请求头。
  ///
  /// 参数:
  /// * `customHeaders`: （可选）一个包含自定义HTTP请求头的Map。如果未提供，则使用默认请求头。
  ///
  /// 返回:
  ///   一个`Future<Map<String, String>>`，包含带有认证信息的HTTP请求头。如果存在有效的token，会在请求头中添加`Authorization: Bearer <token>`。
  ///
  /// 示例:
  /// ```dart
  /// final headers = await _getAuthHeaders({'Custom-Header': 'Value'});
  /// print(headers);
  /// ```
  ///
  /// 注意:
  /// - 如果提供了`customHeaders`，则这些头部将会被用作基础；否则，将使用一个空的Map作为基础。
  /// - 如果获取到的token不为空，则会在返回的headers中添加`Authorization`头部。
  Future<Map<String, String>> _getAuthHeaders([Map<String, String>? customHeaders]) async {
    final token = await getAuthToken();
    // * 使用自定义 headers 或默认 headers
    Map<String, String> headers = customHeaders ?? {};
    if (token != null) {
      // 添加Token到Authorization请求头
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }

}