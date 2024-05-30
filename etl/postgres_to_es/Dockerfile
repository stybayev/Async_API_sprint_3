FROM registry.gitlab.com/dosxana/doskhan_dockerhub/python:3.10-slim-buster

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -m load_data
