import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ATD_DIR = '/home/itakaesu/PycharmProjects/Adversarial-Threat-Detector/'
GYOITHON_DIR = '/home/itakaesu/PycharmProjects/GyoiThon/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DUMMY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowable hosts.
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'atd.apps.AtdConfig',
    'gyoithon.apps.GyoithonConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    'bootstrap4',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'corsheaders',
]

CELERY_TASK_TRACK_STARTED = True

CELERY_RESULT_BACKEND = 'django-db'

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Authentication Type.
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# Required for django-allauth.
SITE_ID = 1

# Disable session login and enable CORS ORIGIN.
REST_SESSION_LOGIN = False
CORS_ORIGIN_ALLOW_ALL = True

# Verify email in Login.
ACCOUNT_EMAIL_VARIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# Setting for JWT.
REST_USE_JWT = True
JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': False,  # Debug.
}

# Allowable Origins.
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
)

# Setting for distribution Email.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Can be published responses.
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'gyoiboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', os.path.join(BASE_DIR, 'atd', 'reports')],
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

WSGI_APPLICATION = 'gyoiboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'atd': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ATD_DIR + 'sqlite3/scan_result.db',
    },
    'gyoithon': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': GYOITHON_DIR + 'sqlite3/scan_result.db',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
