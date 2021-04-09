from rest_framework import serializers
from .models import PlayerModel, PlayerTokenModel
from game.models import SessionModel


class PlayerCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    # session = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        # session_id = validated_data.pop('session')
        # session_instance = SessionModel.objects.get(id=session_id)
        player = PlayerModel.objects.create_player(validated_data)
        player.save()
        PlayerTokenModel.objects.create(player=player)
        return player.objects.get().annotate(
            auth_token='token.key'
        )


    def update(self, instance, validated_data):
        pass


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

# class TokenSerializer(serializers.Serializer):
#     username
#     def create(self, validated_data):
#         pass
