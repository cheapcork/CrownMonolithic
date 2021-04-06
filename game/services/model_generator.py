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
	city = city_generator(players.count(), session_instance.number_of_brokers)

	for player in players:
		if player.role == 'producer':
			models.ProducerModel.objects.create(
				player=player,
				city=next(city),
			).save()
		else:
			models.BrokerModel.objects.create(
				player=player,
				city=next(city),
			).save()
	del city
