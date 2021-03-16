from game.models import Session
from game.services.services_normal import count_turn
from game.services.producer import ProducerNormal as Producer
from game.services.broker import BrokerNormal as Broker
from game.services.transaction import TransactionNormal as Transaction


def change_game_parameters(session_model, session_id):
	db_producers = list(session_model.player.objects.filter(session_id=session_id, role='producer', is_bankrupt=False))
	db_brokers = list(session_model.player.objects.filter(session_id=session_id, role='broker', is_bankrupt=False))
	db_transactions = list(session_model.transaction.objects.filter(session_id=session_id, turn=Session.current_turn))
	session = session_model.objects.filter(session_id=session_id)

	producers = []
	brokers = []
	transactions = []
	crown_balance = session.crown_balance

	for transaction in db_transactions:
		terms = {
			'quantity': transaction.quantity,
			'price': transaction.price
		}
		deal = Transaction(transaction.producer, transaction.broker, terms).form_transaction()
		transactions.append(deal)

	for db_producer in db_producers:
		producer = Producer(db_producer.balance)
		producer.billets_produced = db_producer.billets_produced
		producer.billets_stored = db_producer.billets_stored
		# В сделках хранятся ссылки на объекты БД, но при этом данные объекты не используются непосредственно
		for transaction in transactions:
			if transaction['producer'] == db_producer:
				producer.make_deal(transaction)
		producers.append(db_producer)

	for db_broker in db_brokers:
		broker = Broker(db_broker.balance)
		for transaction in transactions:
			if transaction['broker'] == db_broker:
				broker.make_deal(transaction)
		brokers.append(broker)

	results = count_turn(producers, brokers, transactions, crown_balance)

	# Существует однозначное соответствие между индексами объектов БД и объектов классов

	for i in range(len(producers)):
		db_producer = db_producers[i]
		log_producer = results['producers'][i]
		db_producer.balance = log_producer.balance
		db_producer.is_bankrupt = log_producer.is_bankrupt
		db_producer.billets_stored = log_producer.billets_stored
		# FIXME Я хз, как сохранить экземпляр модели, а не все экземпляры сразу
		db_producer.save()

	for i in range(len(brokers)):
		db_broker = db_brokers[i]
		log_broker = results['brokers'][i]
		db_broker.balance = log_broker.balance
		db_broker.is_bankrupt = log_broker.is_bankrupt
		db_broker.save()

	session.crown_balance = results['crown_balance']
	session.save()
