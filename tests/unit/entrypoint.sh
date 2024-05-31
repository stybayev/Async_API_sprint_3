#!/bin/bash

# Подождать доступности PostgreSQL
while ! nc -z test_db 5432; do
  echo "Ожидание PostgreSQL..."
  sleep 1
done

# Подождать доступности MinIO
while ! nc -z test_minio 9000; do
  echo "Ожидание MinIO..."
  sleep 1
done

# Запустить тесты
pytest tests/unit -p no:warnings
