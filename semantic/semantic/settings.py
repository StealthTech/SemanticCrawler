import os

from utils.config import Configuration


conf = Configuration('project.conf', markdown='main')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = conf.get('PREDEFINED', 'secret_key')

DEBUG = conf.get('PREDEFINED', 'debug', 'bool')

ALLOWED_HOSTS = conf.get('DEPLOY', 'allowed_hosts', 'csv')

EMAIL_ENABLED = conf.get('EMAIL', 'enabled', 'bool')

if EMAIL_ENABLED:
    EMAIL_USE_TLS = conf.get('EMAIL', 'use_tls', 'bool')
    EMAIL_HOST = conf.get('EMAIL', 'host')
    EMAIL_HOST_USER = conf.get('EMAIL', 'host_user')
    EMAIL_HOST_PASSWORD = conf.get('EMAIL', 'host_password')
    EMAIL_PORT = conf.get('EMAIL', 'port')
    DEFAULT_FROM_EMAIL = conf.get('EMAIL', 'default_from')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'semantic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

WSGI_APPLICATION = 'semantic.wsgi.application'

DATABASES = {}

if conf.get('DATABASES', 'storage') == 'mysql':
    DATABASES['default'] = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': conf.get('MYSQL', 'name'),
            'USER': conf.get('MYSQL', 'user'),
            'PASSWORD': conf.get('MYSQL', 'password'),
            'HOST': conf.get('MYSQL', 'tcp_addr'),
            'PORT': conf.get('MYSQL', 'tcp_port'),
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=INNODB,'
                                'character_set_connection=utf8,collation_connection=utf8_unicode_ci',
                'charset': 'utf8'
            }
        }
else:
    DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }

AUTH_USER_MODEL = 'core.User'

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

CACHE_ENABLED = conf.get('REDIS', 'enabled', 'bool')

if CACHE_ENABLED:
    redis_connection_type = conf.get('REDIS', 'connection_type')
    if  redis_connection_type == 'socket':
        cache_location = conf.get('REDIS', 'socket_location')
    elif redis_connection_type == 'tcp':
        cache_location = 'redis://{}:{}'.format(
            conf.get('REDIS', 'tcp_addr'),
            conf.get('REDIS', 'tcp_port')
        )
    else:
        cache_location = None

    if cache_location:
        CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': cache_location
            }
        }
        SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

static_root_checker = conf.get('DEPLOY', 'static_root')
if static_root_checker:
    STATIC_ROOT = os.path.join(PROJECT_ROOT, static_root_checker)
else:
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')

MEDIA_URL = '/uploads/'

AVATAR_MAX_HEIGHT = conf.get('PICTURES', 'avatar_max_height', 'int')

AVATAR_MAX_WIDTH = conf.get('PICTURES', 'avatar_max_width', 'int')

PIC_MAX_HEIGHT = conf.get('PICTURES', 'pic_max_height', 'int')

PIC_MAX_WIDTH = conf.get('PICTURES', 'pic_max_width', 'int')
