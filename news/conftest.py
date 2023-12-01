from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def user():
    return AnonymousUser()


@pytest.fixture
def anonymous(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_count(author):
    today = datetime.today()
    news_count = News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_count


@pytest.fixture
def comments(author, news):
    now = timezone.now()
    for index in range(5):
        comments = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария',
            created=now + timedelta(days=index),
        )
        comments.created = now + timedelta(days=index)
        comments.save()
    return comments


@pytest.fixture
def slug_for_args(news):
    return news.id,


@pytest.fixture
def form_data():
    return {
        'text': 'Текст комментария',
    }
