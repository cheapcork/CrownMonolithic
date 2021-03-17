from django.contrib import admin
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel

admin.site.register(SessionModel)
admin.site.register(PlayerModel)
admin.site.register(ProducerModel)
admin.site.register(BrokerModel)
admin.site.register(TransactionModel)
