from django.apps import apps
from django.conf import settings

def get_session_model():
    app, model = settings.SESSION_MODEL.split('.')
    return apps.get_model(app, model, require_ready=True)

def get_player_model():
    app, model = settings.PLAYER_MODEL.split('.')
    return apps.get_model(app, model, require_ready=True)