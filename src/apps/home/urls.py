from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('category/<int:id>/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product-class/<int:id>/', views.product_class_detail, name='product_class_detail'),
    path('product-class/<int:id>/<slug:slug>/', views.product_class_detail, name='product_class_detail'),
    path('product-detail/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('product-favourite/<int:product_id>/', views.product_favourite, name='product_favourite'),
    path('favourites/', views.product_favourite_list, name='product_favourite_list'),
    path('top-selling/', views.top_selling_products, name='top_selling'),
    path('most-viewed/', views.most_viewed_products, name='most_viewed'),
]