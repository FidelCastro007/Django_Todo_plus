from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .models import Task

# Register View
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if username and password and email:
                from django.contrib.auth.models import User
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'Username already exists'}, status=400)

                User.objects.create_user(username=username, password=password, email=email)
                return JsonResponse({'message': 'User registered successfully'})
            return JsonResponse({'error': 'Invalid data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Login View
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Logout View
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Get Tasks for the Authenticated User
@login_required
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    task_list = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
    return JsonResponse({'tasks': task_list})

# Add a Task
@login_required
def add_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            task = Task.objects.create(user=request.user, title=title, description=description)
            return JsonResponse({'message': 'Task added', 'task': {'id': task.id, 'title': task.title, 'description': task.description}})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Edit a Task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.save()
            return JsonResponse({'message': 'Task updated'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Delete a Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'DELETE':
        try:
            task.delete()
            return JsonResponse({'message': 'Task deleted'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
