from .. import models
import random
import copy


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
		yield cities_for_iter.pop(random.randint(0, len(cities_for_iter) - 1))
		local_players_amount -= 1
		if len(cities_for_iter) == 0:
			cities_for_iter = cities[:brokers_amount]

def create_role_models(session_model, session_id):
	session_instance = session_model.objects.get(id=session_id)
	print(session_instance)
	players = session_instance.player.all()
	print(players)
	city = city_generator(len(players), session_instance.player.filter(role='broker').count())

	for player in players:
		if player.role == 'producer':
			models.ProducerModel.objects.create(
				player=player,
				# session=session_instance,
				city=next(city),
			)
		else:
			models.BrokerModel.objects.create(
				player=player,
				# session=session_instance,
				city=next(city),
			)
	del city
