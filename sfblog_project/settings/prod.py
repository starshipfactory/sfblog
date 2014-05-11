from .base import *  # NOQA
from os import environ

environ.setdefault('SFBLOG_CONFIG_PATH', '/etc/sfblog')

DEBUG = False

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'sfblog',
                'USER': 'sfblog',
                'PASSWORD': open(environ.get('SFBLOG_CONFIG_PATH') + '/pgpassword').read().strip(),
                'HOST': open(environ.get('SFBLOG_CONFIG_PATH') + '/pgserver').read().strip(),
                'PORT': open(environ.get('SFBLOG_CONFIG_PATH') + '/pgport').read().strip(),
        }
}
