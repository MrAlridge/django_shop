import 'package:dio/dio.dart';

Future<void> uploadProductImages(int productId, List<MultipartFile> images) async {
  FormData formData = FormData();
  for (var image in images) {
    formData.files.add(MapEntry('image', image));   // * 字段名称设置为'image'
  }

  try {
    final response = await Dio().post(
      '/api/products/$productId/upload_image/',
      data: formData,
      // ? headers: ... (在启用JWT的情况下还要附带Token)
    );
    if (response.statusCode == 201) {
      // * 处理上传成功的响应
      print('Images uploaded successfully');
    } else {
      // * 处理上传失败的响应
      print('Image upload failed: ${response.statusCode}');
    }
  } catch(error) {
    // ! 处理异常
    print('Error uploading images: $error');
  }
}