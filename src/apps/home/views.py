from django.shortcuts import render, get_object_or_404

from apps.accounts.models import Profile
from apps.home.models import Category


def home(request):

    category = Category.get_root_nodes()

    context = {'category': category}

    return render(request,'home/home.html',context)
