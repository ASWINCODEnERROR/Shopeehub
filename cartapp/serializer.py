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










