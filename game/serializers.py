from rest_framework import serializers

from authorization.serializers import TokenSerializer
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel


class LobbySerializer(serializers.ModelSerializer):
	"""
	Сериализатор для юзерского вида списка сессий
	"""
	player_count = serializers.IntegerField(source='player.count', read_only=True)

	class Meta:
		model = SessionModel
		fields = [
			'id',
			'name',
			'game_type',
			'status',
			'player_count',
			'current_turn',
			'turn_phase',
		]
		read_only = [
			'__all__',
			'player_count'
		]


class SessionAdminSerializer(serializers.ModelSerializer):
	"""
	Сериализатор для администрирования запущенных сессий
	"""
	player_count = serializers.IntegerField(source='player.count', read_only=True)
	players_finished_turn = serializers.SerializerMethodField(
		source='get_players_finished_turn', read_only=True)

	class Meta:
		model = SessionModel
		fields = [
			'id',
			'name',
			'game_type',
			'turn_count',
			'number_of_brokers',
			'crown_balance',
			'status',
			'broker_starting_balance',
			'producer_starting_balance',
			'transaction_limit',
			'current_turn',
			'turn_phase',
			'player_count',
			'players_finished_turn',
		]
		read_only = [
			'__all__',
		]

	@staticmethod
	def get_session_player_count(instance):
		return PlayerSerializer(
			instance.player.all(),
			many=True
		)

	@staticmethod
	def get_players_finished_turn(instance):
		return instance.player.filter(ended_turn=True).count()


class PlayerSerializer(serializers.ModelSerializer):
	"""
	Сериализатор для игрока
	"""
	# token = serializers.SerializerMethodField('get_token_value', read_only=True)

	class Meta:
		model = PlayerModel
		fields = [
			'id',
			'session',
			'nickname',
			'role',
			'city',
			'balance',
			'ended_turn',
			'is_bankrupt',
			'status',
			'position',
		]
		read_only = [
			'id',
			'status',
			'position'
		]


class ProducerSerializer(serializers.ModelSerializer):
	transactions = serializers.SerializerMethodField('get_producer_transactions')

	class Meta:
		model = ProducerModel
		fields = [
			'player',
			'billets_produced',
			'billets_stored',
			'transactions'
		]
		read_only = [
			'player'
		]

	@staticmethod
	def get_producer_transactions(instance):
		transactions = instance.transaction.filter(
			producer=instance.id,
			turn=instance.player.session.current_turn
		)
		return TransactionSerializer(transactions, many=True).data


class BrokerSerializer(serializers.ModelSerializer):
	transactions = serializers.SerializerMethodField('get_broker_transactions')
	player_info = serializers.SerializerMethodField('get_player_info', read_only=True)

	class Meta:
		model = BrokerModel
		fields = [
			'id',
			'player_info',
			'transactions'
		]

	@staticmethod
	def get_player_info(instance):
		info = PlayerSerializer(instance.player).data
		return info

	# FIXME: optimize me, please
	@staticmethod
	def get_broker_transactions(instance):
		transactions = dict()
		transactions['active_transactions'] = TransactionSerializer(
			instance.transaction.filter(
				broker=instance.id,
				turn=instance.player.session.current_turn,
				status='active'

			),
			many=True
		).data
		for turn in range(1, instance.player.session.current_turn + 1):
			transactions[turn] = TransactionSerializer(
				instance.transaction.filter(
					broker=instance.id,
					turn=turn,
					status__in=['accepted', 'denied']
				),
				many=True
			).data

		return transactions


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransactionModel
		fields = '__all__'
		read_only = [
			'id',
			'session',
			'transporting_cost',
			'turn'
		]
		extra_kwargs = {
			'session': {
				'required': False,
			}
		}


class FullProducerInfoSerializer(serializers.ModelSerializer):
	"""
	Выдаёт полную информацию об игроке-производителе
	"""
	player_info = serializers.SerializerMethodField(source='get_player_info', read_only=True)

	class Meta:
		model = ProducerModel
		fields = [
			'id',
			'billets_produced',
			'billets_stored',
			'player_info',
		]

	@staticmethod
	def get_player_info(instance):
		"""
		Добавляет к сериализатору игрока-производителя информацию о хранилище
		"""
		return PlayerSerializer(instance.player).data
