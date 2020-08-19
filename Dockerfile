FROM python:3.6-alpine

RUN adduser -D test_python

WORKDIR /home/test_python

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN \
apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY test_python.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP test_python.py

RUN chown -R test_python:test_python ./
USER test_python

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]

CMD ["python3", "app.py"]