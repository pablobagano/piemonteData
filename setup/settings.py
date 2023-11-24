"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import pymysql
from django.db import DatabaseError, connections
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential
import tempfile

pymysql.install_as_MySQLdb()
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG','False') == 'True'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'piemonteData.apps.PiemontedataConfig'
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

ROOT_URLCONF = 'setup.urls'

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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

try:
    conn_string = str(os.getenv('CONN_STRING_DB'))
    blob_url = str(os.getenv('BLOB_URL'))
    blob_client = BlobClient.from_connection_string(
        conn_string,
        container_name = str(os.getenv('CONTAINER_NAME')),
        blob_name = str(os.getenv('BLOB_NAME')) 
    )
    blob_stream = blob_client.download_blob()
    blob_data = blob_stream.readall()
except Exception as e:
    print(f"{type(e).__name__}:{e}")
try:
    temp_cert_file = tempfile.NamedTemporaryFile(delete=False)
    temp_cert_file.write(blob_data)
    temp_cert_path = temp_cert_file.name
    temp_cert_file.close()
    print(f"Blob data successfully fetched and written to {temp_cert_path}")
except Exception as e:
    print(f"{type(e).__name__}:{e}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': str(os.getenv('DB_NAME')),
        'USER' : str(os.getenv('DB_USER')),
        'PASSWORD' : str(os.getenv('DB_PASSWORD')), 
        'HOST' : str(os.getenv('DB_HOST')), 
        'PORT': '3306',
        'OPTIONS':{
            'ssl':{
                'ca':temp_cert_path
            }
        }
    }
}

try:
    connections['default'].ensure_connection()
    print("Login successfull")
except DatabaseError as db_err:
    print(f"DatabaseError: {db_err}")

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

