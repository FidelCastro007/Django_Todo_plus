from .models import Task
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class CSRFTokenView(APIView):
    permission_classes = [AllowAny]  # This allows anyone to access the registration endpoint
    def get(self, request):
        csrf_token = get_token(request)
        print(csrf_token)  # Debugging: Check if CSRF token is present
        return JsonResponse({'csrfToken': csrf_token})
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]  # This allows anyone to access the registration endpoint
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

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

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                # Generate JWT token for the authenticated user
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return JsonResponse({
                    'message': 'Login successful',
                    'access_token': str(access_token),
                    'refresh_token': str(refresh)
                })
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class LogoutView(APIView):
    permission_classes = [AllowAny]  # This allows anyone to access the registration endpoint
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})


class TaskListView(APIView):
    authentication_classes = [JWTAuthentication]  # Use only JWTAuthentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return JsonResponse({'tasks': serializer.data, 'JWT Token': get_token(request)}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AddTaskView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]  # Use only JWTAuthentication
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def post(self, request):
        try:
            data = request.data
            title = data.get('title')
            description = data.get('description')

            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            task = Task.objects.create(user=request.user, title=title, description=description)
            return JsonResponse({
                'message': 'Task added',
                'data': {'id': task.id, 'title': task.title, 'description': task.description}
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class EditTaskView(APIView):
    authentication_classes = [JWTAuthentication]  # Use only JWTAuthentication
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            data = request.data
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.save()
            return JsonResponse({'message': 'Task updated'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class DeleteTaskView(APIView):
    authentication_classes = [JWTAuthentication]  # Use only JWTAuthentication
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'message': 'Task deleted'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class CompleteTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.completed = True
            task.save()
            return JsonResponse({'message': 'Task marked as complete'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
