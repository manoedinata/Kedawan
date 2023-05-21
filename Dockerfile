# Use a lightweight base image
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app
COPY . /app

# Install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add --no-cache mariadb-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN apk del build-deps

# Set the command to run the startup script
CMD ["/app/startup.sh"]
