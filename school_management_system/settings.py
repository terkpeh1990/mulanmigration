import os
from pathlib import Path
from twilio.http.http_client import TwilioHttpClient
import markdown
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [ '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bankapi.apps.BankapiConfig',
    'crispy_forms',
    'school.apps.SchoolConfig',
    'bakery.apps.BakeryConfig',
    'partytree.apps.PartytreeConfig',
    'salon.apps.SalonConfig',
    'accounts.apps.AccountsConfig',
    'simple_history',
    'corsheaders',
    'drf_yasg',
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
    'crum.CurrentRequestUserMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]


ROOT_URLCONF = config('ROOT_URLCONF')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'school_management_system.wsgi.application'

FIXTURE_DIRS = [
    'fixtures',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        

    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'school_management_system.paginator.CustomPagination',
    "DEFAULT_GENERATOR_CLASS": "rest_framework.schemas.generators.BaseSchemaGenerator",


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = config('LOGIN_URL')
LOGOUT_URL = config('LOGIN_URL')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
CRISPY_TEMPLATE_PACK = 'bootstrap4'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DJANGORESIZED_DEFAULT_SIZE = [128, 128]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

#Bakes
TWILIO_ACCOUNT_SID2 = config('TWILIO_ACCOUNT_SID2')
TWILIO_AUTH_TOKEN2 = config('TWILIO_AUTH_TOKEN2')
TWILIO_PHONE_NUMBER2 = config('TWILIO_PHONE_NUMBER2')


#partytree
TWILIO_ACCOUNT_SID3 = config('TWILIO_ACCOUNT_SID3')
TWILIO_AUTH_TOKEN3 = config('TWILIO_AUTH_TOKEN3')
TWILIO_PHONE_NUMBER3 = config('TWILIO_PHONE_NUMBER3')

#irish
TWILIO_ACCOUNT_SID4 = config('TWILIO_ACCOUNT_SID4')
TWILIO_AUTH_TOKEN4 = config('TWILIO_AUTH_TOKEN4')
TWILIO_PHONE_NUMBER4 = config('TWILIO_PHONE_NUMBER4')


endPoint = config('endPoint')
apiKey = config('apiKey')
bakes_sender_id = config('bakes_sender_id')
partytree_sender_id = config('partytree_sender_id')
mulan_sender_id = config('mulan_sender_id')

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)



SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },

}

REDOC_SETTINGS = {
  'LAZY_RENDERING': False,

}

CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = config('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = config('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = config('CELERY_RESULT_SERIALIZER')
CELERY_TIMEZONE = config('CELERY_TIMEZONE')
print('Markdown module path', markdown.__file__)
print('Markdown version:', markdown.version)