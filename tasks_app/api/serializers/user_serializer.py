from rest_framework import serializers
from api.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["password"]