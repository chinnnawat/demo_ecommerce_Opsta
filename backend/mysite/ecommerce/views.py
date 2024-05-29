from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.http import JsonResponse
from rest_framework import serializers, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group, User
from rest_framework.decorators import action
from .serializers import UserSerializer, GroupSerializer, ProductSerializer

# Create your views here.
def index(request):
    return HttpResponse("noh")

class DetailProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(methods=["GET"], detail=False)
    def getProduct(self, request):
        # queryProduct = Product.objects.get.all()
        queryset = Product.objects.get.all()
        # showProducts = ProductSerializer(queryProduct, many = True, context={'request': request})
        return Response(queryset)


# rest api
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]