
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.views import UserInfo, AuthViewSet, GetUserInfoView
from ecommerce.views import ProductAll, ApplyPromotion, CartViewSet, ShowCartViewSet

# public product
router_public = routers.DefaultRouter()
router_public.register(r'product', ProductAll, basename='product')
# router_public.register(r'auth', AuthViewSet, basename='auth')
router_public.register(r'add_cart', CartViewSet, basename='cartViewSet')
router_public.register(r'apply_promotion', ApplyPromotion, basename='apply_promotion')
router_public.register(r'show_cart', ShowCartViewSet, basename='show_cart')
router_public.register(r'user', GetUserInfoView, basename='get_user_info')


# start
router = routers.DefaultRouter()

# private user
router_user = routers.DefaultRouter()
router_user.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include((router.urls))),
    path('api/public/', include((router_public.urls))),
    path('api/private/', include((router_user.urls))),
    path('get_user_info/', UserInfo.as_view()),
    path("admin/", admin.site.urls),
]