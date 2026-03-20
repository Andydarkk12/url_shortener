# URL shortener service 

Микросервис для сокращения ссылок. Позволяет создавать короткие ссылки и отслеживать количество переходов.

## Возможности

-Сокращение длинной ссылки<br>
-Редирект по короткой ссылке<br>
-Количество переходов

## Эндпоинты API 
|Метод|URL|Описание|
|-|-|-|
| `POST` | `/api/shorten` | Создать короткую ссылку |
| `GET` | `/{short_id}` | Редирект на оригинальный URL |
| `GET` | `/api/stats/{short_id}` | Получить статистику переходов |


### Примеры запросов

**Создание короткой ссылки:**
```bash
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

**Ответ:**
```json
{
  "short_id": "aB3cD4",
  "short_url": "http://localhost:8000/aB3cD4",
  "original_url": "https://google.com"
}
```

**Получение статистики**
```bash
curl http://localhost:8000/api/stats/aB3cD4
```

**Ответ**
```json
{
    "short_id": "aB3cD4",
    "original_url": "https://google.com",
    "clicks": 42,
    "created_at": "2024-03-20T15:30:00Z",
    "short_url": "http://localhost:8000/aB3cD4"
}
```

## Сброка и запуск проекта
### 1. Клонирование репозитория
```bash
git clone https://github.com/Andydarkk12/url_shortener.git
cd url_shortener
```
### 2. Создание и настройка файлов окружения
```bash
cp .env.example .env
```
Откройте файл `.env` и заполните поля:
| Переменная | Описание | Пример |
|-|-|-|
SECRET_KEY|Секретный ключ Django|django-insecure-...
DEBUG|Режим отладки|True или False
ALLOWED_HOSTS|Разрешенные хосты|localhost,127.0.0.1
DOMAIN|Домен сервиса|http://localhost:8000
DB_NAME|Имя базы данных|urlshortener
DB_USER|Пользователь БД|postgres
DB_PASSWORD|Пароль БД|your-password


Генерация SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### 3. Сборка и запуск проекта
```bash
docker compose up --build
```
После запуска создайте суперпользователя для админки (необязательно):
```bash
docker compose exec web python manage.py createsuperuser
```

### 4. Проверка работы
* Админка: `http://localhost:8000/admin`
* API: `http://localhost:8000/api/shorten`

## Запуск тестов
```bash
# Локально
python manage.py test

# Через Docker
docker compose exec web python manage.py test
```
## Технологии
* Python 3.12

* Django 4.2

* Django REST Framework

* PostgreSQL 15

* Docker & Docker Compose