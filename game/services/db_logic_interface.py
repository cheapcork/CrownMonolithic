from game.services.services_normal import count_turn
from game.services.producer import ProducerNormal
from game.services.broker import BrokerNormal
from game.services.transaction import TransactionNormal as Transaction


def change_game_parameters(session_model, session_id: int):
	"""
	Интерфейс, который использует функцию пересчёта хода :count_turn: для изменения полей таблиц в БД.
	"""
	session_instance = session_model.objects.get(id=session_id)

	players_queryset = session_instance.player.all()
	db_producers_queryset = players_queryset.filter(role='producer')
	db_broker_queryset = players_queryset.filter(role='broker')
	print('DB-L: ', players_queryset)

	db_producers, db_brokers = [], []
	for player in db_producers_queryset:
		db_producers.append(player.producer.first())
	for player in db_broker_queryset:
		db_brokers.append(player.broker.first())

	db_transactions = session_instance.transaction.filter(turn=session_instance.current_turn)

	producers, brokers, transactions = [], [], []

	crown_balance = session_instance.crown_balance

	for transaction in db_transactions:
		terms = {
			'quantity': transaction.quantity,
			'price': transaction.price,
			'transporting_cost': transaction.transporting_cost
		}
		deal = Transaction(transaction.producer.id, transaction.broker.id, terms).form_transaction()
		transactions.append(deal)

	for db_producer in db_producers:
		producer = ProducerNormal(db_producer.balance)
		producer.id = db_producer.id
		producer.billets_produced = db_producer.billets_produced
		producer.billets_stored = db_producer.billets_stored
		for transaction in transactions:
			if transaction['producer'] == producer.id:
				producer.make_deal(transaction)
		producers.append(producer)

	for db_broker in db_brokers:
		broker = BrokerNormal(db_broker.balance)
		broker.id = db_broker.id
		for transaction in transactions:
			if transaction['broker'] == broker.id:
				broker.make_deal(transaction)
		brokers.append(broker)

	crown_balance_updated = count_turn(producers, brokers, transactions, crown_balance)

	for producer in producers:
		for db_producer in db_producers:
			if db_producer.id == producer.id:
				db_producer.balance = producer.balance
				db_producer.is_bankrupt = producer.is_bankrupt
				db_producer.billets_produced = producer.billets_produced
				db_producer.billets_stored = producer.billets_stored
				db_producer.save()

	for broker in brokers:
		for db_broker in db_brokers:
			if db_broker.id == broker.id:
				db_broker.balance = broker.balance
				db_broker.is_bankrupt = broker.is_bankrupt
				db_broker.save()

	return crown_balance_updated

