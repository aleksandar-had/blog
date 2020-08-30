FROM python:3.9-rc-alpine
RUN apk add --no-cache --update python3-dev  gcc build-base

RUN adduser -D blog
WORKDIR /home/blog

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt 
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY blog.py config.py boot.sh ./ 
RUN chmod +x boot.sh

ENV FLASK_APP blog.py

RUN chown -R blog:blog ./ 
USER blog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
