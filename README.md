# Hotel Booking API

Проект представляет собой REST API-сервис для управления отелями, номерами и их бронированиями. Сервис предоставляет CRUD-функциональность и реализован с использованием Django, Django REST Framework и PostgreSQL.

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/smaylick/hotel-booking-api.git
cd hotel-booking-api
```

### 2. Создание `.env` файла

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

### 3. Запуск с помощью Docker

```bash
docker-compose up --build
```

Проект будет доступен по адресу: http://localhost:8000/

### 4. Локальный запуск без Docker

```bash
poetry install
poetry run python src/manage.py migrate
poetry run python src/manage.py runserver
```

## Тестирование

```bash
pytest
```

## Примеры curl-запросов

### Отели

#### Создание отеля

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "Test Hotel", "address": "City Center"}' \
    http://localhost:8000/api/hotel/
```

#### Получение списка отелей

```bash
curl -X GET http://localhost:8000/api/hotel/
```

### Номера

#### Создание номера

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"hotel": 1, "description": "Sea view", "price": "1500.00"}' \
    http://localhost:8000/api/hotel/rooms/
```

#### Получение списка номеров с сортировкой

```bash
curl -X GET "http://localhost:8000/api/hotel/rooms/?ordering=price"
```

#### Удаление номера

```bash
curl -X DELETE http://localhost:8000/api/hotel/rooms/1/
```

### Бронирования

#### Создание брони

```bash
curl -X POST -d "room=1" -d "date_start=2025-06-01" -d "date_end=2025-06-05" \
    http://localhost:8000/api/hotel/bookings/create/
```

#### Получение списка броней номера

```bash
curl -X GET "http://localhost:8000/api/hotel/bookings/list/?room_id=1"
```

#### Удаление брони

```bash
curl -X DELETE http://localhost:8000/api/hotel/bookings/1/
```

## 📚 Документация API

Для удобного просмотра и тестирования доступна автоматически сгенерированная Swagger-документация:

- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **OpenAPI schema (JSON)**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

Документация создаётся с помощью библиотеки [`drf-spectacular`](https://drf-spectacular.readthedocs.io/), которая поддерживает спецификацию OpenAPI 3.0.

## Структура проекта

```
hotel-booking-api/
├── src/
│   ├── config/           # Настройки проекта Django
│   └── hotel/            # Основное приложение
├── tests/                # Юнит-тесты
├── Dockerfile
├── docker-compose.yml
├── .env.example          # Шаблон переменных окружения
├── pyproject.toml        # Зависимости и настройки Poetry
└── README.md
```

## Принятые решения

- Структура проекта соответствует шаблону `src-layout`.
- Зависимости и управление окружением — через `poetry`.
- Использован `pytest` и `pytest-django` для написания тестов.
- Добавлены типовые фильтрации и сортировки в списках.
- Настроен Docker + PostgreSQL через `docker-compose`.
- Используются `.env` переменные, шаблон `.env.example` добавлен в проект.
