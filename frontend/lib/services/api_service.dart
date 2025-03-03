import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  // 注册API
  static Future<User?> registerUser({
    required String username,
    required String password,
    required String password2,
    required String email,
    String? firstName,
    String? lastName,
    String? address,
    String? phoneNumber,
  }) async {
    final Uri uri = Uri.parse('$baseUrl/register/');
    final Map<String, dynamic> requestBody = {
      'username': username,
      'password': password,
      'password2': password2,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'address': address,
      'phone_number': phoneNumber,
    };

    try {
      final response = await http.post(
        uri,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 201) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        return User.fromJson(responseData['user']);   // 返回User对象
      } else {
        print('注册失败: ${response.statusCode}');
        print('Response body: ${response.body}');
        return null;  // 注册失败返回null
      }
    } catch(e) {
      print('注册请求发生异常: $e');
      return null;  // 发生异常就返回null
    }
  }

  // 登录API
  static Future<User?> loginUser({
    required String username,   // ! 暂时只使用User登录，等合适再单独做邮箱登录
    required String password,
  }) async {
    final Uri uri = Uri.parse('$baseUrl/login/');
    final Map<String, dynamic> requestBody = {
      'username': username,
      'password': password,
    };

    try {
      final response = await http.post(
        uri,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        return User.fromJson(responseData['user']);
      } else {
        print('登录失败: ${response.statusCode}');
        print('Response body: ${response.body}');
        return null;
      }
    } catch(e) {
      print('登录请求发生异常: $e');
      return null;
    }
  }

  // 登出API
  static Future<bool> logoutUser() async {
    final Uri uri = Uri.parse('$baseUrl/logout/');

    try {
      // * 登出API通常只需要POST请求，不需要body
      final response = await http.post(uri);

      if (response.statusCode == 200) {
        return true;
      } else {
        print('登出失败: ${response.statusCode}');
        print('Response body: ${response.body}');
        return false;
      }
    } catch(e) {
      print('登出请求发生异常: $e');
      return false;
    }
  }

  // 获取用户列表（需要管理员权限)
  static Future<List<User>?> getUserList() async {
    final Uri uri = Uri.parse('$baseUrl/users/');

    try {
      final response = await http.get(uri);

      if ( response.statusCode == 200) {
        final List<dynamic> responseData = jsonDecode(response.body);
        return responseData.map((json) => User.fromJson(json)).toList();
      } else {
        print('获取用户列表失败: ${response.statusCode}');
        print('Response body: ${response.body}');
        return null;
      }
    } catch (e) {
      print('获取用户列表请求发生异常: $e');
      return null;
    }
  }
}