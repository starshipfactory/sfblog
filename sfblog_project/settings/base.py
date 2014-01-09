"""
Django settings for sfblog_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import dirname, join, normpath
BASE_DIR = normpath(join(dirname(dirname(__file__)), ".."))

SIMPLECMS_SETUP_CALLBACK = "core.cms.setup"
SIMPLECMS_REPLACE_ADMIN_INDEX = True

# zinnia settings

SOUTH_MIGRATION_MODULES = {
    'zinnia': 'customblog.zinnia_migrations',
}
ZINNIA_ENTRY_BASE_MODEL = 'customblog.blog_models.BlogEntry'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#&(9az_9ahc(l!2yeo&oy+h7g)$-xwjf*y4m@!$148x)=#=na%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates'),
)

ALLOWED_HOSTS = []

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'zinnia.context_processors.version',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.admin',
    'tagging',
    'mptt',
    'oembed',
    'ckeditor',
    'core',
    'simplecms',
    'zinnia',
    'south',
    'imagetools',
    'customblog',  # keep this below zinnia
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sfblog_project.urls'

WSGI_APPLICATION = 'sfblog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('de', 'Deutsch'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    join(BASE_DIR, "static"),
)

STATIC_ROOT = join(BASE_DIR, "static_root")

MEDIA_URL = "/media/"

MEDIA_ROOT = join(BASE_DIR, "media")

SITE_ID = 1

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format', 'Bold', 'Italic'],
            ['NumberedList', 'BulletedList', 'Table'],
            ['Link', 'Unlink'],
            ['Undo', 'Redo', 'Copy', 'PasteText'],
            ['Source', 'Maximize', ]
        ],
        #'format_tags': 'p;h3;h4;h5;pre;', FIXME bug in ckeditor?
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}
