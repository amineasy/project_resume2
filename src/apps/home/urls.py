from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('category/<int:id>/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product-class/<int:id>/', views.product_class_detail, name='product_class_detail'),
    path('product-class/<int:id>/<slug:slug>/', views.product_class_detail, name='product_class_detail'),
]