
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.views import UserInfo, AuthViewSet
from ecommerce.views import ProductAll, ApplyPromotion, CartViewSet

# query
router = routers.DefaultRouter()
router.register(r'product', ProductAll, basename='product')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'add_cart', CartViewSet, basename='cartViewSet')
router.register(r'apply_promotion', ApplyPromotion, basename='apply_promotion')

urlpatterns = [
    path('api/', include((router.urls))),
    path('get_user_info/', UserInfo.as_view()),
    path("admin/", admin.site.urls),
]