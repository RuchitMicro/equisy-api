from .settings import *


# SECURITY WARNING: don't run with debug turned on in production! Production settings are mentioned in settings_prod.py
DEBUG           = True

ALLOWED_HOSTS   = ['*']

# MIDDLEWARE
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# INSTALLED APPS
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

# DEBUG TOOLBAR INTERNAL IPS
INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
]

# Database
DATABASES = {
    'default': {
        'ENGINE'    :   'django_tenants.postgresql_backend',
        'NAME'      :   'equisy-test',                      # Your database name
        'USER'      :   'postgres',                         # Your database user
        'PASSWORD'  :   'postgres',                         # Your database password
        'HOST'      :   'localhost',                        # Your database host
        'PORT'      :   '5432',                             # Your database port
    }
}

# Django Tenant User
TENANT_USERS_DOMAIN 	=   "localhost"






