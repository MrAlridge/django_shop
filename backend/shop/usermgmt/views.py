from django.urls import is_valid_path
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail # 发送邮件
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # base64加密与解密
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator # 默认Token生成器
from django.urls import reverse

from backend.shop.product.models import Category, Product
from backend.shop.product.serializers import CategorySerializer, ProductSerializer # 用于生成url
from .serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import IsAdminUserOrReadOnly, IsOperatorUser, UserProfile

class UserRegistrationView(generics.CreateAPIView):
    '''
    URL: /api/users/register/

    HTTP Method: POST
    
    使用 UserRegistrationSerializer 验证和序列化数据。
    
    创建用户和 UserProfile。
    
    返回成功或失败信息。
    '''
    serializer_class = UserRegistrationSerializer

class UserLoginView(APIView):
    """
    URL: /api/users/login/

    HTTP Method: POST
    
    使用 UserLoginSerializer 验证数据 (用户名和密码)。
    
    使用 Django 的 authenticate 和 login 函数进行用户认证和登录。
    
    返回认证 token (例如 JWT Token 或 Session ID)。
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) #  仍然可以保留 Django 的 session 登录 (如果需要 session 支持)
                refresh = RefreshToken.for_user(user) #  为用户生成 Refresh Token 和 Access Token
                return Response({
                    'refresh': str(refresh), #  返回 Refresh Token
                    'access': str(refresh.access_token), # 返回 Access Token
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    URL: /api/users/profile/

    HTTP Method: GET (查看), PUT 或 PATCH (编辑)
    
    需要用户认证 (例如使用 JWT Authentication 或 Session Authentication)。
    
    GET 请求：返回当前登录用户的 UserProfile 信息 (使用 UserProfileSerializer 序列化)。
    
    PUT/PATCH 请求：接收前端提交的用户资料数据 (可以使用 UserProfileSerializer 或 UserProfileUpdateSerializer 反序列化)，更新 UserProfile 信息
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # 需要用户认证

    def get_object(self): # 获取当前登录用户的 UserProfile
        return self.request.user.userprofile # 通过 related_name 'userprofile' 访问

    #  PUT 和 PATCH 方法 DRF 已经默认实现，可以直接更新

# TODO: 完成剩下几个视图的具体代码

class PasswordChangeView():
    """    
    URL: /api/users/password/change/
    
    HTTP Method: POST
    
    需要用户认证。
    
    接收旧密码和新密码。
    
    验证旧密码是否正确。
    
    更新用户密码。
    """
    pass

class PasswordResetRequestView():
    """
    URL: /api/users/password/reset/request/
    
    HTTP Method: POST  * 接收用户邮箱或手机号。
    
    验证邮箱或手机号是否存在。
    
    生成一个临时的重置密码 token。
    
    发送包含重置密码链接的邮件或短信给用户。
    """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO:这里看需求还要改成手机号
            email = serializer.validated_data['email']
            user = User.objects.get(email=email) # 获取用户

            # 生成重置密码Token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk)) # 对User ID进行Base64编码
            token = default_token_generator.make_token(user) # 生成token

            # 生成重置密码链接(TODO:前端页面 URL，需要前端配合实现密码重置页面)
            reset_password_url = request.build_absolute_uri(
                # 暂时假设密码重置的URL name是这个
                reverse('password-reset-confirm-frontend', kwargs={'uidb64': uidb64, 'token': token})
            )
            # TODO:构建完整的前段密码重置链接
            # reset_password_url = f"https//<domain>/password-reset/confirm/{uidb64}/{token}/"

            # 发送重置密码的邮件
            mail_subject = 'Password reset request'
            message = f'Please click the following link to reset your password:\n\n'# {reset_password_url}
            send_mail(mail_subject, message, 'from@example.com', [email]) # TODO:实际生产环境要在这里配置好发件邮箱

            return Response({"message": "Password reset link sent to your email address."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ! `PasswordResetConfirmView` 需要接收前端传递的 `uidb64` 和 `token`，以及新密码。  前端需要解析密码重置链接中的 `uidb64` 和 `token`，并将其与新密码一起 POST 到 `/api/users/password/reset/confirm/` 接口。

class PasswordResetConfirmView():
    """
    URL: /api/users/password/reset/confirm/
    
    HTTP Method: POST
    
    接收重置密码 token 和新密码。
    
    验证 token 的有效性。
    
    重置用户密码。
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            uidb64 = request.data.get('uidb64') # 从request data中获取uuid

            try:
                uid = force_str(urlsafe_base64_decode(uidb64)) # Base64 解码 User ID
                user = User.objects.get(pk=uid) # 根据 User ID 获取用户
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password) # 重置密码
                user.save()
                return Response({"message":"Password reset successful."},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Invalid password reset link."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]    # * 应用自定义权限类，管理员可读写，其他用户只读

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOperatorUser|IsAdminUserOrReadOnly]