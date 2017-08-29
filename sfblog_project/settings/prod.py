from .base import *  # NOQA
import dj_database_url
import os

os.environ.setdefault('SFBLOG_CONFIG_PATH', '/etc/sfblog')

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
    "blog.hackerspace-basel.ch",
    "blog.hackerspace-basel.com",
    "blog.hackerspace-basel.net",
    "blog.hackerspace-basel.org",
    "blog.fablab-basel.ch",
    "blog.fablabbasel.ch",
    "blog.makerspace-basel.ch",
    "blog.makerspacebasel.ch",
    "starship-factory.ch",
    "starship-factory.com",
    "starship-factory.de",
    "starship-factory.eu",
    "starship-factory.org",
    "starshipfactory.ch",
    "starshipfactory.de",
    "starshipfactory.eu",
    "starshipfactory.org",
    "hackerspace-basel.ch",
    "hackerspace-basel.com",
    "hackerspace-basel.net",
    "hackerspace-basel.org",
    "fablab-basel.ch",
    "fablabbasel.ch",
    "makerspace-basel.ch",
    "makerspacebasel.ch",
    "ww.starship-factory.ch",
    "www.starship-factory.ch",
    "www.starship-factory.com",
    "www.starship-factory.de",
    "www.starship-factory.eu",
    "www.starship-factory.org",
    "www.starshipfactory.ch",
    "www.starshipfactory.de",
    "www.starshipfactory.eu",
    "www.starshipfactory.org",
    "www.hackerspace-basel.ch",
    "www.hackerspace-basel.com",
    "www.hackerspace-basel.net",
    "www.hackerspace-basel.org",
    "www.fablab-basel.ch",
    "www.fablabbasel.ch",
    "www.makerspace-basel.ch",
    "www.makerspacebasel.ch",
]

DEBUG = False

# Some mail destinations which hopefully won't eat the mails.
ADMINS = (('NGAS Admins', 'admins@ngas.ch'),)
MANAGERS = ADMINS + (('Public Relations', 'pr@lists.starship-factory.ch'),)
EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

# Some security related settings.
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECRET_KEY = os.environ.get('SFBLOG_SECRET_KEY')

# Settings for life behind a reverse proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': dj_database_url.config(conn_max_age=None)
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

ZINNIA_PROTOCOL = "https"

ZINNIA_SPAM_CHECKER_BACKENDS = set()
AKISMET_SECRET_API_KEY = None

if os.path.exists(os.environ.get('SFBLOG_CONFIG_PATH') + '/akismet_secret'):
    ZINNIA_SPAM_CHECKER_BACKENDS = ('zinnia.spam_checker.backends.automattic',)
    AKISMET_SECRET_API_KEY = open(os.environ.get('SFBLOG_CONFIG_PATH') +
                                  '/akismet_secret').read().strip()
