from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status , viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import RegisterSerializer, GetInfoSerializer
from django.contrib.auth import  login
from .models import User
from django.shortcuts import get_object_or_404


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
        
        
        
# class LoginView(generics.CreateAPIView):
class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    
    @action(methods=['post'], detail=False, url_path='login')   
    def login_user(self, request):
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
            
            
# get user info
class GetUserInfoView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetInfoSerializer
    
    @action(methods=['post'], detail=False)
    def get_user_info(self, request):
        user_email = request.data.get('email')
        user_id = get_object_or_404(User, email=user_email)
        print(user_id.id)
        if not user_email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # user = User.objects.get(email=user_email)
            respone_data = {
            "user_id" : user_id.id,
        }
            return Response(respone_data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
    
        