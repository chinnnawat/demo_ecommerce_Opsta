from django.urls import path, include
from . import views
from rest_framework import routers
from .views import DetailProduct, UserViewSet, GroupViewSet

# rest api
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'products', DetailProduct)

urlpatterns = [
    # path("", views.index, name="index"),
    path('', include(router.urls)),
    # path("products/", views.productDetail, name="productDetail"),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]