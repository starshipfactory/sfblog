#!/bin/bash
export PYTHONPATH=/sfblog
/usr/local/bin/django-admin.py collectstatic --noinput
/usr/local/bin/django-admin.py migrate
/usr/local/bin/django-admin.py simplecms_init
/usr/local/bin/gunicorn -w 4 --pythonpath /sfblog sfblog_project.wsgi:application -b 0.0.0.0:8000
