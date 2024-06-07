
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.views import UserInfo, AuthViewSet
from ecommerce.views import DetailProduct


# query
router = routers.DefaultRouter()
router.register(r'product', DetailProduct, basename='product')
router.register(r'auth', AuthViewSet, basename='auth')


urlpatterns = [
    path('api/', include((router.urls))),
    path('get_user_info/', UserInfo.as_view()),
    path("admin/", admin.site.urls),
]

    # path('api/register/', Register.as_view(), name='register'),
    # path('api/login/', LoginView.as_view(), name='login'),
    # path('api/login/', , name='login'),
    # path('accounts/', include('allauth.urls')),