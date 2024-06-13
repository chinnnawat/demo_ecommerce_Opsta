
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.views import UserInfo, AuthViewSet, GetUserInfoView
from ecommerce.views import ProductAll, ApplyPromotion, CartViewSet, ShowCartViewSet

# query
router = routers.DefaultRouter()
router.register(r'product', ProductAll, basename='product')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'add_cart', CartViewSet, basename='cartViewSet')
router.register(r'apply_promotion', ApplyPromotion, basename='apply_promotion')
router.register(r'show_cart', ShowCartViewSet, basename='show_cart')
router.register(r'user', GetUserInfoView, basename='get_user_info')

urlpatterns = [
    path('api/', include((router.urls))),
    path('get_user_info/', UserInfo.as_view()),
    path("admin/", admin.site.urls),
]