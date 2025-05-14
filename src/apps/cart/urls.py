from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove/<int:product_id>/<int:attribute_id>/', views.remove_from_cart, name='remove_from_cart_with_attr'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('increase/<int:product_id>/', views.increase_cart_quantity, name='increase_quantity'),
    path('increase/<int:product_id>/<int:attribute_id>/', views.increase_cart_quantity,name='increase_quantity_with_attr'),
    path('decrease/<int:product_id>/', views.decrease_cart_quantity, name='decrease_quantity'),
    path('decrease/<int:product_id>/<int:attribute_id>/', views.decrease_cart_quantity,name='decrease_quantity_with_attr'),

    path('order', views.order_cart, name='order_cart'),

]