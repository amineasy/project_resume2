from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('باید نام کاربری وارد شود')
        if not password:
            raise ValueError('باید پسوورد وارد شود')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    phone_confirmed = models.BooleanField(default=False)
    city = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = []





class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='profile')
    slug = models.SlugField(unique=True,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)




    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}")
        super(Profile, self).save(*args, **kwargs)



    def __str__(self):
        return f"Profile of {self.user.username}"


