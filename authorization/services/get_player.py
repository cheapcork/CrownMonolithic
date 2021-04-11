from authorization.models import PlayerTokenModel


def get_player_from_token(token):
    """
    :param token: токен игрока
    :return: Объект игрока
    """
    try:
        return PlayerTokenModel.objects.get(key=token).player
    except PlayerTokenModel.DoesNotExist:
        raise ValueError('No such player!')
