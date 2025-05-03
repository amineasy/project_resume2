from django.contrib import admin
from treebeard.forms import movenodeform_factory

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    form = movenodeform_factory(Category)
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)



class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}





class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1




class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('total_price',)
    inlines = [ProductAttributeInline]



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
