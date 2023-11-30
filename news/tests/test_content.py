from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.parametrize(
    'parametrized_client, news_in_list',
    (
        (pytest.lazy_fixture('author_client'), False),
    )
)
def test_new_count(
        parametrized_client, news_in_list
):
    url = reverse('news:home')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert (
        news_count in object_list
    ) is news_in_list <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(author_client, news_count):
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    all_dates = [news_count.date for news_count in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author_client, slug_for_args, comments):
    url = reverse('news:detail', args=slug_for_args)
    response = author_client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    print(all_comments[0].created)
    print(all_comments[1].created)
    assert all_comments[0].created < all_comments[1].created
