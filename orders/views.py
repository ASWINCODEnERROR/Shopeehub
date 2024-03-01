from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Order , OrderedProduct
from orders.serializer import OrderSerializer,OrderedProductSerializer,UpdateStatusSerializer
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from django.db import transaction 
from rest_framework.generics import UpdateAPIView
from rest_framework import status






# class OrderAPIView(APIView):
class OrderAPIView(APIView):
    def for_token(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            return authorization_header.split(' ')[1] 
        return None
 
 
    def get(self, request, format=None):
        try:
            token = self.for_token(request)
            if not token:
                return Response({"error": "Authentication credentials were not provided.", "code": status.HTTP_401_UNAUTHORIZED})

            orders = Order.objects.filter(user=request.user)
            serialized_orders = []

            for order in orders:
              
                order_data = OrderSerializer(order).data

                print("Order_Data" , order_data)
                
                ordered_products = OrderedProduct.objects.all()
                print("++++++++++++++++++++++++++++++++++++++++++" , ordered_products)
                ordered_product_data = OrderedProductSerializer(ordered_products, many=True).data

                print("-------------------------" , ordered_product_data)
                
                
                order_data['ordered_products'] = ordered_product_data

                # serialized_orders.append(order_data)

            return Response({"message": "Items retrieved successfully", "code": status.HTTP_200_OK, "data": order_data})
        except:
            return Response({"error": "Failed to retrieve orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def post(self, request, format=None):
            try:
                token = self.for_token(request)
                if not token:
                    return Response({"error": "Authentication credentials were not provided.", "code": status.HTTP_401_UNAUTHORIZED})

                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    with transaction.atomic(): 
                        order = serializer.save(user=request.user)
                        print("000000000000000000000000000000000order saved", order)

                        ordered_products_data = request.data.get('ordered_products', [])

                        for ordered_product_data in ordered_products_data:
                            product_id = ordered_product_data.get('product_id')
                            quantity = ordered_product_data.get('quantity')
                            print("product&quantity",product_id,quantity)

                            OrderedProduct.objects.create(order=order, product_id=product_id, quantity=quantity)
                            print("order created",serializer.data )
                    return Response({"message": "Order created successfully", "code": status.HTTP_201_CREATED, "data": serializer.data})
                return Response({"message": "Failed to create order", "code": status.HTTP_400_BAD_REQUEST, "data": serializer.errors})
            except:
                return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



class OrderedItemsAPIView(APIView):
    def get(self, request, order_id, format=None):
        try:
            order = Order.objects.filter(id=order_id).first()
            if order:
                ordered_products = OrderedProduct.objects.filter(order_id__id = order.id)
                serializer = OrderedProductSerializer(ordered_products, many=True)
                print("000000000000000111111111111111110000000000000",ordered_products)
                return Response({"message": "Ordered items retrieved successfully", "code": status.HTTP_200_OK, "data": serializer.data})
            else:
                return Response({"error": "Order does not exist for the given ID"}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({"error": "Failed to retrieve ordered items", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateOrderStatusAPIView(UpdateAPIView):
    serializer_class = UpdateStatusSerializer

    def update(self, request, *args, **kwargs):
        try:
            print("0000000000000000000000",self.kwargs.get('pk'))
            order_id = self.kwargs.get('pk')  
            print ("THE ORDER ID TO UPDATE" , order_id)
            order = Order.objects.get(order_id=order_id)  
            serializer = self.get_serializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            
            print ("THE ORDER ID" , order)
            order.status = request.data['status']
            order.save()

            return Response({"message": "Order status updated successfully", "code": status.HTTP_200_OK,"data": serializer.data})
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to update order status", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class UpdateOrderStatusAPIView(UpdateAPIView):
#     serializer_class = UpdateStatusSerializer

#     def update(self, request, *args, **kwargs):
#         try:
#             order = Order.objects.get(id=order_id).first()
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             # print("Order ID:", order_id)  
              
#             self.perform_update(serializer)
#             return Response({"message": "Order status updated successfully", "code": status.HTTP_200_OK, "data": serializer.data})
#         except Exception as e:
#             return Response({"error": "Failed to update order status", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#     # def get(self, request, format=None):
#     def get(self, request):
    
#         try:
            
#             orders = Order.objects.filter(user=request.user)
#             serializer = OrderSerializer(orders, many=True)
#             print ("data",serializer.data)
#             return Response({"message": "Items retrieved successfully", "code": 200, "data": serializer.data})
#         except:
#             print ("888888888888888888888")
#             return Response({"error": "Failed to retrieve orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
#     def post(self, request, format=None):
#         try:
#             serializer = OrderSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(user=request.user)
#                 print ("000000000000000000000000000")
#                 return Response({"message": "Order created successfully", "code": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
#             return Response({"message": "Failed to create order", "code": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# class OrderAPIView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         print("0o0o0o0o0o0o0o0ooo")
#         try:
#             print("THE USER IS" , request.user)
#             orders = Order.objects.filter(user=request.user)
#             serializer = OrderSerializer(orders, many=True)
#             return Response({"message": "Items retrieved successfully", "code": 200, "data": serializer.data})
#         except:
#             return Response({"error": "Failed to retrieve orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
#     def post(self, request, format=None):
#         try:
#             serializer = OrderSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(user=request.user)
#                 return Response({"message": "Order created successfully", "code": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
#             return Response({"message": "Failed to create order", "code": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except PermissionDenied:
#             return Response({"message": "Authentication credentials were not provided.", "code": 401}, status=status.HTTP_401_UNAUTHORIZED)
#         except:
#             return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
    # 
    # def get_permissions(self):
    #     if self.request.method in ["PATCH", "DELETE"]:
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]