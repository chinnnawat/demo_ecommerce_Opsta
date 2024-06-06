from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status , viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate, login
from rest_framework import generics
from .models import User

class UserInfo(APIView):
    # Validate Token
    # recieve user info from token
    def post(self, request, format=None):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return Response({'error': 'Missing or invalid Authorization header'}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = auth_header.split(' ')[1]
        # print(access_token)
        
        user_info_url = f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}'
        
        response = requests.get(user_info_url)  # Use requests.get to make the HTTP request
        
        # print(response)
        
        if response.status_code == 200:
            return Response({
            'message': 'Token received successfully',
            'user_info': response.json()  # Return the JSON response from Google
        }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to fetch user info from Google'}, status=status.HTTP_403_FORBIDDEN)
        
        
        
class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('userData')
        
        if not user_data:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = user_data.get('email')
        first_name = user_data.get('firstName')
        last_name = user_data.get('lastName')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User logged in successfully"
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            user_data = {
                'email': email,
                'name': first_name,
                'lastname': last_name,
                'password': email  # หรือรหัสผ่านอื่นที่ต้องการ
            }
            serializer = RegisterSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        
    # def post(self, request, format=None):
    #     auth_body = request.META
    #     print(auth_body)



# class TestLoginView(APIView):
    # def post(self, request, format=None):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         email = serializer.validated_data['email']
    #         # password = serializer.validated_data['password']
    #         user = authenticate(request, email=email)
            
    #         print(user)
            
    #         if user is not None:
    #             login(request, user)  # ล็อกอินผู้ใช้ทันทีหลังจากการล็อกอิน
    #             return Response({
    #                 "user": {
    #                     "email": user.email,
    #                     "name": user.name,
    #                     "surname": user.surname,
    #                 },
    #                 "message": "User logged in successfully"
    #             })
    #         else:
    #             return Response({"error": "Invalid login credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)