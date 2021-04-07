from game import models
import random


def city_generator(players_amount, brokers_amount):

	cities = [
		'IV',
		'WS',
		'TT',
		'AD',
		'NF',
		'ET',
	]
	cities_for_iter = cities[:brokers_amount]
	while players_amount > 0:
		yield cities_for_iter.pop(random.randint(0, len(cities_for_iter) - 1))
		players_amount -= 1
		if len(cities_for_iter) == 0:
			cities_for_iter = cities[:brokers_amount]


def generate_role_instances(session_instance):
	players = session_instance.player.all()
	# city = city_generator(players.count(), session_instance.number_of_brokers)
	cities = ['IV', 'WS', 'TT', 'AD', 'NF', 'ET']

	for player in players:
		# FIXME це пиздец
		player.city = random.choice(cities[:session_instance.number_of_brokers])
		if player.role == 'producer':
			player.balance = session_instance.producer_starting_balance
			player.save()
			models.ProducerModel.objects.create(
				player=player).save()
		else:
			player.balance = session_instance.broker_starting_balance
			player.save()
			models.BrokerModel.objects.create(
				player=player
			).save()
