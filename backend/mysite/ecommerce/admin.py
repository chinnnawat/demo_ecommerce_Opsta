from django.contrib import admin
from .models import Product, Cart, Promotion, Category, Order, CartProduct

# Product
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Promotion)
admin.site.register(Order)

