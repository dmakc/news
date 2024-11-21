from datetime import datetime

from django.conf import settings
from django.db import models

from core.constants import MAX_SLICE, MAX_FIELD_LENGTH


class News(models.Model):
    title = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    date = models.DateField(
        default=datetime.today,
        verbose_name='Дата',
    )

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'

    def __str__(self):
        return self.text[:MAX_SLICE]


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.text[:MAX_SLICE]
