from rest_framework import serializers
from api.models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer (JSON) for tasks"""
    class Meta:
        model = Task
        fields = "__all__"