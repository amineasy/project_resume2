from django.db import models
from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title
