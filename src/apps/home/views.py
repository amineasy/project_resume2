from django.shortcuts import render, get_object_or_404

from apps.accounts.models import Profile


def home(request):
    profile = get_object_or_404(Profile, user=request.user)

    context = {'profile': profile}
    return render(request,'home/home.html',context)
