class UserProfile {
  int id;
  String username;
  String? email; //  邮箱可能为空

  UserProfile({required this.id, required this.username, this.email});

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'],
      username: json['username'],
      email: json['email'], //  邮箱可能为 null
    );
  }
}