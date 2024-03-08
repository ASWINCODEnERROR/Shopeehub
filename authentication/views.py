from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import ChangePasswordSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.message import MESSAGE_ERROR, MESSAGE_SUCCESS
from authentication.models import User




class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registration successful",
                "code": status.HTTP_201_CREATED,
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("username" , username )
        print("password" , password )
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login'+ MESSAGE_SUCCESS,
                'code': status.HTTP_200_OK,
                'access_token': str(refresh.access_token),
                'role': user.role 
            })
        return Response({'message': MESSAGE_ERROR }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_registered_users(request):
    registered_users = User.objects.all()
    serializer = UserSerializer(registered_users, many=True)
    return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'message': 'Old password is incorrect', 'code': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully', 'code': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

