# from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product, Cart, CartProduct, Promotion, Category, Order



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() # show name
    class Meta:
        model = Product
        fields = '__all__'
        
        
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartProduct 
        fields = ['product', 'quantity' ]
        
        
class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True, read_only=True)
    class Meta:
        model = Cart 
        fields = ['created_at', 'cart_products', 'totalPrice']
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
        