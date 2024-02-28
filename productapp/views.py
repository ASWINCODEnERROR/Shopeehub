from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from .filters import ProductFilter
from rest_framework.decorators import api_view
from productapp.serializer import ProductSerializer,CategorySerializer,ReviewSerializer
from .models import *
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
# from authentication.models import User
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated,BasePermission






# Create your views here.



class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'superadmin']



# for paginaation purposes==========================
class CustomPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page' 
    page_size_query_param = 'limit'
    max_page_size = 100  

# product session=====================================


class ApiProduct(APIView):
    permission_classes = [IsAuthenticated]  

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminOrSuperAdmin()]
        return super().get_permissions()

    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category_name', 'category__title', 'price']
    ordering_fields = ['price', 'size']

    def get(self, request, pk=None):
        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            queryset = Product.objects.all()
    
            ordering = request.query_params.get('ordering')
            print("Ordering================================:", ordering)
            
            if ordering == 'size':
           
                queryset = queryset.exclude(size__isnull=True).exclude(size__exact='')
  
            if ordering:
                if ordering == 'price':
                    queryset = queryset.order_by('price')
                elif ordering == '-price':
                    queryset = queryset.order_by('-price')
                elif ordering == 'size':
                    queryset = queryset.order_by('size')
                elif ordering == '-size':
                    queryset = queryset.order_by('-size')
               
            product_filter = ProductFilter(request.query_params, queryset=queryset)
                   
            print("Sorted queryset:", queryset)

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(product_filter.qs, request)
            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# multiple image sessions 
class MultipImageUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk):
        try:
            product_image_list = []
            product_images = request.FILES.getlist('images')
            for image in product_images:
                product_image_list.append(ProductImage(product_id=pk, image=image))
            ProductImage.objects.bulk_create(product_image_list)
            return Response("Images uploaded successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# for categories
class ApiCategories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        categories = Category.objects.filter(category_id=pk)
        if categories.exists():
            category = categories.first()
            serializer = CategorySerializer(category, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("Category not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        categories = Category.objects.filter(category_id=pk)
        if categories.exists():
            category = categories.first()
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Category not found", status=status.HTTP_404_NOT_FOUND)




# =================================================================================================



class ReviewListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

# def product_detail_with_reviews(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     serializer = ProductSerializer(product)
#     return JsonResponse(serializer.data)



# Review=======================

# class ApiReview(APIView):
#     def get(self, request, format=None):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         review = self.get_object(pk)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



#     def get_serializer_context(self):
#         return {"product":self.kwargs["product"]}







