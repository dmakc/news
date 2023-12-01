from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects
# Дополнительно импортируем функцию slugify.
from pytils.translit import slugify

# Импортируем из модуля forms сообщение об ошибке:
from news.forms import WARNING, BAD_WORDS
from news.models import News, Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, form_data, slug_for_args,
):
    url = reverse('news:detail', args=slug_for_args)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_note(
    author_client, author, form_data, slug_for_args,
):
    url = reverse('news:detail', args=slug_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_user_cant_use_bad_words(
    author_client, comments, form_data, slug_for_args,
):
    url = reverse('news:detail', args=slug_for_args)
    form_data['text'] = {f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == 5


def test_author_can_edit_comment(
    author_client, form_data, comments, slug_for_args,
):
    url = reverse('news:edit', args=slug_for_args)
    url_news = reverse('news:detail', args=slug_for_args)
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{url_news}#comments')
    comments.refresh_from_db()
    assert comments.text == form_data['text']


def test_author_can_delete_comment(
    author_client, slug_for_args, comments,
):
    url = reverse('news:delete', args=slug_for_args)
    url_news = reverse('news:detail', args=slug_for_args)
    response = author_client.post(url)
    assertRedirects(response, f'{url_news}#comments')
    assert Comment.objects.count() == 4


def test_user_cant_edit_comment_of_another_user(
    admin_client, form_data, comments, slug_for_args,
):
    url = reverse('news:edit', args=slug_for_args)
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comments.id)
    assert comments.text == comment_from_db.text


def test_user_cant_delete_comment_of_another_user(
    admin_client, slug_for_args, comments,
):
    url = reverse('news:delete', args=slug_for_args)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 5
