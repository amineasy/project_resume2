from django.urls import path
from . import views
from .views import *

app_name = 'accounts'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='profile'),

]


#برای class base view

urlpatterns += [
    path('login/', Login.as_view(), name='login'),

]