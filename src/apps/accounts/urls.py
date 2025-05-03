from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<slug:slug>/', views.user_profile, name='profile'),

    path('edit-profile/', views.user_edit_profile, name='edit-profile'),


]





#برای class base view

urlpatterns += [
    path('login/', Login.as_view(), name='login'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

