from django.db import models
from django.contrib.auth.models import User

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