FROM python:3.10-slim

WORKDIR /tests

# Установка зависимостей
COPY requirements.txt /tests/
RUN pip install -r requirements.txt

# Установка netcat-openbsd для скриптов ожидания
RUN apt-get update && apt-get install -y netcat-openbsd

# Копирование тестового кода
COPY . /tests/

# Копирование скриптов ожидания
COPY wait-for-es.sh wait-for-redis.sh /usr/local/bin/

# Делаем скрипты исполняемыми
RUN chmod +x /usr/local/bin/wait-for-es.sh /usr/local/bin/wait-for-redis.sh

# Запуск скриптов ожидания и тестов
CMD [ "sh", "-c", "/usr/local/bin/wait-for-es.sh && /usr/local/bin/wait-for-redis.sh && pytest tests/functional/src -p no:warnings" ]
