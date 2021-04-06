from game.models import SessionModel, UserModel, PlayerModel
from game.serializers import SessionLobbySerializer, SessionGameSerializer, PlayerSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


"""
Simple func, HttpResponse for sockets. Need to work
"""


def ws_response(type_event, data) -> object:
    return {
        'type': type_event,
        'data': data
    }


def sessions_update():
    sessions = SessionModel.objects.filter(status='initialized')
    async_to_sync(get_channel_layer().group_send)(
        'search_for_session',
        {
            'type': 'sessions',
            'data': SessionLobbySerializer(sessions, many=True).data
        }
    )


def change_group(user_id=None, old_group=None, new_group=None):
    assert user_id, 'No user!'
    assert UserModel.objects.filter(id=user_id), 'No user!'
    assert old_group, 'No old group!'
    assert new_group, 'No new group!'

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_discard)('user_{}'.format(user_id), old_group)
    async_to_sync(channel_layer.group_add)('user_{}'.format(user_id), new_group)


def join_session(user, session_pk):
    try:
        session_instance = SessionModel.objects.get(pk=session_pk)
    except SessionModel.DoesNotExist:
        return ws_response('error', {'error': 'No such session!'})

    try:
        player_instance = PlayerModel.objects.get(user=user.id)
        if player_instance.session.id == session_instance.id:
            return ws_response('error', {'error': 'You\'ve already joined this session!'})
        elif not player_instance.session.id == 0:
            return ws_response('error', {'error': 'You\'ve already joined another session!'})
    except PlayerModel.DoesNotExist:
        player_serialized = PlayerSerializer(data={
            'nickname': user.username,
            'user': user.id,
            'session': session_instance.id,
        })
        if not player_serialized.is_valid():
            return ws_response('error', {'error': player_serialized.errors})
        player_serialized.save()
        session_serializer = SessionGameSerializer(
            session_instance,
            context={'user': user}
        )
        change_group(user.id, 'search_for_session', 'game_{}'.format(session_serializer.data.id))
        return ws_response('session', session_serializer.data)


def leave_session(user, session):
    pass
