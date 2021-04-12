from django.test import TestCase
from .models import PlayerModel, PlayerTokenModel
from .serializers import PlayerSerializer, PlayerCreateSerializer
import json


# Create your tests here.

class PlayerAuthTest(TestCase):
    player_data = {
        'username': 'player1',
    }
    # @classmethod
    # def setUpTestData(cls):
    #     pass

    def test_player_serializer(self):
        player_serializer = PlayerCreateSerializer(data=self.player_data, many=False)
        assert player_serializer.is_valid(), player_serializer.errors
        player = player_serializer.save()
        # player = player_serializer.data

        # print(type(player), player.auth_token)
        self.assertEqual(player.username, 'player1')
