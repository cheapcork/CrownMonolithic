# from .utils import get_player
from .models import PlayerTokenModel
from django.utils.deprecation import MiddlewareMixin


class PlayerAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            player = PlayerTokenModel.objects.get(key=token).player
            request.player = player
        except KeyError:
            print('no token')
        except PlayerTokenModel.DoesNotExists:
            print('not a player')