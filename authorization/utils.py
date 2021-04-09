from .models import PlayerTokenModel
from CrownMonolithic.utils import get_player_model


def get_player(token):
    """
    :param token: токен игрока
    :return: Объект игрока
    """
    try:
        return PlayerTokenModel.objects.get(key=token).player
    except PlayerTokenModel.DoesNotExists:
        raise ValueError('No such player!')