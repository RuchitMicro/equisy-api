"""
Django settings for equisy_api project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z-7y@+gos+2rct1@p#)$*nx=*^nohi&^abcwi0$u_e05ya!3ls'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
SHARED_APPS = (
    'django_tenants', # mandatory
    'web', # you must list the app where your tenant model resides in

    'django.contrib.postgres',

    # everything below here is optional
    'django.contrib.admin',
    'django.contrib.auth', # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes', # Defined in both shared apps and tenant apps
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
	'tenant_users.tenants', # defined only in shared apps
    
    'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

    'users', # Custom app that contains the new User Model (see below). Must NOT exist in TENANT_APPS

    'django_cleanup.apps.CleanupConfig',
    'admin_reorder',
    'tinymce',
    'jsoneditor',
)

TENANT_APPS = (
	# The following Django contrib apps must be in TENANT_APPS
	'django.contrib.contenttypes',

	'django.contrib.postgres',
	# everything below here is optional
	'django.contrib.admin',
	'django.contrib.auth', # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes', # Defined in both shared apps and tenant apps
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# your tenant-specific apps
	'tenant',
)

INSTALLED_APPS      =   list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_USERS_DOMAIN 	=   "localhost"
TENANT_MODEL            =   "web.Startup"
TENANT_DOMAIN_MODEL     =   "web.Domain"

AUTH_USER_MODEL 		= 'users.TenantUser'

AUTHENTICATION_BACKENDS = (
    "tenant_users.permissions.backend.UserBackend",
)

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF            = 'equisy_api.urls'
PUBLIC_SCHEMA_URLCONF 	= 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'equisy_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Refer to settings_dev.py & settings_prod.py for database settings
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

import os
STATIC_URL = 'static/'
STATIC_URL          =   '/static/'
STATICFILES_DIRS    =   [
    os.path.join(BASE_DIR, 'web/static'),
]
STATIC_ROOT =   os.path.join(BASE_DIR, 'static')
MEDIA_URL   =   '/media/'
MEDIA_ROOT  =   os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Azure Key Vault Settings
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

key_vault_url   = "https://<your-key-vault-name>.vault.azure.net/"
credential      = DefaultAzureCredential()
client          = SecretClient(vault_url=key_vault_url, credential=credential)

def get_secret(secret_name):
    return client.get_secret(secret_name).value

# # Example usage
# SECRET_KEY = get_secret("django-secret-key")
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': get_secret("db-name"),
#         'USER': get_secret("db-user"),
#         'PASSWORD': get_secret("db-password"),
#         'HOST': get_secret("db-host"),
#         'PORT': get_secret("db-port"),
#     }
# }




