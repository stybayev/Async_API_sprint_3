#!/bin/sh
# Проверяем доступность Redis на порту 6379
while ! nc -z redis 6379; do
  echo "Waiting for Redis..."
  sleep 1
done
echo "Redis is ready!"
