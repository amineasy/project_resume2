from django.contrib import admin

from apps.cart.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [OrderItemInline]




admin.site.register(Order,OrderAdmin)

