FROM python:2.7-slim
LABEL maintainer Alexander Clausen <alex@gc-web.de>

RUN apt-get -q -y update
RUN apt-get -q -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold --purge install git

ARG CACHE_EPOCH=2017-08-29-1

ADD . /sfblog

RUN pip install /sfblog/wheels/*.whl

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "--pythonpath", "/sfblog", "sfblog_project.wsgi:application", "-b", "0.0.0.0:8000"]
