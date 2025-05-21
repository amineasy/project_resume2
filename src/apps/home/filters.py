from django.utils import timezone
from datetime import timedelta
import django_filters

from apps.home.models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='effective_price', lookup_expr='gte', label='حداقل قیمت')
    price_max = django_filters.NumberFilter(field_name='effective_price', lookup_expr='lte', label='حداکثر قیمت')
    class Meta:
        model = Product
        fields = []


