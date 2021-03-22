from .. import models
import random
import copy


def player_role_models_create(session_model, session_id):
	def city_generator(players_amount, brokers_amount):
		local_players_amount = copy.copy(players_amount)
		cities = [
			'NF',
			'TT',
			'WS',
			'IV',
			'AD',
			'ET',
		]
		cities_for_iter = cities[:brokers_amount]
		while local_players_amount > 0:
			yield cities.pop(random.randint(0, len(cities_for_iter) - 1))
			local_players_amount -= 1
			if len(cities_for_iter) == 0:
				cities_for_iter = cities[:brokers_amount]

	session_instance = session_model.objects.get(id=session_id)
	players = session_instance.player.all()
	city = city_generator(len(players), session_instance.players.filter(role=brokers).count())

	producer_models = [
		models.ProducerModel.objects.create(
			player=player,
			session=session_instance,
			city=next(city),
		)
		for player in players if player.role == 'producer'
	]
	broker_models = [
		models.BrokerModel.objects.create(
			player=player,
			session=session_instance,
			city=next(city),
		)
		for player in players if player.role == 'brokers'
	]

	return broker_models, producer_models
