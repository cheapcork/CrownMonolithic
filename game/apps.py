from django.apps import AppConfig


class GameConfig(AppConfig):
	name = 'game'

	# FIXME Что это?
	def ready(self):
		pass
