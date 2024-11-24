from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Model to represent a task in the to-do list.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    password = models.CharField(max_length=255)  # Add a password field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def _str_(self):
        return self.title