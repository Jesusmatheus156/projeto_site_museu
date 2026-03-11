from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-##4_j_p91fei^%6hy5g@m47e-406-f^&mo)-ru(fw&@39et7mr')

DEBUG = True

ALLOWED_HOSTS = [
    'museuindigenaluizacantofa.org.br', 
    'www.museuindigenaluizacantofa.org.br', 
    '72.61.54.114', 
    'localhost', 
    '127.0.0.1'
]

LOGIN_URL = '/admin'  

CSRF_TRUSTED_ORIGINS = [
    'https://museuindigenaluizacantofa.org.br',
    'https://www.museuindigenaluizacantofa.org.br',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projeto_museu.urls'

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

WSGI_APPLICATION = 'projeto_museu.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

# Definir os idiomas suportados
LANGUAGES = [
    ('pt-br', _('Português')),
    ('en', _('English')),
    ('es', _('Español')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'

MEDIA_ROOT = '/var/www/museu/media'

CKEDITOR_UPLOAD_PATH = 'uploads/' # Onde o CKEditor salvará as imagens internas

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

IGNORE_PATTERNS = [
    'requirements.txt',
    '*.pyc',
    '*.mo',
    '*.svn',
    'CVS',
    '.DS_Store',
]


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "base" / "static",
]

STATIC_ROOT = '/var/www/museu/static_root'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'
