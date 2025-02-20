class ApiEndpoints {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; //  Django 后端 API 的 Base URL (开发环境)

  // 用户相关 API
  static const String userRegister = '$baseUrl/users/register/';
  static const String userLogin = '$baseUrl/users/login/';
  static const String userProfile = '$baseUrl/users/profile/';
  //  ... 其他用户 API

  // 商品相关 API
  static const String productList = '$baseUrl/products/list/';
  static const String productDetail = '$baseUrl/products/products/'; // 注意 URL 结构，Django REST Framework 默认的 ViewSet 会生成类似 /api/products/{id}/ 的 URL
  static const String categoryList = '$baseUrl/categories/';
  //  ... 其他商品 API
}