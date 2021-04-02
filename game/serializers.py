from rest_framework import serializers
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	player = serializers.SerializerMethodField('get_player')

	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'player',
		]
		read_only = [
			'id',
			'username',
			'player',
		]

	def get_player(self, instance):
		try:
			return PlayerSerializer(instance.player.get(), many=False).data
		except PlayerModel.DoesNotExist:
			return None


class PlayerSerializer(serializers.ModelSerializer):
	role_info = serializers.SerializerMethodField('get_role_info')
	class Meta:
		model = PlayerModel
		fields = [
			'id',
			'user',
			'nickname',
			'role',
			'role_info',
			'session',
			'user',
		]
		read_only = [
			'id',
		]

	def get_role_info(self, instance):
		role_classes = {
			'broker': {'model': BrokerModel, 'serializer': BrokerFullSerializer},
			'producer': {'model': ProducerModel, 'serializer': ProducerSerializer}
		}
		if instance.role == 'unassigned':
			return 'unassigned'

		model = role_classes[instance.role]['model'].objects.get(player=instance.id)
		return role_classes[instance.role]['serializer'](model).data


# class PlayerSessionSerializer(serializers.ModelSerializer):
# 	player = PlayerSerializer(many=True, read_only=True)
# 	me = serializers.SerializerMethodField('get_my_info')
# 	class Meta:
# 		model = SessionModel
# 		fields = [
# 			'id',
# 			'name',
# 			'game_type',
# 			'number_of_players',
# 			'turn_count',
# 			'status',
# 			'current_turn',
# 			'player',
# 			'me',
# 		]
#
# 	def get_my_info(self, obj):
# 		role = obj.player.get(pk=self.context['user'].id).role
# 		if role == 'broker':
# 			model = BrokerModel.objects.get(user=self.context['user'].id)
# 			return BrokerSerializer(model).data
# 		elif role == 'producer':
# 			model = ProducerModel.objects.get(user=self.context['user'].id)
# 			return ProducerSerializer(model).data
# 		return role


class SessionLobbySerializer(serializers.ModelSerializer):
	players = serializers.IntegerField(source='player.count', read_only=True)
	players_finished_turn = serializers.SerializerMethodField(
		source='get_players_finished_turn', read_only=True)
	class Meta:
		model = SessionModel
		fields = [
			'id',
			'name',
			'game_type',
			'number_of_players',
			'turn_count',
			'number_of_brokers',
			'crown_balance',
			'status',
			'broker_starting_balance',
			'producer_starting_balance',
			'transaction_limit',
			'current_turn',
			'turn_phase',
			'players',
			'players_finished_turn',
		]
		read_only = [
			'id',
			'game_type',
			'number_of_brokers',
			'players',
			'players_finished_turn',
		]

	def get_session_players(self, instance):
		return PlayerSerializer(
			instance.player.all(),
			many=True
		)

	def get_players_finished_turn(self, instance):
		return instance.player.filter(ended_turn=True).count()

class SessionListSerializer(serializers.ModelSerializer):
	players = serializers.IntegerField(source='player.count', read_only=True)
	class Meta:
		model = SessionModel
		fields = [
			'id',
			'name',
			'status',
			'players'
		]
		read_only = [
			'id',
			'name',
			'status',
			'players'
		]


class SessionGameSerializer(serializers.ModelSerializer):
	me = serializers.SerializerMethodField('get_player')
	players_finished_turn = serializers.SerializerMethodField(
		source='get_players_finished_turn', read_only=True)
	class Meta:
		model = SessionModel
		fields = [
			'id',
			'name',
			'status',
			'current_turn',
			'turn_phase',
			'me',
			'players_finished_turn'
		]
		read_only = [
			'id',
			'name',
			'status',
			'current_turn',
			'turn_phase',
			'me',
			'players_finished_turn'
		]

	def get_player(self, instance):
		player = instance.player.filter(user=self.context['user'].id)
		if player.exists():
			return PlayerSerializer(player.get(), many=False).data
		return "You are not in this session!"

	def get_players_finished_turn(self, instance):
		return instance.player.filter(ended_turn=True).count()


class ProducerSerializer(serializers.ModelSerializer):
	transactions = serializers.SerializerMethodField('get_producer_transactions')
	class Meta:
		model = ProducerModel
		fields = [
			'id',
			'city',
			'balance',
			'billets_produced',
			'billets_stored',
			'is_bankrupt',
			'status',
			'transactions'
		]
		read_only = [
			'id',
			'city',
			'balance',
			'billets_produced',
			'billets_stored',
			'is_bankrupt',
			'status',
			'transactions'
		]

	def get_producer_transactions(self, instance):
		transactions = instance.transaction.filter(
			producer=instance.id,
			turn=instance.player.session.current_turn
		)
		return TransactionSerializer(transactions, many=True).data


class BrokerLittleSerializer(serializers.ModelSerializer):
	class Meta:
		model = BrokerModel
		fields = [
			'id',
			'player',
			'city',
			'is_bankrupt',
		]
		read_only = [
			'id',
			'player',
			'city',
			'is_bankrupt',
		]


class BrokerFullSerializer(serializers.ModelSerializer):
	transactions = serializers.SerializerMethodField('get_broker_transactions')
	crown_balance = serializers.IntegerField(source='player.session.crown_balance')
	class Meta:
		model = BrokerModel
		fields = [
			'id',
			'city',
			'balance',
			'crown_balance',
			'is_bankrupt',
			'status',
			'transactions',
		]
		read_only = [
			'id',
			'city',
			'balance',
			'crown_balance',
			'is_bankrupt',
			'status',
			'transactions',
		]

	# FIXME: optimize me, please
	def get_broker_transactions(self, instance):
		transactions = {}
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
		fields = [
			'id',
			'session',
			'producer',
			'broker',
			'quantity',
			'price',
			'transporting_cost',
			'turn',
			'status'
		]
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