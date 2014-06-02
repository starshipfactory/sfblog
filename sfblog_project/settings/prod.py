from .base import *  # NOQA
from os import environ

environ.setdefault('SFBLOG_CONFIG_PATH', '/etc/sfblog')

ALLOWED_HOSTS = [
		"blog.starship-factory.ch",
		"blog.starship-factory.com",
		"blog.starship-factory.de",
		"blog.starship-factory.eu",
		"blog.starship-factory.org",
		"blog.starshipfactory.ch",
		"blog.starshipfactory.de",
		"blog.starshipfactory.eu",
		"blog.starshipfactory.org",
		"starship-factory.ch",
		"starship-factory.com",
		"starship-factory.de",
		"starship-factory.eu",
		"starship-factory.org",
		"starshipfactory.ch",
		"starshipfactory.de",
		"starshipfactory.eu",
		"starshipfactory.org",
		"www.starship-factory.ch",
		"www.starship-factory.com",
		"www.starship-factory.de",
		"www.starship-factory.eu",
		"www.starship-factory.org",
		"www.starshipfactory.ch",
		"www.starshipfactory.de",
		"www.starshipfactory.eu",
		"www.starshipfactory.org",
		]

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
