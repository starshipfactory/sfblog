# Julianes settings
from .dev import *

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'sfblog',
        'USER': 'sfblog',
        'PASSWORD': 'test',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

