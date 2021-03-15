from rest_framework.serializers import ModelSerializer
from .models import Session, Player, Producer, Broker


class SessionSerializer(ModelSerializer):
	class Meta:
		model = Session
		fields = '__all__'


class PlayerSerializer(ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'


class ProducerSerializer(ModelSerializer):
	class Meta:
		model = Producer
		fields = '__all__'


class BrokerSerializer(ModelSerializer):
	class Meta:
		model = Broker
		fields = '__all__'
