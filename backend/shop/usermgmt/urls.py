from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, PasswordChangeView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'), # 获取和更新用户资料
    # TODO: 这几个视图等代码完善了再取消注释
    # path('users/password/change/', PasswordChangeView.as_view(), name='password-change'),
    # path('users/password/reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # path('users/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]