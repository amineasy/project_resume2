from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import *
from django.urls import reverse_lazy

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'],password=data['password'])
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



