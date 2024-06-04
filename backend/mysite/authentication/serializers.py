from rest_framework.serializers import ModelSerializer
from .models import CustomerUserModel
from django.conf import settings

class CustomUserModelSerializer(ModelSerializer):
  class Meta:
    model = CustomerUserModel
    fields = [
      "userId",
      "username",
      "email",
      "password",
    ]

  def create(self, validated_data):
    user = CustomerUserModel.objects.create(
      validated_data["username"],
      validated_data["email"],
      validated_data["password"]
    )

    return user