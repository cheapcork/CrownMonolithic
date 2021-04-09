from rest_framework import serializers
from .models import PlayerModel, PlayerTokenModel


class PlayerCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        player, token = PlayerModel.objects.create_player(validated_data['username'])
        return PlayerWithTokenSerializer(player).data

    def update(self, instance, validated_data):
        pass


class PlayerWithTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    auth_token = serializers.CharField(source='token.key', max_length=100, read_only=True)

    class Meta:
        model = PlayerModel
        fields = [
            'id',
            'username',
            'auth_token',
        ]


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

    class Meta:
        model = PlayerModel
        fields = [
            'id',
            'username',
        ]
