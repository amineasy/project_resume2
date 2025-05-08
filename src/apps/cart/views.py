from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from apps.cart.sessions import Cart
from apps.home.models import Product, ProductAttribute


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        cart = Cart(request)
        quantity = int(request.POST.get('quantity', 1))
        color_id = request.POST.get('color_id')
        size_id = request.POST.get('size_id')

        attribute = None
        if color_id or size_id:
            filters = {'product': product}
            if color_id:
                filters['color__id'] = color_id
            if size_id:
                filters['size__id'] = size_id
            try:
                attribute = ProductAttribute.objects.get(**filters)
            except ProductAttribute.DoesNotExist:
                messages.error(request, 'واریانت انتخاب‌شده معتبر نیست.')
                return redirect('home:product_detail', id=product.id, slug=product.slug)

        # بررسی موجودی
        max_quantity = attribute.quantity if attribute else product.quantity
        if quantity > max_quantity:
            messages.error(request, 'تعداد درخواستی بیشتر از موجودی است.')
            return redirect('home:product_detail', id=product.id, slug=product.slug)

        cart.add_cart(product=product, attribute=attribute, quantity=quantity)
        messages.success(request, f'{product.title} به سبد خرید اضافه شد.')

    return redirect('cart:cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': cart.get_total_price()})


def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('cart_view')


def update_cart(request, item_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update_quantity(item_id, quantity)
    return redirect('cart:cart_view')
