from django.urls import path
from .views import *


urlpatterns = [
    path('orders/', OrderAPIView.as_view(), name='order-list-create'),
    # path('test/', Test.as_view(), name='test'),
      path('orders/<int:order_id>/items/', OrderedItemsAPIView.as_view(), name='ordered-items'),
      path('order/<int:pk>/update-status/', UpdateOrderStatusAPIView.as_view(), name='update-order-status'),
]
