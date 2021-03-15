from django.contrib import admin
from .models import Session, Player, Producer, Broker

admin.site.register(Session)
admin.site.register(Player)
admin.site.register(Producer)
admin.site.register(Broker)
