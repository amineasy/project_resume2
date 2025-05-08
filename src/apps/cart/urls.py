from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:product_id>/<int:attribute_id>/', views.add_to_cart, name='add_to_cart_with_attribute'),
    path('remove_from_cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<str:item_id>/', views.update_cart, name='update_cart'),
]