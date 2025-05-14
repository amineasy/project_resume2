from apps.home.models import Product, ProductAttribute

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add_to_cart(self, product, attribute=None, quantity=1):
        product_id = str(product.id)
        if attribute:
            item_id = f'{product_id}_{attribute.id}'
            price = attribute.price
        else:
            item_id = product_id
            price = product.price

        if item_id not in self.cart:
            self.cart[item_id] = {
                'product_id': product_id,
                'attribute_id': attribute.id if attribute else None,
                'price': int(price),
                'quantity': int(quantity)
            }
        else:
            self.cart[item_id]['quantity'] += quantity

        self.save()

    def update_quantity(self, product, attribute=None, quantity=1):
        """به‌روزرسانی تعداد یک محصول خاص"""
        product_id = str(product.id)
        item_id = f'{product_id}_{attribute.id}' if attribute else product_id

        if item_id in self.cart:
            self.cart[item_id]['quantity'] = int(quantity)
            self.save()

    def remove(self, product, attribute=None):
        """حذف یک آیتم خاص از سبد خرید"""
        product_id = str(product.id)
        item_id = f'{product_id}_{attribute.id}' if attribute else product_id

        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        product_ids = [item.split('_')[0] for item in item_ids]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        attribute_ids = [
            item['attribute_id'] for item in self.cart.values()
            if item['attribute_id'] is not None
        ]
        attributes = ProductAttribute.objects.filter(id__in=attribute_ids)
        attribute_map = {attr.id: attr for attr in attributes}

        cart = self.cart.copy()
        for item_id, item in cart.items():
            product_id = item['product_id']
            product = product_map.get(product_id)

            if not product:
                continue  # ⛔ آیتمی که محصولش وجود ندارد را رد کن

            item['product'] = product
            price = int(item['price'])
            quantity = int(item['quantity'])
            item['price'] = price
            item['quantity'] = quantity
            item['total_price'] = price * quantity

            if item['attribute_id']:
                item['attribute'] = attribute_map.get(item['attribute_id'])

            yield item

    def __len__(self):
        """تعداد کل آیتم‌های موجود در سبد خرید (بر اساس تعدادشان)"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_cart_total_price(self):
        return sum(item['total_price'] for item in self)

    def clear(self):
        """خالی کردن کامل سبد خرید"""
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True
