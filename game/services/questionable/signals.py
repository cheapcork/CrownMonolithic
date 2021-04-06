from .models import SessionModel
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .views_ws import sessions_update


@receiver([post_save, post_delete], sender=SessionModel)
def session_list_updated(sender, **kwargs):
    print('Signal! from', kwargs['instance'], kwargs)
    sessions_update()
