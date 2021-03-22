from .. import models
import random
import copy

def player_role_models_create(session, brokers, producers):
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

	city = city_generator(len(session.player.all()), len(brokers))

	producers = [
		models.ProducerModel.objects.create(
			player=player,
			session=session_instance,
			city=next(city),
		)
		for player in producers
	]
	brokers = [
		models.BrokerModel.objects.create(
			player=player,
			session=session_instance,
			city=next(city),
		)
		for player in brokers
	]

	return brokers, producers