from django.urls import path
from .views import ApiCart





urlpatterns = [
    path('api/cart/', ApiCart.as_view(), name='api-cart'),
    path('api/cart/<int:pk>/', ApiCart.as_view(), name='api-cart-detail'),
    path('api/cart/user_totals/', ApiCart.as_view(), {'get': 'user_cart_totals'}, name='api-cart-user-totals'),
]


# ================================================================= =================================================================







# urlpatterns = [
#     path('api/cart/', ApiCart.as_view(), name='api-cart-list'),
#     path('api/cart/<int:pk>/', ApiCart.as_view(), name='api-cart-detail'),
#     # path('api/cart/subtotal/', ApiCart.subtotal, name='api-cart-subtotal'),
#     # path('api/cart/total/', ApiCart.total, name='api-cart-total'),
#     # path('api/cart/user-totals/', ApiCart.user_cart_totals, name='api-cart-user-totals'),
#     # path('api/cart/', UserCartItems.as_view(), name='user_cart_items'),
#     path('api/cart/user_totals/', ApiCart.as_view({'get': 'user_cart_totals'}), name='api-cart-user-totals'),


# ]
