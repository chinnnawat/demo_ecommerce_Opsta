# from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product



class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True) => show id
    category = serializers.StringRelatedField() # show name
    class Meta:
        model = Product
        fields = '__all__'