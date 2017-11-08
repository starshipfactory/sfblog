FROM python:2.7-slim
LABEL maintainer Alexander Clausen <alex@gc-web.de>

RUN apt-get -q -y update
RUN apt-get -q -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold --purge install git

ADD . /sfblog
RUN chmod -R a+rX /sfblog
RUN pip install /sfblog/wheels/*.whl
RUN rm -r /sfblog/wheels/

EXPOSE 8000
VOLUME ["/var/www/media", "/var/www/static", "/etc/sfblog"]
RUN useradd -ms /bin/bash sfblog
USER sfblog
CMD ["/sfblog/deployment/start_gunicorn.sh"]
