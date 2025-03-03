from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action # 引入action装饰器
from rest_framework.response import Response # 导入Response
from rest_framework.views import APIView     # 导入API View
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from django.contrib.auth.models import User
from .serializers import LoginSerializer, UserSerializer, UserProfileSerializer, RegisterSerializer
from django.contrib.auth import login, logout

class UserViewSet(viewsets.ModelViewSet):
    """用户API接口"""
    queryset = User.objects.all().order_by('-date_joined')  # 按照加入时间倒序排列
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.all().prefetch_related('profile').order_by('-date_joined')
    
    @action(detail=True, methods=['get'])   # * 添加一个action，用于获取用户的详细profile信息
    def profile_detail(self, request, pk=None):
        """获取用户详细Profile信息"""
        user = self.get_object() # 获取当前用户
        profile = user.profile # 通过 related_name 'profile' 获取 UserProfile 对象
        serializer = UserProfileSerializer(profile) #  使用 UserProfileSerializer 序列化 UserProfile 对象
        return Response(serializer.data) # 返回序列化后的数据
    
class RegisterView(GenericAPIView):         # * GenericAPIView提供了serializers的通用处理
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):   # 处理POST请求
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serializer = UserSerializer(user)
        return Response({
            "user": user_serializer.data,
            "message": "用户注册成功",
        }, status=status.HTTP_201_CREATED)
    
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    serializer_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response({
            "user": user_serializer.data,
            "message": "用户登录成功",
        }, status=status.HTTP_200_OK)   # 登陆成功返回200
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)     # 使用Django的logout方法清除session
        return Response({
            "message": "用户登出成功."
        }, status=status.HTTP_200_OK)

# TODO 完成账户激活，密码重置API