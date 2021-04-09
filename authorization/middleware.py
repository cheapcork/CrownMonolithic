from .utils import get_player
from django.utils.deprecation import MiddlewareMixin


class PlayerAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            request.player = get_player(token)
        except KeyError:
            print('no token')
        except PlayerTokenModel.DoesNotExists:
            print('not a player')