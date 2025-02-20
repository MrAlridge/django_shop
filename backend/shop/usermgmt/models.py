from django.db import models
from django.contrib.auth.models import User
from rest_framework import permissions

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='userprofile') # 关联 User 模型，并设为 OneToOneField 和主键
    phone_number = models.CharField(max_length=20, blank=True) # 手机号，允许为空
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True) # 头像，上传到 profile_images 目录，允许为空
    gender = models.CharField(max_length=10, blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')]) # 性别，可选
    date_of_birth = models.DateField(null=True, blank=True) # 出生日期，允许为空
    address = models.TextField(blank=True) # 默认收货地址，允许为空
    role = models.CharField(max_length=20, default='customer', choices=[('customer', 'Customer'), ('admin', 'Admin'), ('operator', 'Operator')]) # 用户角色，默认为 customer
    created_at = models.DateTimeField(auto_now_add=True) # 创建时间，自动添加
    updated_at = models.DateTimeField(auto_now=True) # 更新时间，自动更新

    def __str__(self):
        return self.user.username   # 管理后台显示的用户名 
    
# * DRF权限类相关
class IsAdminUserOrReadOnly(permissions.BasePermission):
    """允许管理员用户执行任何操作, 但是其他用户只能执行只读操作."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # * SAFE_METHODS包括GET,HEAD,OPTIONS
            return True     # * 只读允许所有用户访问
        return request.user and request.user.is_staff # 非读请求只允许staff用户(管理员)
    
    def has_object_permission(self, request, view, obj):    # * 对象级别权限控制
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    
class IsOperatorUser(permissions.BasePermission):   # * 运营人员权限
    """只允许管理员访问"""
    def has_permission(self, request, view):
        return request.user and request.user.userprofile.role == 'operator' # 检查角色是否为管理员
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.userprofile.role == 'operator'