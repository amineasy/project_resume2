from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.is_active = True
            user.save()
            return redirect('home:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class Login(LoginView):
    authentication_form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home:home')


def logout_view(request):
    logout(request)
    return redirect('home:home')


def user_edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'accounts/edit-profile.html', context)


def user_profile(request, slug=None):
    user = request.user
    profile = get_object_or_404(Profile, user=user, slug=slug)
    context = {'profile': profile, 'user': user}
    return render(request, 'accounts/profile.html', context)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/password_reset/done/'


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/reset/done/'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
