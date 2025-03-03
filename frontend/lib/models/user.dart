class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final bool isStaff;
  final UserProfile? profile;   // 用户资料

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.isStaff,
    this.profile,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      // 这两个字段可能为空
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      isStaff: json['is_staff'],
      // * 如果存在profile的话就解析它
      profile: json['profile'] != null ? UserProfile.fromJson(json['profile']) : null,
    );
  }
}

class UserProfile {
  final String? avatar;
  final String? address;
  final String? phoneNumber;

  UserProfile({
    this.avatar,
    this.address,
    this.phoneNumber,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      avatar: json['avatar'],
      address: json['address'],
      phoneNumber: json['phone_number'],
    );
  }
}