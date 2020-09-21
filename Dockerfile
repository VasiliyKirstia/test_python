FROM python:buster

RUN mkdir -p /app/dlogs
COPY . /app

WORKDIR /app

VOLUME /app/dlogs

CMD ['python', 'test_python.py']