import random


def distribute_roles(session_model, session_id):
	"""
	Распределяет роли игроков в сессии
	"""
	session_instance = session_model.objects.get(id=session_id)

	players_queryset = session_instance.player.all()

	preassigned_brokers = session_instance.player.filter(role='broker')
	preassigned_producers = session_instance.player.filter(role='producer')

	player_models_list = list(players_queryset)
	for broker in preassigned_brokers:
		player_models_list.remove(broker)
	for producer in preassigned_producers:
		player_models_list.remove(producer)

	number_of_brokers_to_distribute = session_instance.number_of_brokers - preassigned_brokers.count()
	try:
		broker_players_sample = random.sample(player_models_list, number_of_brokers_to_distribute)
		min_players, max_players = session_instance.number_of_players.split('-')
		print(int(min_players), session_instance.player.count(), int(max_players))
		assert int(min_players) <= session_instance.player.count() <= int(max_players)
	except (ValueError, AssertionError):
		raise Exception('Not enough players!')

	for player in players_queryset:
		for broker_player in broker_players_sample:
			if player == broker_player:
				player.role = 'broker'
				player.save()
				player_models_list.remove(broker_player)
		for remaining_player in player_models_list:
			remaining_player.role = 'producer'
			remaining_player.save()

