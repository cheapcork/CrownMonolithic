from django.db import models
from game.models import SessionModel
import binascii
import os


class PlayerManager(models.Manager):
    def create_player(self, username):
        if not username:
            raise ValueError('Username required')
        # if not session:
        #     raise ValueError('Session instance required')
        # player = self.model(username=username, session=session)
        player = self.model(username=username)
        player.save()
        return player


class PlayerModel(models.Model):
    username = models.CharField('nickname', max_length=100, unique=True)
    # session = models.ForeignKey(SessionModel, on_delete=models.CASCADE,
    #                             verbose_name='Session')

    objects = PlayerManager()
    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'Игрок {self.username}'


class PlayerTokenModel(models.Model):
    key = models.CharField('key', max_length=100)
    player = models.OneToOneField(PlayerModel, on_delete=models.CASCADE,
                                  related_name='token', verbose_name='player')
    created = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
