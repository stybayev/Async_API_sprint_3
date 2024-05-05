## Инструкция по запуску:

1) Клонируем репозиторий:
   ```
   git clone git@github.com:stybayev/Async_API_sprint_2.git
   ```
2) Заходим в корневую директрию проекта `/Async_API_sprint_2`:
   ```
   cd path/to/Async_API_sprint_2
   ```
3) Создаем файл `.env` и копируем в него содержимое файла `.env.example`:
   ```
   cp .env.example .env
   ```
4) Запускаем сервисы:
   ```
    docker-compose -f docker-compose.dev.yml up      
   ```
5) Все должно работать!
