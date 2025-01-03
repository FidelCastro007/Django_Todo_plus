from rest_framework import serializers
from .models import Task  # Assuming you have a Task model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = ['id','user', 'title', 'description','completed']  # Explicitly include fields you need
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        # Add more claims if required
        if hasattr(user, 'profile'):  # Assuming a Profile model linked to User
            token['full_name'] = user.profile.full_name
            token['verified'] = user.profile.verified

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Custom response with user details
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
        }

        return data
