from django.shortcuts import render, get_object_or_404

from apps.accounts.models import Profile


def home(request):

    return render(request,'home/home.html')
