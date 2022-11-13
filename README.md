![Workflow Badge](https://github.com/mrgolubeff/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# api_yamdb
# Проект «API для Yatube»
### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Из пользовательских оценок формируется рейтинг произведения.
### Авторы
Андрей Малышев, Елена Блинова, Владимир Голубев

### Установка
--- Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:mrgolubeff/api_yamdb.git
cd api_yamdb
```

--- Cоздать и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
```
--- Установить зависимости из файла requirements.txt:
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
--- Выполнить миграции:
```sh
python manage.py migrate
```
--- Запустить проект:
```sh
python manage.py runserver
```

### Примеры запросов
(При запросах к локальному серверу)

Запрос
```
GET http://127.0.0.1:8000/api/v1/titles
```
Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```

Запрос
```
GET http://127.0.0.1:8000/api/v1/
```
Вернет список доступных эндпоинтов

### Наполнение env-файла (/infra_sp2/nginx/)
DB_ENGINE=[path to postgresql backend] # указываем, что работаем с postgresql
DB_NAME=[datebase name] # имя базы данных
POSTGRES_USER=[login] # логин для подключения к базе данных
POSTGRES_PASSWORD=[password] # пароль для подключения к БД
DB_HOST=[container name] # название сервиса (контейнера)
DB_PORT=[bd port] # порт для подключения к БД
SECRET_KEY=[Django secret key] # Секретный ключ из файла settings.py

### Команды для запуска приложения в контейнерах
1. Перейти в директорию infra_sp2/infra (в которой хранится файл docker-compose.yaml)
2. Из этой директории выполнить команду *docker-compose up -d --build* (это пересоберет контейнеры и запустит их в фоновом режиме)
3. Сделать миграции командой *docker-compose exec web python manage.py migrate*
4. Остановить исполнение проекта можно командой *docker-compose down*
