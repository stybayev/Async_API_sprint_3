FROM python:3.10-slim

WORKDIR /tests

# Установка зависимостей
COPY requirements.txt /tests/
RUN pip install -r requirements.txt

# Копирование тестового кода
COPY . /tests/

# Команда для запуска тестов
# CMD ["pytest", "/tests/functional/src"]


