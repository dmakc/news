import pytest

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment
from django.contrib.auth.models import AnonymousUser


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author)  # Логиним автора в клиенте.
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
def comments(author, news):
    news = Comment.objects.create(
        news=news,
        author=author,
        text='Текст новости',
    )
    return news


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def slug_for_args(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return news.pk,


# Добавляем фикстуру form_data
@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
    }
