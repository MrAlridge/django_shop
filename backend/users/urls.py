from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# 注册users路由到ViewSet
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),    # 注册API
    path('login/', views.LoginView.as_view(), name='login'),             # 登录API
    path('logout/', views.LogoutView.as_view(), name='logout'),          # 登出API
]
