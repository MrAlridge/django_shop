import 'package:flutter/material.dart';
import '../services/api_service.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _password2Controller = TextEditingController();
  final _emailController = TextEditingController();

  String _errorMessage = '';    // 用于显示错误信息

  Future<void> _register() async {
    if (_formKey.currentState!.validate()) {
      final username = _usernameController.text;
      final password = _passwordController.text;
      final password2 = _password2Controller.text;
      final email = _emailController.text;

      final user = await ApiService.registerUser(
        username: username,
        password: password,
        password2: password2,
        email: email,
      );

      if (user != null) {
        print('注册成功: ${user.username}');
        // TODO 跳转到登录页面或者直接进入应用主页
      } else {
        setState(() {
          // ! 显示错误信息
          _errorMessage = '注册失败，请检查输入信息';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('注册')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: <Widget>[
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(labelText: '用户名'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入用户名';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: '邮箱'),
                validator: (value) {
                  if (value == null || value.isEmpty || !value.contains('@')) {
                    return '请输入有效的邮箱地址';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _passwordController,
                obscureText: true,    // TODO 这里后期可以跟显示密码进行联动
                decoration: const InputDecoration(labelText: '密码'),
                validator: (value) {
                  if (value == null || value.isEmpty || value.length < 6) {
                    return '密码长度至少为6位';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _password2Controller,
                obscureText: true,  // TODO 这里也是
                decoration: const InputDecoration(labelText: '确认密码'),
                validator: (value) {
                  if (value == null || value.isEmpty || value != _passwordController.text) {
                    return '两次密码输入不一致';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _register,
                child: const Text('注册'),
              ),
              if (_errorMessage.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 10.0),
                  child: Text(
                    _errorMessage,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
            ],
          )),
      ),
    );
  }
}