from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import UserProfile

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
                login(request, user)
                #  TODO:  生成并返回认证 token (例如 JWT)  -  这里简化处理，实际项目中需要生成 token
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
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
    pass

class PasswordResetConfirmView():
    """
    URL: /api/users/password/reset/confirm/
    
    HTTP Method: POST
    
    接收重置密码 token 和新密码。
    
    验证 token 的有效性。
    
    重置用户密码。
    """
    pass