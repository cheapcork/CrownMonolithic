from django.utils.deprecation import MiddlewareMixin

from authorization.models import TokenModel


class PlayerAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            request.player = TokenModel.objects.get(token=token).player
        except KeyError:
            print('no token')
        except ValueError:
            print('not a player')
