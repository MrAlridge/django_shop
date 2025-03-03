from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """用户的扩展信息"""
    # * 与默认用户模型建立一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # * 用户头像，上传到avatars目录
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='地址')
    # * 用户电话号码
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username}的资料'
# Create your models here.
