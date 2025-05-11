from itertools import product

from django.db import models
from treebeard.mp_tree import MP_Node

from config import settings


class Category(MP_Node):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title





class ProductClass(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title





class Product(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField(blank=True,null=True)
    discount_price = models.IntegerField(blank=True,null=True)
    total_price = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(default=1)

    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)

    def get_total_price(self):
        if self.discount_price:
            discount_amount = (self.discount_price / 100) * self.price
            return self.price - discount_amount
        return self.price


    def __str__(self):
        return self.title



    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='attributes_related')
    color = models.ForeignKey('ProductColor', on_delete=models.CASCADE,blank=True, null=True)
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(blank=True,null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)

    def get_total_price(self):
        if self.price is not None:
            base_price = self.price
        else:
            base_price = self.product.price

        if self.discount_price is not None:
            discount = self.discount_price
        else:
            discount = self.product.discount_price

        if discount:
            discount_amount = (discount / 100) * base_price
            return base_price - discount_amount

        return base_price


    def get_price(self):
        if self.price is not None:
            return self.price
        else:
            self.price = self.product.price
            return self.price


    def get_discount_price(self):
        if self.price == self.product.price:
            self.discount_price = self.product.discount_price
            return self.discount_price
        else:
            return None






    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        self.price = self.get_price()
        self.discount_price = self.get_discount_price()

        super().save(*args, **kwargs)









class ProductColor(models.Model):
    color = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.color



class ProductSize(models.Model):
    size = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.size



class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


    def __str__(self):
        return f'{self.user} - {self.product}'