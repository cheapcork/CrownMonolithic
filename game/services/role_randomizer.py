import random


def distribute_roles(session_model, session_id):
	"""
	Распределяет роли игроков в сессии
	"""
	session_instance = session_model.objects.get(id=session_id)
	players_queryset = session_instance.player.all()
	broker_players = random.sample(list(players_queryset), session_instance.number_of_brokers)

	for player in broker_players:
		player.role = 'broker'
		player.save()

	for player in players_queryset:
		if player.role == 'unassigned':
			player.role = 'producer'
			player.save()
