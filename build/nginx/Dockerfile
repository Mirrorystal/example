FROM nginx:1.7

ADD ./default.conf /etc/nginx/conf.d/default.conf

RUN sed -i s/'txt;'/'txt log;'/ /etc/nginx/mime.types
