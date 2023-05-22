# Dockerfile to run Kedawan on Docker container
# With: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/

FROM tiangolo/uwsgi-nginx-flask:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
