from rest_framework import serializers
from productapp.serializer import *
from cartapp.models import *
from authentication.models import User
from .models import Order, OrderedProduct
from django.db import transaction
from django.contrib.auth import get_user_model





class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]


class OrderedProductSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderedProduct
        fields = ['id', 'product', 'quantity']




class OrderSerializer(serializers.ModelSerializer):
    ordered_products = OrderedProductSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all()) 

    class Meta:
        model = Order
        fields = ['id', 'user', 'email', 'phone', 'address', 'name', 'order_id', 'order_date',
                  'total_amount', 'status', 'payment_method', 'is_paid', 'ordered_products']

    



class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']



# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email')  

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

# class OrderedProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     class Meta:
#         model = OrderedProduct
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     ordered_products = OrderedProductSerializer(many=True, read_only=True)
#     user = CustomUserSerializer()  
#     class Meta:
#         model = Order
#         fields = '__all__'




    # def create(self, validated_data):
    #     ordered_products_data = validated_data.pop('ordered_products')
    #     with transaction.atomic():
    #         order = Order.objects.create(**validated_data)
    #         for ordered_product_data in ordered_products_data:
    #             product_data = ordered_product_data.pop('product')
    #             product = Product.objects.get(id=product_data['id'])
    #             OrderedProduct.objects.create(order=order, product=product, **ordered_product_data)
    #     return order
            