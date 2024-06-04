from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4

# Create your models here.

# user Model on Google
class CustomeerModelManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        # create customer
        user= self.model(
            username = username,
            email = self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using = self._db)
        
        return user


class CustomerUserModel(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(max_length=16, default=uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=16, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customer_users'  # New argument
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customer_users'  # New argument
    )
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    active = models.BooleanField(default=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomeerModelManager()
    
    class Meta:
        verbose_name = "Customer User"