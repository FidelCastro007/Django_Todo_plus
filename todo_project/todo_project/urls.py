from django.urls import path, include
from todo.views import LoginView  # Import the LoginView class-based view

urlpatterns = [
    path('api/', include('todo.urls')),  # Include API-related routes
    path('accounts/login/', LoginView.as_view(), name='login'),  # Use LoginView class here
]
