from django.contrib import admin
from .models import Category, Product, ProductImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent_category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)} #  根据名称自动填充 Slug 字段

admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline): #  TabularInline 以表格形式嵌入
    model = ProductImage
    extra = 1 #  默认显示 1 个空的图片上传表单

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description', 'short_description', 'sku', 'barcode')
    ordering = ('-created_at', 'price')
    prepopulated_fields = {'sku': ('name',)} #  根据名称自动填充 SKU 字段 (实际 SKU 生成规则可能更复杂)
    inlines = [ProductImageInline] #  在 Product 编辑页嵌入 ProductImage 的编辑

fieldsets = ( #  自定义表单页字段分组
        ('Basic Information', { #  分组名称
            'fields': ('name', 'category', 'brand', 'unit', 'sku', 'barcode', 'is_active') #  分组包含的字段
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock_quantity')
        }),
        ('Description', {
            'fields': ('short_description', 'description'),
            'classes': ('collapse',) #  默认折叠分组
        }),
    )


admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductImage) # ProductAdmin 中已经通过 inlines 管理 ProductImage，这里可以不注册，也可以注册 ProductImage 模型本身的管理

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone_number') #  搜索关联 User 模型的字段，使用 user__username 语法

# TODO: 等具体需求到了再对用户自定义模型进行细化
# admin.site.register(UserProfile, UserProfileAdmin)