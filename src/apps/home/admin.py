from django.contrib import admin
from treebeard.forms import movenodeform_factory
from treebeard.admin import TreeAdmin
from django.db.models import Sum, Count

from .models import *
from ..cart.models import OrderItem
from ..media.admin import CategoryImageInline, ProductImageInline, ProductClassImageInline
from ..media.models import ProductImage


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
















class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('color',)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('size',)





class TopSellingFilter(admin.SimpleListFilter):
    title = 'پرفروش‌ترین'
    parameter_name = 'top_selling'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'پرفروش‌ترین'),
            ('no', 'غیر پرفروش'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.annotate(
                total_sold=Sum('order_item__quantity')
            ).order_by('-total_sold')[:10]
        elif self.value() == 'no':
            return queryset.annotate(
                total_sold=Sum('order_item__quantity')
            ).order_by('total_sold')[:10]
        return queryset


class MostViewedFilter(admin.SimpleListFilter):
    title = 'پربازدیدترین'
    parameter_name = 'most_viewed'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'پربازدیدترین'),
            ('no', 'کم‌بازدید'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.order_by('-view_count')[:10]
        elif self.value() == 'no':
            return queryset.order_by('view_count')[:10]
        return queryset



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'view_count', 'get_total_sold']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = [TopSellingFilter, MostViewedFilter]
    readonly_fields = ('total_price',)
    inlines = [ProductAttributeInline, ProductImageInline]

    def get_total_sold(self, obj):
        return OrderItem.objects.filter(product=obj).aggregate(total=Sum('quantity'))['total'] or 0

    get_total_sold.short_description = 'تعداد فروش'




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(ProductAttribute)
admin.site.register(Favourite)
