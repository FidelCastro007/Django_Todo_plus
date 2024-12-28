from django.urls import path
from .views import register_view, login_view, logout_view, get_tasks, add_task, edit_task, delete_task,api_response
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tasks/', get_tasks, name='get_tasks'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('status/', api_response, name='api_status'),  # New API status endpoint
]
