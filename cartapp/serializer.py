from rest_framework import serializers
from .models import Cartitems
from productapp.serializer import ProductSerializer
from cartapp.models import *
from django.contrib.auth.models import User


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]

class CartitemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True) 
    subtotal = serializers.SerializerMethodField()
 

    class Meta:
        model = Cartitems
        fields = ['id', 'product', 'quantity', 'subtotal']
        # fields = ['id', "user",'product', 'quantity', 'subtotal', 'grand_total']
        

    def create(self, validated_data):
        print("THE VALIDATED DATA IS" , validated_data)
        return Cartitems.objects.create(**validated_data)

    def get_subtotal(self, obj):
        product = obj.product
        if product:
            return product.price * obj.quantity
        return 0 
















# ===================================================================================================================


















    # def get_grand_total(self, obj):
    #       return obj.quantity * (obj.product.price if obj.product else 0)

# class CartSerializer(serializers.ModelSerializer):
#     id = serializers.UUIDField(read_only=True)
#     items =CartitemsSerializer(read_only=True)
#     grand_total = serializers.SerializerMethodField()
#     class Meta:
#         model = Cartitems
#         fields = ["id","items","grand_total"]
        
        
#     def get_grand_total(self, obj):
#         items = obj.items.all()
#         grand_total = sum(item.subtotal for item in items)
#         return grand_total
#     # def main_total(self, cart: Cartitems):
#     #     items =cart.items.all()
#     #     total = sum([item.quantity * item.product.price for item in items])