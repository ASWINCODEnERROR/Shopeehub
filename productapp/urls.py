from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ApiProduct, ApiCategories, MultipImageUpload, ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView


urlpatterns = [
    # ApiProduct view
    path('products/', ApiProduct.as_view(), name='api_product_list'), 
    path('products/<uuid:pk>/', ApiProduct.as_view(), name='api_product_detail'), 
    
    # ApiCategories view
    path('categories/', ApiCategories.as_view(), name='api_category_list'), 
    path('categories/<uuid:pk>/', ApiCategories.as_view(), name='api_category_detail'),  
    
    #when a product have multiple images 
    path('products/<uuid:pk>/images/bulk_upload/', MultipImageUpload.as_view(), name='bulk_image_upload'),



# = ==================================================================  =   =================================================================

    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-retrieve-update-destroy'),
    # path('reviews/', ApiReview.as_view(), name='review-list'),
    # path('reviews/<int:pk>/', ApiReview.as_view(), name='review-detail'),

]
  