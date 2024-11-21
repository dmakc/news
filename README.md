#  News

Cайт, на котором выкладываются актуальные новости.

## Описание проекта

Приложение созданное для ведения новостной рубрики.
Посетители могут зарегистрироваться на сайте.
Авторизованные пользователи имеют возможно оставлять комментарии к новостям.

___
## Стек технологии
![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg) ![Django 3.2.15](https://img.shields.io/badge/Django-3.2.15-green.svg)

## Как развернуть проект

1. Клонировать репозиторий git@github.com:dmakc/news.git
```
git clone git@github.com:dmakc/news.git
```

2. Установить и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```

3. Установить зависимости и применить миграции
```
pip install -r requirements.txt
python manage.py migrate
```

4. Для загрузки заготовленных новостей после применения миграций выполните команду:
```
bash
python manage.py loaddata news.json
```

5. Создать суперпользователя
```
python manage.py createsuperuser
```

6. Запустить проект
```
python manage.py runserver
```

## Автор
[Давыдов Максим](https://github.com/dmakc)
