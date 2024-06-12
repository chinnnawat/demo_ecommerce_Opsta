# from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product, Cart, CartProduct, Promotion, Category



class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True) => show id
    category = serializers.StringRelatedField() # show name
    class Meta:
        model = Product
        fields = '__all__'
        
        
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct 
        fields = ['product', 'quantity' ]
        
        
class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True, read_only=True)
    class Meta:
        model = Cart 
        fields = ['totalPrice', 'created_at', 'cart_products']
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'