from rest_framework import serializers
from .models import PlayerTokenModel
from django.conf import settings
from CrownMonolithic.utils import get_player_model, get_session_model


class PlayerCreateSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=100)
    session = serializers.IntegerField()

    def create(self, validated_data):
        player, token = get_player_model().objects.create_player(validated_data)
        return PlayerWithTokenSerializer(player).data

    def update(self, instance, validated_data):
        pass


class PlayerWithTokenSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=100)
    auth_token = serializers.CharField(source='token.key', max_length=100, read_only=True)

    class Meta:
        model = get_player_model()
        fields = [
            'id',
            'nickname',
            'session',
            'auth_token',
        ]


class PlayerSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=100)

    class Meta:
        model = get_player_model()
        fields = [
            'id',
            'nickname',
            'session',
        ]
