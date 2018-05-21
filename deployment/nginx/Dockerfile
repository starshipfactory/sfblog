FROM nginx:1.14.0
LABEL maintainer Alexander Clausen <alex@gc-web.de>

ADD ./nginx.conf /etc/nginx/conf.d/sfblog.conf
RUN rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
