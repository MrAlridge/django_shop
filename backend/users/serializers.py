import email
from pydantic import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import password_validation, authenticate

class UserProfileSerializer(serializers.ModelSerializer): #  为 UserProfile 创建一个 Serializer
    avatar = serializers.ImageField(required=False) #  ImageField 需要特别声明,  required=False 表示头像不是必须的

    class Meta:
        model = UserProfile
        fields = ['avatar', 'address', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True) #  嵌套 UserProfileSerializer，用于展示用户资料
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'profile'] #  添加 'profile' 字段
        # fields = '__all__' #  如果你想包含所有字段，可以使用 '__all__'， 但通常建议显式列出需要的字段

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    # ! write_only 表示这个字段只用于写入，不用于序列化输出，validators 添加密码验证
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)   # 再次输入的密码
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.ImageField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        # 注册接口需要接收的字段
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'avatar', 'address', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # ? 验证两次密码输入是否一致
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "两次密码输入不一致."})
        # ? 验证用户名是否已经存在
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "用户名已存在."})
        # ? 验证邮箱是否已存在
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "邮箱已存在."})
        # ? 验证手机号是否已存在, 这里要检查的是UserProfile模型
        if UserProfile.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "手机号已存在."})
        return data
    
    def create(self, validated_data):
        """创建用户和用户资料"""
        user = User.objects.create_user(    # ! 使用create_user方法创建用户会自动对密码进行哈希加密
            username=validated_data['username'],
            email=validated_data['email'],
            # 使用get方法, 如果validated——data里面没用first——name字段，则使用默认值''
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])   # ! 显式设置密码
        user.save()

        UserProfile.objects.create(     # 创建UserProfile对象
            user=user,
            avatar=validated_data.get('avatar'),
            address=validated_data.get('address'),
            phone_number=validated_data.get('phone_number')
        )
        return user
    
class LoginSerializer(serializers.Serializer):      # 创建登录 Serializer
    # * 用户名和邮箱可以二选一，所以可以留空，但必须需要一个
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password')

        if not username and not email:
            raise serializers.ValidationError({"error": "用户名或邮箱必须提供一个."})
        
        user = None     # 初始化user
        if email:
            # 使用django的authenticate方法验证用户
            user = authenticate(email=email, password=password)
        elif username:
            user = authenticate(username=username, password=password)

        if not user:
            # ! 如果验证失败，authenticate会返回None
            raise serializers.ValidationError({"error": "用户名或邮箱/密码错误."})
        
        # TODO 这一块需要考虑用户是否需要被激活

        if not user.is_active:
            # 验证用户是否被激活
            raise serializers.ValidationError({"error":"用户未激活."})
        
        #  将验证成功的 user 对象添加到 validated_data 中，方便在 View 中使用
        data['user'] = user
        return data
    
