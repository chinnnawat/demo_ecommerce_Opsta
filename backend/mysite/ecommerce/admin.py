from django.contrib import admin
from .models import Product, Cart, Promotion, Category, Order

# Product
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Promotion)
admin.site.register(Order)

