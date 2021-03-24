from rest_framework import serializers
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel


class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayerModel
		fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
	player = PlayerSerializer(many=True, read_only=True)
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
			'player',
		]
		read_only = [
			'id',
			'game_type',
			'number_of_brokers',
			'player',
		]

	def get_session_players(self, instance):
		return PlayerSerializer(
			instance.player.all(),
			many=True
		)


class ProducerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProducerModel
		fields = '__all__'


class BrokerSerializer(serializers.ModelSerializer):
	class Meta:
		model = BrokerModel
		fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransactionModel
		fields = '__all__'