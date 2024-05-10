#!/bin/sh
# Проверяем доступность Elasticsearch на порту 9200
while ! nc -z elasticsearch 9200; do
  echo "Waiting for Elasticsearch..."
  sleep 1
done
echo "Elasticsearch is ready!"
