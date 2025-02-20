import email
import token
from typing import Required
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

# 我们需要使用 Django REST Framework (DRF) 的 Serializers 将 User 和 UserProfile 模型的数据转换为 JSON 格式，
# 以便在 API 接口中返回给前端，同时也要能够将前端传递的 JSON 数据反序列化为模型对象。

class UserSerializer(serializers.ModelSerializer):
    '''
    序列化Django默认的 User 模型
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] # 可以根据需要添加或删除字段

class UserProfileSerializer(serializers.ModelSerializer):
    '''序列化自定义的 UserProfile 模型。'''
    user = UserSerializer(read_only=True) # 嵌套 UserSerializer，只读

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'profile_image', 'gender', 'date_of_birth', 'address', 'role', 'created_at', 'updated_at']
        read_only_fields = ['role', 'created_at', 'updated_at', 'user'] # 角色、创建时间、更新时间、user 字段只读

class UserRegistrationSerializer(serializers.Serializer): # 注册序列化器，不需要 ModelSerializer
    '''用于用户注册时的数据验证和序列化。'''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) # write_only 密码只用于写入，不用于读取
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False) # 手机号可选

    def validate_username(self, value): # 验证用户名是否已存在
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value): # 验证邮箱是否已存在
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data): # 创建用户
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        UserProfile.objects.create(user=user, phone_number=validated_data.get('phone_number', '')) # 创建 UserProfile
        return user

class UserLoginSerializer(serializers.Serializer): # 登录序列化器，不需要 ModelSerializer
    '''用于用户登录时的数据验证和序列化。'''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    """用于验证密码重置请求的Serializer(邮箱或手机号)"""
    # TODO:这一块看实际情况可能要改成手机号
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """用来验证邮箱地址的方法"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address not found!")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    """用于验证密码重置确认的 Serializer (token 和新密码)。"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:    # 验证两次密码输入是否一致
            raise serializers.ValidationError("Passwords do not match")
        return data
