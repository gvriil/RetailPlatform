# RetailPlatform

## Описание проекта

Система управления сетью торговых точек и поставщиков с возможностью отслеживания товаров, задолженностей и иерархических отношений между узлами сети.

## Технологии

- Python 3.12+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Django Filter

## Установка и настройка

### Клонирование репозитория

```bash
git clone git@github.com:gvriil/RetailPlatform.git
cd RetailPlatform
```

### Настройка виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта:

```
# .env
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/network_db

# Настройки для подключения к внешним сервисам
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Миграции и запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Основные возможности

### Административная панель

- Управление узлами сети (торговые точки, склады, поставщики)
- Фильтрация по городам и странам
- Функция очистки задолженности перед поставщиком

### REST API

Доступ к API имеют только активные сотрудники.

#### Узлы сети (NetworkNode)
- `GET /api/nodes/` - список узлов сети
- `POST /api/nodes/` - создание узла
- `GET /api/nodes/{id}/` - информация о конкретном узле
- `PUT/PATCH /api/nodes/{id}/` - обновление данных (поле задолженности защищено от изменений)
- `DELETE /api/nodes/{id}/` - удаление узла
- `POST /api/nodes/{id}/clear_debt/` - очистка задолженности
- `GET /api/nodes/statistics/` - агрегированная статистика

#### Товары (Product)
- Полный CRUD с фильтрацией, поиском и пагинацией

## Безопасность

- Для защиты чувствительных данных используется файл `.env`
- Кастомная система разрешений для доступа к API
- Защита полей от несанкционированного изменения

## Дополнительная документация

Полную документацию API можно найти по адресу `/api/docs/` после запуска проекта.