from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from .models import CustomUser, Task
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# Register a new user
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        user = CustomUser.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User registered successfully'})

# Login a user
@csrf_protect  # Ensure CSRF protection
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=401)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Logout a user
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Get tasks
@login_required
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    task_list = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
    return JsonResponse({'tasks': task_list})

# Add a task
@csrf_exempt
@login_required
def add_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        task = Task.objects.create(user=request.user, title=title, description=description)
        return JsonResponse({'message': 'Task added', 'task': {'id': task.id, 'title': task.title, 'description': task.description}})

# Edit a task
@csrf_exempt
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.save()
        return JsonResponse({'message': 'Task updated'})

# Delete a task
@csrf_exempt
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted'})
