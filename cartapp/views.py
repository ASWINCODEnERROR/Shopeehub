from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from cartapp.models import Cartitems
from cartapp.serializer import CartitemsSerializer
from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from productapp.models import Product

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.contrib.auth.models import User


class ApiCart(APIView):
    
    
    
    
    
    def get(self, request):
        user_id = request.query_params.get('user_id') 
        
        if not user_id:
            return JsonResponse({"error": "User ID parameter is missing", "code": 400})
        
        try:
           user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User with provided ID does not exist", "code": 404})
        
        queryset = Cartitems.objects.filter(user_id=user_id)  
        serializer = CartitemsSerializer(queryset, many=True)
        print("000000000000000000000000000")
        return Response({"message": "Items retrieved successfully", "code": 200, "data": serializer.data})


    def post(self, request):
        print("THE PRODUCT ID IS", request.data)
        serializer = CartitemsSerializer(data=request.data)
        product_data = Product.objects.get(id=request.data['product'])
        print("Product data", product_data)
        
        if serializer.is_valid():
            try:
                serializer.save(product=product_data)
                return JsonResponse({"message": "Item created successfully", "code": 200, "data": serializer.data})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            item = Cartitems.objects.get(pk=pk)
            serializer = CartitemsSerializer(item)
            return JsonResponse({"message": "Item retrieved successfully", "code": 200, "data": serializer.data})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Item with provided ID does not exist", "code": 404})

    def put(self, request, pk=None):
        try:
            item = Cartitems.objects.get(pk=pk)
            serializer = CartitemsSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Item updated successfully", "code": 200, "data": serializer.data})
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Item with provided ID does not exist", "code": 404})
        
        
    def delete(self, request, pk=None):
        try:
            item = Cartitems.objects.get(pk=pk)
            item.delete()
            print("Item deleted successfully")
            return Response({"message": "Item deleted successfully","code": status.HTTP_204_NO_CONTENT})
        except Cartitems.DoesNotExist:
            print("Item does not exist")
            return Response({"error": "Item does not exist","code" : status.HTTP_404_NOT_FOUND})

    def user_cart_totals(self, request):
        user_carts = Cartitems.objects.filter(user__isnull=False).values('user').annotate(
            subtotal=ExpressionWrapper(F('product__price') * F('quantity'), output_field=FloatField()),
        )

        grand_total = sum(item['subtotal'] for item in user_carts)
        return Response({'grand_total': grand_total})

