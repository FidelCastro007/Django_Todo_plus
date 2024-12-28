from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e18v7-sa^r+@-0g7*r6gjn8@g_i&*m_0tdgwz*2qv9366xbqz0'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',  # Add your app here
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CorsMiddleware for CORS handling
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF middleware should stay here
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_COOKIE_SAMESITE = 'None'  # Or 'Strict' if appropriate
CSRF_COOKIE_HTTPONLY = True  # Helps with security
# CSRF and CORS (if needed)

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

# Enable cookies
SESSION_COOKIE_SECURE = False  # Set True for HTTPS
CSRF_COOKIE_SECURE = False

ROOT_URLCONF = 'todo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'todo_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'todo_db',  # Your MySQL database name
        'USER': 'admin1',  # Your MySQL username
        'PASSWORD': 'admin123',  # Your MySQL password
        'HOST': '127.0.0.1',  # or 'localhost'
        'PORT': '3306',  # Default MySQL port
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'todo.CustomUser'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
LOGIN_URL = '/api/login/'  # Update to your login API endpoint


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Frontend origin
]

DEBUG = False

CORS_ALLOW_CREDENTIALS = True
