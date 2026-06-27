from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-wrd@k5c63l-25ln)85jwma^uf$he_n077de(m!-(rhiu5#*d+q')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'core',
    'usuarios',
    'productos',
    'catalogo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SecurityHeadersMiddleware',
]

ROOT_URLCONF = 'dcrm.urls'

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

WSGI_APPLICATION = 'dcrm.wsgi.application'

# --- Database: SQLite por defecto, MySQL si está configurado ---
_requested_engine = os.environ.get('DJANGO_DB_ENGINE', 'sqlite').lower()

if 'mysql' in _requested_engine:
    try:
        import MySQLdb
        _engine = 'django.db.backends.mysql'
    except ImportError:
        import warnings
        warnings.warn("mysqlclient no está instalado. Usando SQLite como fallback.")
        _engine = 'django.db.backends.sqlite3'
else:
    _engine = 'django.db.backends.sqlite3'

_is_sqlite = 'sqlite' in _engine

DATABASES = {
    'default': {
        'ENGINE': _engine,
        'NAME': os.environ.get('DJANGO_DB_PATH' if _is_sqlite else 'DJANGO_DB_NAME',
                               str(BASE_DIR / 'db.sqlite3') if _is_sqlite else 'dcrm'),
        'USER': os.environ.get('DJANGO_DB_USER', 'dcrm_user'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'DcrmPass2026!'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DB_PORT', '3306'),
    }
}

if not _is_sqlite:
    DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}
# -----------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login/'

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'website', 'templates', 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
