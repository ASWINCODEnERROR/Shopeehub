from django.contrib import admin
from .models import Order, OrderedProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'order_date', 'total_amount', 'status', 'is_paid')
    list_filter = ('status', 'is_paid')
    search_fields = ('order_id', 'user__username', 'email', 'phone', 'name')

@admin.register(OrderedProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity') 
    search_fields = ('order__order_id', 'product__name')
