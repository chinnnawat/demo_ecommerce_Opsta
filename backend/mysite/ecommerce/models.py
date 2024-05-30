from django.db import models
import uuid
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

# Category
class Category(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category 


# Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    imageUrl = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    


# Promotion model
class Promotion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    discount = models.IntegerField()
    start_date = models.DateTimeField()
    during_date = models.IntegerField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=50, unique=True, blank=True)

    # save
    def save(self, *args, **kwargs):
        if not self.code:
            self.gen_code()
            # super().save(*args, **kwargs)

        self.cal_end_date()
        super().save(*args, **kwargs)
            
    # cal
    def cal_end_date(self): 
        if not self.end_date:
            if(self.during_date < 0 ):
                self.during_date = self.during_date * -1
            self.end_date = self.start_date + timedelta(days=self.during_date)
        if not self.during_date:
            self.during_date = (self.end_date - self.start_date).days
            self.end_date = self.end_date
        if self.end_date and self.during_date:
            # depend on during date
            self.end_date = self.start_date + timedelta(days=self.during_date)
            
            # depend on calendar end_date
            # self.end_date = self.end_date
            # self.during_date = (self.end_date - self.start_date).days

    def gen_code(self):
        self.code = str(uuid.uuid4()).replace("-", "")[:5]
        
    # enable?
    def enable_code(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    
    
    def __str__(self):
        return self.name 

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"


# Customer
class Customer(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'
    

# Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f'Order {self.id} by {self.customer}'
    