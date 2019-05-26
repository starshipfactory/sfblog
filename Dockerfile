FROM python:2.7-slim
LABEL maintainer Alexander Clausen <alex@gc-web.de>

RUN useradd -ms /bin/bash sfblog
RUN apt-get -q -y update
RUN apt-get -q -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold --purge install git

ADD . /sfblog
ADD deployment/ancientca.crt /usr/local/share/ca-certificates/ancientca.crt
RUN update-ca-certificates
RUN chmod -R a+rX /sfblog
RUN pip install /sfblog/wheels/*.whl
RUN rm -r /sfblog/wheels/

EXPOSE 8000
VOLUME ["/var/www/media", "/var/www/static", "/etc/sfblog"]
USER sfblog
CMD ["/sfblog/deployment/start_gunicorn.sh"]
