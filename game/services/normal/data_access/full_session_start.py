def start_session(session_instance, max_capacity=True):
    if max_capacity:
        min_players, max_players = session_instance.number_of_players.split('-')
        print(type(session_instance.player.count()))
        assert session_instance.player.count() == int(max_players), 'Not enough players!'
    session_instance.status = 'created'
    session_instance.save()
