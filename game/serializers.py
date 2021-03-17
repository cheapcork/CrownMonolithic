from rest_framework.serializers import ModelSerializer
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel


class SessionSerializer(ModelSerializer):
	class Meta:
		model = SessionModel
		fields = '__all__'


class PlayerSerializer(ModelSerializer):
	class Meta:
		model = PlayerModel
		fields = '__all__'


class ProducerSerializer(ModelSerializer):
	class Meta:
		model = ProducerModel
		fields = '__all__'


class BrokerSerializer(ModelSerializer):
	class Meta:
		model = BrokerModel
		fields = '__all__'
