from game.services.normal.business_logic.count_turn import count_turn
from game.services.normal.business_logic.producer import ProducerNormal
from game.services.normal.business_logic.broker import BrokerNormal
from game.services.normal.business_logic.transaction import TransactionNormal as Transaction


def generate_producer(db_producer_model_instance, producer_class):
	producer = producer_class(db_producer_model_instance.balance)
	producer.id = db_producer_model_instance.id
	producer.billets_produced = db_producer_model_instance.billets_produced
	producer.billets_stored = db_producer_model_instance.billets_stored
	return producer


def generate_broker(db_broker_model_instance, broker_class):
	broker = broker_class(db_broker_model_instance.balance)
	broker.id = db_broker_model_instance.id
	return broker


def save_producer(producer_class_instance, db_producer_model_instance):
	db_producer_model_instance.balance = producer_class_instance.balance
	db_producer_model_instance.is_bankrupt = producer_class_instance.is_bankrupt
	db_producer_model_instance.billets_produced = producer_class_instance.billets_produced
	db_producer_model_instance.billets_stored = producer_class_instance.billets_stored
	db_producer_model_instance.status = producer_class_instance.status
	db_producer_model_instance.save()


def save_broker(broker_class_instance, db_broker_model_instance):
	db_broker_model_instance.balance = broker_class_instance.balance
	db_broker_model_instance.is_bankrupt = broker_class_instance.is_bankrupt
	db_broker_model_instance.status = broker_class_instance.status
	db_broker_model_instance.save()


def change_game_parameters(session_model, session_id: int):
	"""
	Интерфейс, который использует функцию пересчёта хода :count_turn:
	для изменения полей таблиц в БД.
	"""
	session_instance = session_model.objects.get(id=session_id)

	players_queryset = session_instance.player.all()
	db_producers_queryset = players_queryset.filter(role='producer')
	db_broker_queryset = players_queryset.filter(role='broker')

	db_producers, db_brokers = [], []
	for player in db_producers_queryset:
		db_producers.append(player.producer.first())
	for player in db_broker_queryset:
		db_brokers.append(player.broker.first())

	db_transactions = session_instance.transaction.filter(
		turn=session_instance.current_turn, status='accept')

	producers, brokers, transactions = [], [], []

	crown_balance = session_instance.crown_balance

	for transaction in db_transactions:
		terms = {
			'quantity': transaction.quantity,
			'price': transaction.price,
			'transporting_cost': transaction.transporting_cost
		}
		deal = Transaction(transaction.producer.id, transaction.broker.id,
						   terms).form_transaction()
		transactions.append(deal)

	for db_producer in db_producers:
		producer = generate_producer(db_producer, ProducerNormal)
		for transaction in transactions:
			if transaction['producer'] == producer.id:
				producer.make_deal(transaction)
		producers.append(producer)

	for db_broker in db_brokers:
		broker = generate_broker(db_broker, BrokerNormal)
		for transaction in transactions:
			if transaction['broker'] == broker.id:
				broker.make_deal(transaction)
		brokers.append(broker)

	crown_balance_updated = count_turn(producers, brokers,
									   transactions, crown_balance)

	for producer in producers:
		for db_producer in db_producers:
			if db_producer.id == producer.id:
				save_producer(producer, db_producer)

	for broker in brokers:
		for db_broker in db_brokers:
			if db_broker.id == broker.id:
				save_broker(broker, db_broker)

	return crown_balance_updated


def initialize_game_settings(session_model, session_id: int):
	"""
	Инициализирует игровые настройки
	"""
	session_instance = session_model.objects.get(id=session_id)

	if session_instance.game_type == 'normal':
		if session_instance.number_of_players == '12-14':
			if not session_instance.number_of_brokers:
				session_instance.number_of_brokers = 3
			session_instance.broker_starting_balance = 8000
			session_instance.producer_starting_balance = 4000
		elif session_instance.number_of_players == "15-20":
			if not session_instance.number_of_brokers:
				session_instance.number_of_brokers = 4
			session_instance.broker_starting_balance = 12000
			session_instance.producer_starting_balance = 6000
		elif session_instance.number_of_players == "21-25":
			if not session_instance.number_of_brokers:
				session_instance.number_of_brokers = 5
			session_instance.broker_starting_balance = 12000
			session_instance.producer_starting_balance = 6000
		elif session_instance.number_of_players == "26-30":
			if not session_instance.number_of_brokers:
				session_instance.number_of_brokers = 6
			session_instance.broker_starting_balance = 12000
			session_instance.producer_starting_balance = 6000
		elif session_instance.number_of_players == "31-35":
			if not session_instance.number_of_brokers:
				session_instance.number_of_brokers = 7
			session_instance.broker_starting_balance = 12000
			session_instance.producer_starting_balance = 6000
	elif session_instance.game_type == 'hard':
		session_instance.broker_starting_balance = 12000
		session_instance.producer_starting_balance = 6000


def save(self, *args, **kwargs):
	if not self.pk:
		initialize_game_settings(SessionModel, self.id)
		super(SessionModel, self).save(*args, **kwargs)
	if self.status == 'initialized':
		super().save(*args, **kwargs)
	if self.status == 'created':
		try:
			distribute_roles(SessionModel, self.id)
			create_role_models(SessionModel, self.pk)
			self.crown_balance = self.broker_starting_balance * self.number_of_brokers / 4
			self.current_turn = 1
			self.status = 'started'
		except Exception as e:
			print(e)
			self.status = 'initialized'
		super().save(*args, **kwargs)
	if self.status == 'started':
		if 0 < self.current_turn < self.turn_count:
			if self.turn_phase == 'negotiation':
				self.turn_phase = 'transaction'
			else:
				self.crown_balance = change_game_parameters(SessionModel, self.id)
				self.current_turn += 1
				for player in self.player.all():
					player.ended_turn = False
					player.save()
				transaction_denier(self)
		if self.current_turn == self.turn_count:
			self.status = 'finished'
		super().save(*args, **kwargs)
	if self.status == 'finished':
		super().save(*args, **kwargs)