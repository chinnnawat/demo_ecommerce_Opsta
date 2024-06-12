from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from authentication.serializers import RegisterSerializer
from .models import Product, Cart, CartProduct, Promotion
from django.http import JsonResponse
from rest_framework import serializers, permissions, viewsets
from rest_framework.response import Response
from authentication.models import User
from rest_framework.decorators import action
from .serializers import  ProductSerializer, CartSerializer, CartProductSerializer, PromotionSerializer
from rest_framework import status
import json
from django.contrib.auth import  login

# Create your views here.
def index(request):
    return HttpResponse("noh")

class ProductAll(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(methods=["GET"], detail=False)
    def getProduct(self):
        queryset = Product.objects.get.all()
        return Response(queryset)
    
    @action(methods=["GET"], detail=True)
    def getProduct_detail(self, request, pk=None):
        product = self.get_object()
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
            
    
class ApplyPromotion(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    @action(methods=["POST"], detail=False)
    def apply_promotion(self, request):
        cart = Cart.objects.get(user=request.user)
        promotion_code = request.data.get('promotion_code')
        promotion = get_object_or_404(Promotion, code=promotion_code)
        if promotion.enable_code():
            total_price = (promotion.discount / 100) * cart.totalPrice
            return Response(f"Promotion applied successfully. Total price is {total_price}")
        else:
            return Response("Promotion is not valid")
        
        
        
class CartViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    
    @action(methods=["post"], detail=False)
    def add_to_cart(self, request):
        user = request.data.get('user') #  รับข้อมูลผู้ใช้ที่ล็อกอินอยู่
        quantity = request.data.get('quantity')
        product_id = request.data.get('product')
        price_unit = request.data.get('price')
        
        print("Current User : ", user)
        print("Quantity : ", quantity)
        print("Product ID : ", product_id)
        print("Price Per  Unit : ", price_unit)
        
        # check from database
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < int(quantity):
            return Response({"error": "Not enough stock available"}, status=400)
        
        
        # get user id from db and compare it with the user from request
        user_id = get_object_or_404(User, email=user)
        print("User ID : ", user_id.id)
        
        # generate Cart
        cart, created = Cart.objects.get_or_create(user=user_id)
        print("Cart : ",cart)
        
        
        # Check if CartProduct already exists in the cart
        try:
            cart_product = CartProduct.objects.get(product=product, cart=cart)
            cart_product.quantity += int(quantity)
            cart_product.save()
        except CartProduct.DoesNotExist:
            cart_product = CartProduct.objects.create(product=product, quantity=quantity, cart=cart)
        
        print("Cart Product : ", cart_product)
        
        # Update total price in cart
        cart.update_total_price()
        print("Cart Product : ",cart_product)
        
        
        # response_data to frontend
        respone_data = {
            "message": "Product added to cart successfully",
            "user_id" : user_id.id,
        }


        return Response(respone_data)
    




class ShowCartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    @action(methods=["POST"], detail=False)
    def show_detal_cart(self, request):
        user_email = request.data.get('user')
        user = get_object_or_404(User ,email=user_email)
        
        print(user)
        
        # user = User.objects.get(email=request.user)
        # cart = Cart.objects.get(user=user)
        # cart_products = CartProduct.objects.filter(cart=cart)
        # serializer = CartProductSerializer(cart_products, many=True)
        return Response("serializer.data")
    
    