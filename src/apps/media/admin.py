from django.contrib import admin

from apps.media.models import CategoryImage, ProductClassImage, ProductImage


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1


class ProductClassImageInline(admin.TabularInline):
    model = ProductClassImage
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


admin.site.register(CategoryImage)
admin.site.register(ProductClassImage)
admin.site.register(ProductImage)
