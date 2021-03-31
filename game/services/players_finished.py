from ..models import SessionModel

def players_finished(session_instance):
    players_count = session_instance.player.count()
    players_finished_turn = session_instance.player.filter(ended_turn=True).count()
    print('fin', players_finished_turn, players_count)
    if players_count == players_finished_turn:
        session_instance.save()
        print(session_instance.current_turn)
