import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='old_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='old_price', lookup_expr='lte')
    category_name = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    product_name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {
            'category__category_id': ['exact'],
            
        }
        
    def filter_size(self, queryset, name, value):
        if value in ['s', 'm','l','xl','xxl']:
            return queryset.filter(size=value)
        return queryset