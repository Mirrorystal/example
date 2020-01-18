FROM python:3.8

RUN pip3 install --no-cache-dir \
    flask==1.1.1 \
    flask-login==0.4.1 \
    flask-restful==0.3.7 \
    flask-wtf==0.14.2 \
    flask-mongoengine==0.9.5 \
    passlib==1.7.1 \
    pillow==6.2.1 \
    gevent==1.4.0 \
    flask-uploads==0.2.1 \
    openpyxl==3.0.2 \
    prometheus-flask-exporter==0.12.1 \
    -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /srv/backend

EXPOSE 5000

ENTRYPOINT [ "python3", "run.py" ]
