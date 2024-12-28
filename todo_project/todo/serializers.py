from rest_framework import serializers
from .models import Task  # Assuming you have a Task model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # Include all fields or specify the fields explicitly
