FROM python:3.6-alpine

RUN adduser -D test_python

WORKDIR /home/test_python

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY test_python.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP test_python.py

RUN chown -R test_python:test_python ./
USER test_python

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]