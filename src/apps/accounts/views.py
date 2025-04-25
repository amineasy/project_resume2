from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import *

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
