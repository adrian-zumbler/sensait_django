"""
Django settings for ardsensor project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'djzfi+pmw9mw7%#p(#ht_ul@#b8#(ue+*&iv5ufi(y+^spp*)h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'client',
    'corsheaders',
    'bootstrapform',
    'markdown_deux',
    'helpdesk',
    'arduino',
    'ticket',
    'dashboard',
    'widget_tweaks',
    'ws4redis',
    'channels',
    'utils',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = '/logins/'

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'ardsensor.urls'

WEBSOCKET_URL = '/ws/'

WS4REDIS_EXPIRE = 7200

WSGI_APPLICATION = 'ws4redis.django_runserver.application'

#WSGI_APPLICATION = 'ardsensor.wsgi.application'

WS4REDIS_ALLOWED_CHANNELS = 'arduino.channels.get_allowed_channels'

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_PREFIX = 'session'

CHANNEL_LAYERS = {
    "default": {
        #"BACKEND": "asgiref.inmemory.ChannelLayer",
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "ardsensor.routing.channel_routing",
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.media",
                'django.core.context_processors.static',
                'ws4redis.context_processors.default',
            ],
        },
    },
]


EMAIL_HOST = 'mail.sensait.com'

EMAIL_PORT = 465

EMAIL_HOST_USER = 'alertas@sensait.com'

EMAIL_HOST_PASSWORD = 'Y4bfaJ^P'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_USE_TLS = True

EMAIL_USE_SSL = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # '/home/jose/dev/corpbit/ardsensor/static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')  # '/home/jose/dev/corpbit/ardsensor/static/media'

if 'manto' in BASE_DIR:
    WS4REDIS_CONNECTION = {
        'host': '192.168.253.32',
        'port': 6379,
        'db': 0,
        'password': None,
    }

    CHANNEL_LAYERS = {
        "default": {
            # "BACKEND": "asgiref.inmemory.ChannelLayer",
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("192.168.253.32", 6379)],
            },
            "ROUTING": "ardsensor.routing.channel_routing",
        },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'sensait',
            'USER': 'sensait_user',
            'PASSWORD': 'yG6$Pz2&',
            'HOST': '192.168.253.32',
            'PORT': '',
        }
    }

    STATIC_ROOT = os.path.join(BASE_DIR, '../static/')

    MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')

    DEBUG = True

    ALLOWED_HOSTS = ['sensait.dyndns.org', '192.168.253.31']

    SESSION_REDIS_HOST = '192.168.253.32'

