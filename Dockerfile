FROM python:2.7-slim
LABEL maintainer Alexander Clausen <alex@gc-web.de>

RUN apt-get -q -y update
RUN apt-get -q -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold --purge install git nginx-light supervisor

ADD ./supervisord.conf /etc/supervisor/conf.d/sfblog.conf
ADD ./nginx.conf /etc/nginx/sites-enabled/sfblog.conf
RUN rm /etc/nginx/sites-enabled/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir /var/www/static/
RUN mkdir /var/www/media/

ADD . /sfblog
RUN pip install /sfblog/wheels/*.whl

EXPOSE 80

CMD ["supervisord", "-n"]
