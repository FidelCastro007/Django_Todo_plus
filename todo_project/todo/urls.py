# from django.urls import path
# from .views import register_view, login_view, logout_view, get_tasks, add_task, edit_task, delete_task,api_response,get_csrf
# from rest_framework.authtoken.views import obtain_auth_token

# urlpatterns = [
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('tasks/', get_tasks, name='get_tasks'),
#     path('tasks/add/', add_task, name='add_task'),
#     path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
#     path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
#     #path('token/', obtain_auth_token, name='api_token_auth'),
#     path('status/', api_response, name='api_status'),  # New API status endpoint
#     path('csrf/', get_csrf, name='csrf'),
# ]

from django.urls import path
from .views import CSRFTokenView, RegisterView, LoginView, LogoutView, TaskListView, AddTaskView, EditTaskView, DeleteTaskView,MyTokenObtainPairView,CompleteTaskView

urlpatterns = [
    path('csrf/', CSRFTokenView.as_view(), name='csrf-token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # Ensure LoginView is imported here
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/add/', AddTaskView.as_view(), name='add-task'),
    path('tasks/edit/<int:task_id>/', EditTaskView.as_view(), name='edit-task'),
    path('tasks/delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete-task'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tasks/complete/<int:task_id>/', CompleteTaskView.as_view(), name='complete-task'),
]
