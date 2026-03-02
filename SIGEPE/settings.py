"""
Django settings for SIGEPE project.
"""

import os
from pathlib import Path
import sys
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env se existir
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Adicionar a pasta 'apps' ao sys.path
sys.path.insert(0, str(BASE_DIR / 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'troque-esta-chave-em-producao')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Adicione aqui o(s) domínio(s) ou IP(s) do seu servidor
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost, 192.168.1.131,*').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    # Apps do projeto
    'apps.main.apps.MainConfig',
    'apps.autenticacao.apps.AutenticacaoConfig',
    'apps.recepcao.apps.RecepcaoConfig',
    'apps.gabinetes.apps.GabinetesConfig',
    'apps.veiculos.apps.VeiculosConfig',
    'apps.relatorios',
    'crispy_forms',
    'crispy_bootstrap5',
]

# Configuração para arquivos estáticos: usar WhiteNoise em produção
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SIGEPE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'SIGEPE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = False
USE_TZ = True

DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = 'd/m/Y H:i:s'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging
# Em desenvolvimento (DEBUG=True): mantém console + rotação de arquivo e nível mais verboso
# Em produção (DEBUG=False): remove console, usa rotação com delay e níveis mais contidos
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'rotating_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'info.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'delay': True,
        },
        'service_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'service.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'delay': True,
        },
        'audit_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'audit.log'),
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'verbose',
            'delay': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'rotating_info'] if DEBUG else ['rotating_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.recepcao': {
            'handlers': ['console', 'rotating_info'] if DEBUG else ['rotating_info'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        # Logs do servidor (runserver/ASGI/WSGI)
        'django.server': {
            'handlers': ['console', 'service_file'] if DEBUG else ['service_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Se estiver usando gunicorn em produção, capta erros e acessos
        'gunicorn.error': {
            'handlers': ['console', 'service_file'] if DEBUG else ['service_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console', 'service_file'] if DEBUG else ['service_file'],
            'level': 'WARNING' if not DEBUG else 'INFO',
            'propagate': False,
        },
        'audit': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Certifica que o diretório de logs existe
logs_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(logs_dir, exist_ok=True)

# SMTP (exemplo, revise para seu provedor)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.seuprovedor.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'usuario@dominio.com'
# EMAIL_HOST_PASSWORD = 'sua_senha'
# EMAIL_USE_TLS = True

# Outras opções de segurança recomendadas para produção:
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#X_FRAME_OPTIONS = 'DENY'

# Configurações de segurança
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin settings
ADMIN_URL = 'admin/'
LOGIN_URL = 'autenticacao:login_sistema'
LOGIN_REDIRECT_URL = 'recepcao:home_sistema'
LOGOUT_REDIRECT_URL = 'autenticacao:login_sistema'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# =====================
# Configurações customizadas de imagens, cache e upload (vindas de config/settings.py)
# =====================

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Media files configuration (já existe, mas mantido para referência)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum upload size (5MB)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Allowed image types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']

# Image sizes configuration
IMAGE_SIZES = {
    'thumbnail': (100, 100),
    'medium': (300, 300),
    'large': (800, 800)
}

# Image quality settings
IMAGE_QUALITY = {
    'thumbnail': 75,
    'medium': 85,
    'large': 90
}
