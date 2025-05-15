from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.cart.forms import OrderForm
from apps.cart.models import OrderItem
from apps.cart.sessions import Cart
from apps.home.models import Product, ProductAttribute

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    color_id = request.POST.get('color_id')
    size_id = request.POST.get('size_id')
    quantity = int(request.POST.get('quantity', 1))

    attribute = None
    if color_id or size_id:
        try:
            attribute = ProductAttribute.objects.get(product=product, color_id=color_id or None, size_id=size_id or None)
        except ProductAttribute.DoesNotExist:
            messages.error(request, 'این ترکیب رنگ و سایز وجود ندارد.')
            return redirect(request.META.get('HTTP_REFERER', 'home:home'))

    cart.add_to_cart(product, attribute, quantity)
    messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد.')
    return redirect('cart:cart_view')


def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'total_price': cart.get_cart_total_price()
    })


def decrease_cart_quantity(request, product_id, attribute_id=None):
    """کاهش تعداد محصول در سبد خرید"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    attribute = None
    if attribute_id:
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)

    # مقدار فعلی
    current_quantity = cart.cart.get(
        f'{product_id}_{attribute_id}' if attribute else str(product_id),
        {}
    ).get('quantity', 1)

    new_quantity = current_quantity - 1

    if new_quantity < 1:
        messages.error(request, 'حداقل تعداد باید ۱ باشد.')
    else:
        cart.update_quantity(product, attribute, new_quantity)
        messages.success(request, 'تعداد کاهش یافت.')

    return redirect('cart:cart_view')





def increase_cart_quantity(request, product_id, attribute_id=None):
    """افزایش تعداد محصول در سبد خرید"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    attribute = None
    if attribute_id:
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)

    max_quantity = attribute.quantity if attribute else product.quantity

    # مقدار فعلی
    current_quantity = cart.cart.get(
        f'{product_id}_{attribute_id}' if attribute else str(product_id),
        {}
    ).get('quantity', 0)

    new_quantity = current_quantity + 1

    if new_quantity > max_quantity:
        messages.error(request, 'تعداد درخواستی بیشتر از موجودی است.')
    else:
        cart.update_quantity(product, attribute, new_quantity)
        messages.success(request, 'تعداد افزایش یافت.')

    return redirect('cart:cart_view')






def remove_from_cart(request, product_id, attribute_id=None):
    """حذف یک آیتم از سبد خرید"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    attribute = None
    if attribute_id:
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)

    cart.remove(product, attribute)
    messages.success(request, 'محصول از سبد خرید حذف شد.')

    return redirect('cart:cart_view')


def clear_cart(request):
    """خالی کردن کامل سبد خرید (اختیاری)"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'سبد خرید خالی شد.')
    return redirect('cart:cart_view')


def order_cart(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'سبد خرید خالی است.')
        return redirect('cart:cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for i in cart:
                try:

                    product_instance = Product.objects.get(id=i['product_id'])
                    attribute_instance = None
                    if i['attribute_id']:
                        attribute_instance = ProductAttribute.objects.get(id=i['attribute_id'])

                    OrderItem.objects.create(
                        order=order,
                        product=product_instance,
                        attribute=attribute_instance,
                        quantity=i['quantity'],
                        price=i['price']
                    )
                except Product.DoesNotExist:
                    messages.error(request, f"محصول با ID {i['product_id']} یافت نشد.")
                    continue
                except ProductAttribute.DoesNotExist:
                    messages.error(request, f"ویژگی با ID {i['attribute_id']} یافت نشد.")
                    continue

            cart.clear()
            messages.success(request, 'سفارش با موفقیت ثبت شد.')
        else:
            messages.error(request, 'لطفاً فرم را به درستی پر کنید.')
    else:
        form = OrderForm()

    context = {'form': form, 'cart': cart}
    return render(request, 'cart/order_cart.html', context)