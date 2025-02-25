from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usermgmt.urls')), # 包含 user 应用的 URL 配置，URL 前缀为 /api/user/
    path('api/', include('product.urls')),  # 包含 product 应用的 URL 配置，URL 前缀为 /api/product/
    path('api/', include('order.urls')),
    path('api/', include('cart.urls')),
]
