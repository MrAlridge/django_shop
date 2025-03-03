from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin #  重命名默认的 UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile # 导入 UserProfile 模型

# 定义一个内联类，用于在 UserAdmin 中显示 UserProfile 信息
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False #  不允许在 UserAdmin 中删除 UserProfile，UserProfile 的删除应该由 User 删除级联完成
    verbose_name_plural = '用户资料' #  在 UserAdmin 中显示的 Inline 名称

# 继承自默认的 UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,) #  将 UserProfileInline 添加到 UserAdmin 中

# 重新注册 User 模型，使用我们自定义的 UserAdmin
admin.site.unregister(User) #  先取消默认的注册
admin.site.register(User, UserAdmin) #  再使用我们自定义的 UserAdmin 重新注册
admin.site.register(UserProfile) #  注册 UserProfile 模型，方便单独管理，虽然通常我们通过 UserAdmin 管理 UserProfile