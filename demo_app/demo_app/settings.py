from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

SECRET_KEY = 'django-insecure-&ye_*si1htd3#_d#i(+7x2bcp_p$@_1b-ugz$g4*@z=iy^3opw'

DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'middleware.ErrorMiddleware',
]

ROOT_URLCONF = 'demo_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo_app.wsgi.application'


DATABASES = {}
AUTH_PASSWORD_VALIDATORS = []



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
