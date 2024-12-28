from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .models import Task
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .serializers import TaskSerializer

# Register View
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Validate input
            if not username or not password or not email:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email address'}, status=400)
            
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            CustomUser.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'message': 'User registered successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Login View
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful', 'token': token.key})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
# Logout View
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def api_response(success, data=None, message=None, status=200):
    return JsonResponse({'success': success, 'data': data, 'message': message}, status=status)

# Get All Tasks
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    try:
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return api_response(True, data=serializer.data)
    except Exception as e:
        return api_response(False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Add a Task
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_task(request):
    try:
        data = request.data
        title = data.get('title')
        description = data.get('description')

        if not title:
            return api_response(False, message="Title is required", status_code=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(user=request.user, title=title, description=description)
        return api_response(True, data={'id': task.id, 'title': task.title, 'description': task.description}, message="Task added")
    except Exception as e:
        return api_response(False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

# Edit a Task
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        data = request.data
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.save()
        return api_response(True, message="Task updated")
    except Task.DoesNotExist:
        return api_response(False, message="Task not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return api_response(False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

# Delete a Task
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return api_response(True, message="Task deleted")
    except Task.DoesNotExist:
        return api_response(False, message="Task not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return api_response(False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
