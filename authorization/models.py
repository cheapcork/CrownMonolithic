from django.db import models
import binascii
import os
from django.conf import settings
from CrownMonolithic.utils import get_player_model
from game.models import PlayerModel


def generate_token():
	"""
	Генерирует токен для пользователя
	"""
	return binascii.hexlify(os.urandom(20)).decode()


class TokenModel(models.Model):
	token = models.CharField(max_length=200, default=generate_token)
	player = models.OneToOneField(PlayerModel, on_delete=models.CASCADE, related_name='token', default=0)

	class Meta:
		verbose_name = 'Токен'
		verbose_name_plural = 'Токены'

	def __str__(self):
		return f'Токен игрока {self.player.nickname}'
