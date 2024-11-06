from rest_framework import serializers
from .models import UserRequest

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ['user_id', 'user_name', 'service_category', 'product_code']
