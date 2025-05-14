# forms.py

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'postal_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'phone': 'شماره تماس',
            'address': 'آدرس',
            'postal_code': 'کد پستی',
        }
