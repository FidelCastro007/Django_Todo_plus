from django.urls import path, include
from todo.views import login_view  # Ensure this path is correct

urlpatterns = [
    path('api/', include('todo.urls')),  # Include API-related routes
    # path('accounts/login/', login_view, name='login'),  # Login endpoint
]
