from decimal import Decimal, ROUND_DOWN
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from authentication.serializers import RegisterSerializer
from .models import Product, Cart, CartProduct, Promotion, Order
from django.http import JsonResponse
from rest_framework import serializers, permissions, viewsets
from rest_framework.response import Response
from authentication.models import User
from rest_framework.decorators import action
from .serializers import  ProductSerializer, CartSerializer, CartProductSerializer, PromotionSerializer
from rest_framework import status
import json
from django.contrib.auth import  login
from django.db.models import Sum, F
from django.utils import timezone

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
        
        # Update the stock of the product
        product.stock -= int(quantity)
        product.save()
        
        # Update total price in cart
        cart.update_total_price()
        print("Cart Product : ",cart_product)
        
        
        
        cart_product_detail = get_object_or_404(Cart, user=user_id)
        
        print(cart_product_detail.id)
        
        
        # response_data to frontend
        respone_data = {
            "message": "Product added to cart successfully",
            "user_id" : user_id.id,
        }


        return Response(respone_data)
    
    
    @action(methods=["post"], detail=False)
    def plus(self, request):
        user_email = request.data.get('user')
        product_id = request.data.get('product')
        
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, email=user_email)
        
        cart = get_object_or_404(Cart, user=user)
        cart_product = get_object_or_404(CartProduct, product=product, cart=cart)
        
        cart_product.quantity += 1
        cart_product.save()
        
        # Update the stock of the product
        product.stock -= 1
        product.save()
        
        cart.update_total_price()
        
        return Response({"message": "Product quantity increased", "quantity": cart_product.quantity, "totalPrice": cart.totalPrice})
    
    @action(methods=["post"], detail=False)
    def minus(self, request):
        user_email = request.data.get('user')
        product_id = request.data.get('product')
        
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, email=user_email)
        
        cart = get_object_or_404(Cart, user=user)
        cart_product = get_object_or_404(CartProduct, product=product, cart=cart)
        
        if cart_product.quantity >= 1:
            cart_product.quantity -= 1
            cart_product.save()
            
            
            # Update the stock of the product
            product.stock += 1
            product.save()
        
        if cart_product.quantity == 0:
            cart_product.delete()
            cart.update_total_price()
            message = "Product removed from cart"
        else:
            cart.update_total_price()
            message = "Product quantity decreased"
            
        return Response({"message": message, "quantity": cart_product.quantity if cart_product.quantity > 0 else 0, "totalPrice": cart.totalPrice})
    
    @action(methods=["post"], detail=False)
    def remove(self, request):
        user_email = request.data.get('user')
        product_id = request.data.get('product')
        
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, email=user_email)
        
        cart = get_object_or_404(Cart, user=user)
        cart_product = get_object_or_404(CartProduct, product=product, cart=cart)
        
        # Update the stock of the product
        product.stock += cart_product.quantity
        product.save()
        
        cart_product.delete()
        cart.update_total_price()
        
        return Response({"message": "Product removed from cart", "totalPrice": cart.totalPrice})
    
    
    @action(methods=["POST"], detail=False)
    def checkout(self, request):
        user_email = request.data.get('user')
        
        if not user_email:
            return Response({"error": "User email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, email=user_email)
        cart = get_object_or_404(Cart, user=user)
        cart_products = CartProduct.objects.filter(cart=cart)
        
        if not cart_products.exists():
            return Response({"error": "No products in cart"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cal sum price
        sum_price = cart_products.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or Decimal(0)
        
        # Cal discount
        promotions = Promotion.objects.all()
        best_promotion = None
        best_total = sum_price
        savings = Decimal(0)
        
        for promotion in promotions:
            if promotion.enable_code():
                if promotion.discount > 10 and sum_price >= 1000:
                    total_with_discount = sum_price * (1 - Decimal(promotion.discount / 100))
                    if total_with_discount < best_total:
                        best_total = total_with_discount
                        best_promotion = promotion
                
                elif promotion.discount <= 10 and sum_price < 1000:
                    total_with_discount = sum_price * (1 - Decimal(promotion.discount / 100))
                    if total_with_discount < best_total:
                        best_total = total_with_discount
                        best_promotion = promotion
                
                savings = sum_price - best_total
        
        # สร้าง Order
        order = Order.objects.create(
            customer=user,
            promotion=best_promotion,
            quantity=cart_products.count(),
            totalPrice=best_total,
            date=timezone.now()
        )
        
        for cart_product in cart_products:
            order.product.add(cart_product.product)
            cart_product.delete()
        
        cart.update_total_price()  # อัปเดต totalPrice ของ cart
        
        return Response({"message": "Order placed successfully", "totalPrice": best_total}, status=status.HTTP_201_CREATED)
        
        

class ShowCartViewSet(viewsets.ModelViewSet):
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    @action(methods=["POST"], detail=False)
    def show_detal_cart(self, request):
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart = Cart.objects.filter(user=user)
        if not cart:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart = cart.first()
        cart_products = CartProduct.objects.filter(cart=cart)
        
        # Cal sum price
        sum_price = cart_products.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or Decimal(0)
        
        # Cal discount
        promotions = Promotion.objects.all()
        # print(promotions)
        best_promotion = None
        best_total = sum_price
        savings = Decimal(0)
        
        for promotion in promotions:
            if promotion.enable_code():
                # 15% more than 1000
                if promotion.discount > 10 and sum_price >= 1000:
                    total_with_discount = sum_price * (1 - Decimal(promotion.discount / 100))
                    best_promotion = promotion
                    best_total = total_with_discount
                
                # 10% less than 1000
                if promotion.discount <= 10 and sum_price < 1000:
                    total_with_discount = sum_price * (1 - Decimal(promotion.discount / 100))
                    best_promotion = promotion
                    best_total = total_with_discount

                savings = sum_price - best_total
            
            else:
                best_promotion = None
                best_total = sum_price
                savings = Decimal(0)
        
        
        savings = savings.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        serializer = self.get_serializer(cart)
        response_data = {
            "cart": [serializer.data],  # Wrap cart data in an array
            "sum_price": sum_price,
            "savings": round(savings, 2),
            "total": round(best_total, 2),
            "promotion": best_promotion.name if best_promotion else "No promotion applied"
        }
        
        return Response(response_data)
    
    
    

        
        
    
    
    # queryset = Cart.objects.all()
    # serializer_class = CartSerializer

    # @action(methods=["POST"], detail=False)
    # def show_detal_cart(self, request):
    #     user_id = request.data.get('user_id')
        
    #     if not user_id:
    #         return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         user = User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    #     carts = Cart.objects.filter(user=user)
    #     serializer = self.get_serializer(carts, many=True)
        
    #     return Response(serializer.data)