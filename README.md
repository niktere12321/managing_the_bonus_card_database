# Проект managing_the_bonus_card_database

## Описание

managing_the_bonus_card_database это веб-приложение для управления базой данных бонусных карт.

Пользователи могут:
- Просматривать все свои карты и фильтровать их по многим полям;
- Просматривать профиль карты и историю покупок по ней;
- Создавать карты;
- Активация/деактивация карту;
- Удалять карту

## Технологии
- Python 3.9.13
- Django 4.1.4
- Celery 4.4.7

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/niktere12321/managing_the_bonus_card_database.git
```
```bash
cd managing_the_bonus_card_database/
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

* Можете устоновить свои настойки в директории где находить файл settings.py назвав свой файл с настройками settings_local.py

* Выполните миграции:
```bash
cd managing/
```
```bash
python manage.py migrate
```

* Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

* Запустите сервер:
```bash
python manage.py runserver
```

* Во втором терминале запустить Celery в директории где находиться manage.py предварительно запустив Redis:
```bash
celery -A managing worker -l info -P gevent
```

---
## Об авторе

Терехов Никита Алексеевич
