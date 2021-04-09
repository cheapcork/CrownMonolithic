from django.test import TestCase
from .models import PlayerModel, PlayerTokenModel
from .serializers import PlayerSerializer, PlayerCreateSerializer

# Create your tests here.

class PlayerAuthTest(TestCase):
    player_data = {
        'username': 'player1',
    }
    @classmethod
    def setUpTestData(cls):
        pass

    def player_serializer_test(self):
        player_serializer = PlayerCreateSerializer(data=self.player_data)
        assert not player_serializer.is_valid()
        player = player_serializer.save()
