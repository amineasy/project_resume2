from django.db import models
from PIL import Image as PILImage

from apps.home.models import *


class Image(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class CategoryImage(Image):
    image = models.ImageField(upload_to='category-image',blank=True,null=True)
    image_category = models.ForeignKey('home.Category',on_delete=models.CASCADE,blank=True,null=True,related_name='images')




class ProductClassImage(Image):
    image = models.ImageField(upload_to='product-image',blank=True,null=True)
    image_product_class = models.ForeignKey('home.ProductClass',on_delete=models.CASCADE,blank=True,null=True,related_name='images')




class ProductImage(Image):
    image = models.ImageField(upload_to='product-image', blank=True, null=True)
    image_product = models.ForeignKey('home.Product', on_delete=models.CASCADE, related_name='images')

