from django.contrib import admin
from treebeard.forms import movenodeform_factory
from treebeard.admin import TreeAdmin

from .models import *
from ..media.admin import CategoryImageInline, ProductImageInline, ProductClassImageInline


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    inlines = [CategoryImageInline]



class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductClassImageInline]





class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1




class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('total_price',)
    inlines = [ProductAttributeInline,ProductImageInline]




class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('color',)



class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('size',)




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(ProductAttribute)
