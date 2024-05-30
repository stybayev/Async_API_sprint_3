FROM registry.gitlab.com/dosxana/doskhan_dockerhub/python:3.11-slim-buster

WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PIP_ROOT_USER_ACTION=ignore

RUN groupadd -r django && useradd -d /opt/app -r -g django django \
    && chown django:django -R /opt/app/

COPY app/requirements.txt requirements.txt
COPY app/uwsgi/uwsgi.ini uwsgi.ini

RUN apt-get update && apt-get install -y netcat-traditional gcc libpq-dev \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY app/ .

RUN chmod +x docker-entrypoint.sh \
    && mkdir /opt/app/static \
    && mkdir /opt/app/uploads

EXPOSE 8001

RUN chown -R django:django /opt/app/static \
    && chown -R django:django /opt/app/uploads

USER django
ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]
