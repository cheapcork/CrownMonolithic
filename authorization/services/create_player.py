from CrownMonolithic.utils import get_player_model


def create_player(session, nickname):
    """
    DAL. Создаёт модель игрока при подключении к лобби
    """
    player = get_player_model().objects.create_player(session, nickname)
    return player
