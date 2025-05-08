from apps.home.models import Product, ProductAttribute


CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add_cart(self, product, attribute=None, quantity=1, override_quantity=False):

        product_id = str(product.id)
        if attribute:
            item_id = f"{product_id}_{attribute.id}"
            price = attribute.total_price or product.total_price
        else:
            item_id = product_id
            price = product.total_price

        if item_id not in self.cart:
            self.cart[item_id] = {
                'product_id': product_id,
                'attribute_id': attribute.id if attribute else None,
                'quantity': quantity,
                'price': price
            }
        else:
            if override_quantity:
                self.cart[item_id]['quantity'] = quantity
            else:
                self.cart[item_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update_quantity(self, item_id, quantity):
        if item_id in self.cart and quantity > 0:
            self.cart[item_id]['quantity'] = quantity
            self.save()
        elif quantity <= 0:
            self.remove(item_id)

    def clear(self):
        self.cart = {}
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True

    def get_cart_items(self):
        cart_items = []
        for item_id, item in self.cart.items():
            product = Product.objects.get(id=item['product_id'])
            attribute = None
            if item['attribute_id']:
                attribute = ProductAttribute.objects.get(id=item['attribute_id'])
            cart_items.append({
                'item_id': item_id,
                'product': product,
                'attribute': attribute,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item['price'] * item['quantity']
            })
        return cart_items

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        return iter(self.get_cart_items())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

