import pytest
from django.conf import settings

from django.urls import reverse


# @pytest.mark.parametrize(
#     'parametrized_client, note_in_list',
#     (
#         (pytest.lazy_fixture('author_client'), True),
#         (pytest.lazy_fixture('admin_client'), False),
#     )
# )
# def test_notes_list_for_different_users(
#         news, parametrized_client, note_in_list
# ):
#     url = reverse('news:home')
#     response = parametrized_client.get(url)
#     object_list = response.context['object_list']
#     assert (news in object_list) is note_in_list


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), False),
        (pytest.lazy_fixture('admin_client'), True),
    )
)
def test_new_count(
        news_count, parametrized_client, note_in_list
):
    url = reverse('news:home')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    print(note_in_list)
    assert (
        news_count in object_list
    ) is note_in_list <= settings.NEWS_COUNT_ON_HOME_PAGE
