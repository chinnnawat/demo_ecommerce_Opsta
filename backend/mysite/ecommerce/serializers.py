from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True) => show id
    category = serializers.StringRelatedField() # show name
    class Meta:
        model = Product
        fields = '__all__'