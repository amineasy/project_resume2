from django.urls import path
from . import views
from .views import *

app_name = 'accounts'


urlpatterns = [
    path('register/', views.register, name='register'),
]


#برای class base view

urlpatterns += [
    path('login/', Login.as_view(), name='login'),

]