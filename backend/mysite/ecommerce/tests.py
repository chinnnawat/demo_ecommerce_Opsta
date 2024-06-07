from django.test import TestCase
from .models import Category, Product, Promotion, Cart, CartProduct
from django.utils import timezone
from freezegun import freeze_time
import datetime
from datetime import timedelta
from authentication.models import User, MyUserManager
from django.urls import reverse


class CategoryTestCase(TestCase):
    # Create Category
    def setUp(self):
        self.category1 = Category.objects.create(category = 'Electronics') # id = 1
        self.category2 = Category.objects.create(category = 'Automotive') # id =2
    
    def test_category_creation_electronic(self):
        category = Category.objects.get(id=self.category1.id)
        self.assertEqual(category.category, "Electronics")
    
    def test_category_creation_automotion(self):
        category = Category.objects.get(id=self.category2.id)
        self.assertEqual(category.category, "Automotive")
    
    def test_unique_id(self):
        self.assertNotEqual(self.category1.id, self.category2.id)
        
# Product
class ProductTestCase(TestCase):
    # Create Product
    @freeze_time("2024-05-30 14:00:00")
    def setUp(self):
        self.category = Category.objects.create(category = "Electronics")
        
        self.product = Product.objects.create(
            name = "Laptop",
            description = "Laptops are designed to be portable computers. They are smaller and lighter than desktops. The name connotes the user's ability to put the computer in their lap while they use it. Laptops have rechargeable batteries that can be used for a set period away from a power source.",
            price = 99,
            stock = 10,
            category = self.category,
            imageUrl = "www.google.com"
        )
    @freeze_time("2024-05-30 14:00:00")
    def test_product_create(self):
        self.assertIsNotNone(self.product.id)
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.description, "Laptops are designed to be portable computers. They are smaller and lighter than desktops. The name connotes the user's ability to put the computer in their lap while they use it. Laptops have rechargeable batteries that can be used for a set period away from a power source.")
        self.assertEqual(self.product.price, 99)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.imageUrl, "www.google.com")
        self.assertEqual(self.product.category, self.category)
        assert datetime.datetime.now() == datetime.datetime(2024,5,30,14,00,00)
    
    # Update Product
    @freeze_time("2024-06-30 14:00:00")
    def test_product_update(self):
        self.product.name = "Update Laptop"
        self.product.price = 50
        self.product.stock = 100
        self.category.category = "Desktop PC"
        self.product.save()
        self.product.refresh_from_db()
        assert datetime.datetime.now() == datetime.datetime(2024,6,30,14,00,00)


# Promotion
class PromotionTestCase(TestCase):
    # cal (+)
    def test_promotion_cal_end_date_positive(self):
        startDate = timezone.now()
        promotion = Promotion(start_date = startDate, during_date = 5)
        promotion.cal_end_date()
        expectEndDate = startDate + timedelta(days=5)
        
        self.assertEqual(promotion.end_date, expectEndDate)
        
        
    # cal (-)
    def test_promotion_cal_end_date_nagative(self):
        startDate = timezone.now()
        promotion = Promotion(start_date = startDate, during_date = -5)
        promotion.cal_end_date()
        expectEndDate = startDate + timedelta(days = promotion.during_date)
        
        self.assertEqual(promotion.end_date, expectEndDate)
    
    # gen code 
    def test_promotion_gen_code(self):
        promotion = Promotion()
        promotion.gen_code()
        print(promotion.code)
        self.assertIsNotNone(promotion.code)
        
    # enableCode?
    def test_promotion_enable_code(self):
        startDate = timezone.now() - timedelta(3)
        endDate = timezone.now() + timedelta(3)
        promotion = Promotion(start_date = startDate, end_date = endDate)
        self.assertIs(promotion.enable_code(), True)
        
    # disableCode
    def test_promotion_disable_code(self):
        startDate = timezone.now() - timedelta(3)
        endDate = timezone.now() - timedelta(3)
        promotion = Promotion(start_date = startDate, end_date = endDate)
        self.assertIs(promotion.enable_code(), False)
        
    # save
    def test_promotion_save(self):
        startDate = timezone.now()
        promotion = Promotion(start_date = startDate, during_date = 5, discount=10)
        promotion.save()
        # code
        self.assertIsNotNone(promotion.code, True)
        expectEndDate = startDate + timedelta(days=5)
        # end date
        self.assertEqual(expectEndDate, promotion.end_date)
        
# Cart
class CartTestCase(TestCase):
    # setUp
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test', lastname='User')
        self.category = Category.objects.create(category='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Test description', price=10.0, category=self.category)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_product = CartProduct.objects.create(product=self.product, cart=self.cart, quantity=1)
        
    def test_cart_creation(self):
        self.assertIsNotNone(self.cart.id)
        self.assertEqual(self.cart.id, 1)
        self.assertEqual(self.user.id, self.cart.user.id)
        
    def test_cart_product_quantity_increase(self):
        self.client.force_login(self.user)
        quantity = self.cart_product.quantity
        
        # add_to_cart => function name in views.py
        # add prodct +1
        # response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        
        update_cart_product = CartProduct.objects.get(id=self.cart_product.id)
        self.assertEqual(update_cart_product.quantity +1 , quantity+1)


        
        
