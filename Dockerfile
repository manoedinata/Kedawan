# Dockerfile to run Kedawan on Docker container
# With: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/

FROM tiangolo/uwsgi-nginx-flask:python3.11

RUN apt-get update && apt-get install cron -y 

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

ADD crontab /etc/cron.d/kedawan-autodelete

RUN chmod 0644 /etc/cron.d/kedawan-autodelete

RUN crontab /etc/cron.d/kedawan-autodelete
