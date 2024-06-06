from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.http import JsonResponse
from rest_framework import serializers, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group, User
from rest_framework.decorators import action
from .serializers import  ProductSerializer

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