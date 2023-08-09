from django.db import models

from messenger.settings import AUTH_USER_MODEL


class Chat(models.Model):
    messages = models.ManyToManyField('Message', related_name='messages', verbose_name='Сообщения')
    participants = models.ManyToManyField(AUTH_USER_MODEL, verbose_name='Участники')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)


class Message(models.Model):
    class Status(models.TextChoices):
        SENT = 'sent', 'Отправлено'
        RECEIVED = 'received', 'Получено'

    text = models.CharField(verbose_name='Текст', max_length=200)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=Status.choices, default=Status.SENT)
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sender', verbose_name='Отправитель',
                               on_delete=models.CASCADE)
