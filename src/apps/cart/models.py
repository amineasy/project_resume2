from django.db import models

from apps.home.models import Product, ProductAttribute
from config import settings



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    postal_code = models.CharField(max_length=10,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)


    def total_price(self):
        return sum(i.total_price() for i in self.items.all())


    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"










class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items',)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='order_item')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def total_price(self):
        return self.quantity * self.price












