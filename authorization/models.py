from django.db import models


class UserModel(models.Model):
    username = models.CharField(max_length=150, verbose_name='Ник пользователя', unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username}'
