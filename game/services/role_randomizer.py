import random


def distribute_roles(session_model, session_id):
	"""
	Распределяет роли игроков в сессии
	"""
	session_instance = session_model.objects.get(id=session_id)
	players_queryset = session_instance.player.filter(role='unassigned')
	assigned_brokers = session_instance.player.filter(role='broker').count()
	assigned_producers = session_instance.player.filter(role='producer').count()
	# unassigned
	broker_players = random.sample(list(players_queryset), session_instance.number_of_brokers)

	for player in broker_players:
		player.role = 'broker'
		print(player)

	for player in players_queryset:
		if player.role == 'unassigned':
			player.role = 'producer'

	for player in players_queryset:
		player.save()
