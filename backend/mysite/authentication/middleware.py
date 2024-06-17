from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json
import requests
from .models import User
# from django.contrib.auth import login as auth_login
from django.contrib.auth import login as auth_login
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser

from .backend import TokenAuthBackend

class GoogleOAuth2Middleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
    
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            print('Auth Header:', auth_header)
            access_token = auth_header.split('Bearer ')[1]
            user_info = self.get_user_info(access_token)
            print('User Info:', user_info)
            if user_info:
                user = self.get_or_create_user(user_info)
                if user:
                    print(f"Authenticated User: {user}")
                    request.active_user = user
        
        return self.get_response(request)
        
    def get_user_info(self, access_token):
        print(f'Access Token: {access_token}')
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo?access_token=' + access_token,
                # headers={'Authorization': f'Bearer {access_token}'}
            )
            
            print(f'Response Status Code: {response.status_code}')
               
            if response.status_code == 200:
                return response.json()
            
        except requests.RequestException:
            return None
        return None
    
    def get_or_create_user(self, user_info):
        email = user_info.get('email')
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')
        
        print(f'Email: {email}', f'First Name: {first_name}', f'Last Name: {last_name}', sep='\n')
        
        if not email:
            return None
        
        try:
            user = User.objects.get(email=email)
            user_id = user.id
            print('User ID :', user_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                password=email
            )
        return user

    # def process_request(self, request):
        
    #     if request.path != '/api/private/auth/login_user/':
    #         return
        
    #     auth_header = request.headers.get('Authorization')
    #     if auth_header and auth_header.startswith('Bearer '):
    #         access_token = auth_header.split('Bearer ')[1]
    #         user_info = self.get_user_info(access_token)
    #         if user_info:
    #             user = self.get_or_create_user(user_info)
    #             if user:
    #                 request.user = user
    #                 request._auth = user
    #                 auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    #                 print(f"Authenticated User: {request._auth}")