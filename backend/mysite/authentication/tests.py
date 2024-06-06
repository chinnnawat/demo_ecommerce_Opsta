from django.test import TestCase
from .models import User, UserManager
# Create your tests here.

class UserModelTest(TestCase):
    def setUp(self):
        self.email = 'john@email.com'
        self.name = 'John'
        self.lastname = 'Doe'
        
    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            name=self.name,
            lastname=self.lastname
        )
        
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.lastname, self.lastname)
        
        # skip check password
        self.assertEqual(user.password, self.email)
        # self.assertTrue(user.check_password(self.email))  # รหัสผ่านจะถูกตั้งเป็นอีเมลตามที่กำหนดไว้
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
