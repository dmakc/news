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


@pytest.mark.parametrize(
    'name',
    ('news:home')
)
def test_news_order(name, author_client):
    url = reverse(name)
    response = author_client.get(url)
    object_list = response.context['object_list']
    print(object_list)
    all_dates = [news_count.date for news_count in object_list]
    print(all_dates)
    sorted_dates = sorted(all_dates, reverse=True)
    assert (all_dates is sorted_dates)
