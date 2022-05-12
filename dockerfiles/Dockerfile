FROM python:3.8-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install git iputils-ping gcc -y
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . /app
RUN useradd backend
RUN chown -R backend:backend /app
USER backend
