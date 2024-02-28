from django.urls import path
from .views import RegisterView, LoginView,ChangePasswordView,get_registered_users

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('registered-users/', get_registered_users, name='registered-users'),
    
]