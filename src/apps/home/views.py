import json
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from apps.accounts.models import Profile
from apps.home.models import Category, ProductClass, Product, Favourite

User = get_user_model()





def home(request):
    # دریافت دسته‌بندی‌های ریشه
    category = Category.get_root_nodes()

    # دریافت 3 محصول پرفروش با کش
    cache_key_top = 'top_selling_products_home'
    top_selling = cache.get(cache_key_top)
    if top_selling is None:
        print("محاسبه پرفروش‌ترین محصولات برای صفحه اصلی...")
        top_selling = Product.get_top_selling_products(limit=3)  # فقط 3 تا
        cache.set(cache_key_top, top_selling, 60 * 15)  # 15 دقیقه کش
    else:
        print("گرفتن پرفروش‌ترین از کش برای صفحه اصلی")

    # دریافت 3 محصول پربازدید با کش
    cache_key_viewed = 'most_viewed_products_home'
    most_viewed = cache.get(cache_key_viewed)
    if most_viewed is None:
        print("محاسبه پربازدیدترین محصولات برای صفحه اصلی...")
        most_viewed = Product.get_most_viewed_products(limit=3)  # فقط 3 تا
        cache.set(cache_key_viewed, most_viewed, 60 * 15)  # 15 دقیقه کش
    else:
        print("گرفتن پربازدیدترین از کش برای صفحه اصلی")

    context = {
        'category': category,
        'top_selling': top_selling,
        'most_viewed': most_viewed
    }
    return render(request, 'home/home.html', context)

def top_selling_products(request):
    # دریافت همه پرفروش‌ترین محصولات با کش
    cache_key = 'top_selling_products'
    top_selling = cache.get(cache_key)
    if top_selling is None:
        print("محاسبه پرفروش‌ترین محصولات...")
        top_selling = Product.get_top_selling_products(limit=5)  # مثلاً 10 تا
        cache.set(cache_key, top_selling, 60 * 15)  # 15 دقیقه کش
    else:
        print("گرفتن پرفروش‌ترین از کش")

    context = {
        'top_selling': top_selling
    }
    return render(request, 'home/top_selling.html', context)

def most_viewed_products(request):
    # دریافت همه پربازدیدترین محصولات با کش
    cache_key = 'most_viewed_products'
    most_viewed = cache.get(cache_key)
    if most_viewed is None:
        print("محاسبه پربازدیدترین محصولات...")
        most_viewed = Product.get_most_viewed_products(limit=5)  # مثلاً 10 تا
        cache.set(cache_key, most_viewed, 60 * 15)  # 15 دقیقه کش
    else:
        print("گرفتن پربازدیدترین از کش")

    context = {
        'most_viewed': most_viewed
    }
    return render(request, 'home/most_viewed.html', context)


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
    user = request.user
    is_favourite = False
    product.increase_view_count()

    if user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=user, product=product).exists()

    # بهینه‌سازی کوئری با select_related
    attributes = product.attributes_related.select_related('color', 'size').all()

    # دریافت لیست رنگ‌ها و اندازه‌ها
    colors = attributes.filter(color__isnull=False) \
        .values('color_id', 'color__color') \
        .distinct()

    sizes = attributes.filter(size__isnull=False) \
        .values('size_id', 'size__size') \
        .distinct()

    # تولید داده‌های واریانت با مدیریت None
    variant_data = [
        {
            'color_id': attr.color.id if attr.color else None,
            'size_id': attr.size.id if attr.size else None,
            'price': attr.price or 0,
            'discount_price': attr.discount_price or None,
            'total_price': attr.total_price or 0
        }
        for attr in attributes
    ]

    # واریانت پیش‌فرض
    default_attribute = attributes.first() if attributes.exists() else None

    context = {
        'product': product,
        'is_favourite': is_favourite,
        'colors': colors,
        'sizes': sizes,
        'has_colors': colors.exists(),
        'has_sizes': sizes.exists(),
        'default_attribute': default_attribute,
        'variant_data': json.dumps(variant_data),
    }
    return render(request, 'home/product_detail.html', context)


def product_favourite(request, product_id):
    http_referer = request.META.get('HTTP_REFERER', 'home:home')  # پیش‌فرض: صفحه اصلی
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    product = get_object_or_404(Product, id=product_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f'{product.title} به علاقه‌مندی‌ها اضافه شد.')
    else:
        favourite.delete()
        messages.success(request, f'{product.title} از علاقه‌مندی‌ها حذف شد.')

    return redirect(http_referer)


def product_favourite_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    favourites = Favourite.objects.filter(user=request.user)
    context = {'favourites': favourites}
    return render(request, 'home/product_favourite_list.html', context)
