from django.shortcuts import render, get_object_or_404
from apps.accounts.models import Profile
from apps.home.models import Category, ProductClass, Product



def home(request):

    category = Category.get_root_nodes()

    context = {'category': category}

    return render(request,'home/home.html',context)





def category_detail(request, id, slug=None):
    category = get_object_or_404(Category, id=id, slug=slug)
    product_classes = ProductClass.objects.filter(category=category)
    children = category.get_children()
    context = {
        'category': category,
        'product_classes': product_classes,
        'children': children,
    }
    return render(request, 'home/category_detail.html', context)




def product_class_detail(request, id, slug=None):
    product_class = get_object_or_404(ProductClass, id=id, slug=slug)
    products = Product.objects.filter(product_class=product_class)
    context = {
        'product_class': product_class,
        'products': products,
    }
    return render(request, 'home/product_class_detail.html', context)










def product_detail(request, id, slug=None):

    product = get_object_or_404(Product, id=id, slug=slug)
    context = {'product': product}

    return render(request,'home/product_detail.html',context)