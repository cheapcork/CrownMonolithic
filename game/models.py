from django.db import models
from game.services.db_logic_interface import change_game_parameters
from game.services.role_randomizer import distribute_roles
from game.services.get_transporting_cost import get_transporting_cost
from game.services.create_role_models import create_role_models
from authorization.models import UserModel

ROLES = (
    ('unassigned', 'Не назначена'),
    ('producer', 'Производитель'),
    ('broker', 'Маклер')
)

GAME_TYPES = (
    ('normal', 'Стандартная'),
    ('hard', 'Сложная')
)

SESSION_STATUSES = (
    ('initialized', 'Сессия инициализирована'),
    ('created', 'Сессия создана'),
    ('started', 'Сессия заполнена'),
    ('finished', 'Сессия закончилась')
)

PLAYER_NUMBER_PRESET = (
    ('12-14', '12-14 Игроков'),
    ('15-20', '15-20 Игроков'),
    ('21-25', '21-25 Игроков'),
    ('26-30', '26-30 Игроков'),
    ('31-35', '31-35 Игроков'),
)

CITIES = (
    ('unassigned', 'Не назначен'),
    ('IV', "Айво"),
    ('WS', "Вемшир"),
    ('TT', "Тортуга"),
    ('AD', "Алендор"),
    ('NF', "Неверфол"),
    ('ET', "Этруа"),)


class SessionModel(models.Model):
    """
    Модель игровой сессии вместе со всеми настройками
    """
    name = models.CharField(max_length=150)
    game_type = models.CharField(max_length=15, choices=GAME_TYPES, default='normal')
    number_of_players = models.CharField(max_length=20, choices=PLAYER_NUMBER_PRESET, default='12-14')
    turn_count = models.PositiveSmallIntegerField()

    number_of_brokers = models.PositiveSmallIntegerField(editable=False)
    crown_balance = models.PositiveSmallIntegerField(default=0, editable=False)
    status = models.CharField(max_length=15, choices=SESSION_STATUSES, default='initialized', editable=True)
    broker_starting_balance = models.PositiveSmallIntegerField(editable=False)
    producer_starting_balance = models.PositiveSmallIntegerField(editable=False)
    transaction_limit = models.PositiveSmallIntegerField(default=2000, editable=False)
    current_turn = models.PositiveSmallIntegerField(verbose_name='Текущий ход', default=0, editable=True)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def initialize_game_settings(self):
        """
        Инициализирует игровые настройки
        """
        if self.game_type == 'normal':
            if self.number_of_players == '12-14':
                if not self.number_of_brokers:
                    self.number_of_brokers = 3
                self.broker_starting_balance = 8000
                self.producer_starting_balance = 4000
            elif self.number_of_players == "15-20":
                if not self.number_of_brokers:
                    self.number_of_brokers = 4
                self.broker_starting_balance = 12000
                self.producer_starting_balance = 6000
            elif self.number_of_players == "21-25":
                if not self.number_of_brokers:
                    self.number_of_brokers = 5
                self.broker_starting_balance = 12000
                self.producer_starting_balance = 6000
            elif self.number_of_players == "26-30":
                if not self.number_of_brokers:
                    self.number_of_brokers = 6
                self.broker_starting_balance = 12000
                self.producer_starting_balance = 6000
            elif self.number_of_players == "31-35":
                if not self.number_of_brokers:
                    self.number_of_brokers = 7
                self.broker_starting_balance = 12000
                self.producer_starting_balance = 6000
        elif self.game_type == 'hard':
            self.broker_starting_balance = 12000
            self.producer_starting_balance = 6000

    def save(self, *args, **kwargs):
        if not self.pk:
            self.initialize_game_settings()
            super(SessionModel, self).save(*args, **kwargs)
        if self.status == 'initialized':
            distribute_roles(SessionModel, self.id)
            create_role_models(SessionModel, self.pk)
            self.status = 'created'
            super(SessionModel, self.save(*args, **kwargs))
        if self.status == 'created':
            self.crown_balance = self.broker_starting_balance * self.number_of_brokers / 4
            self.current_turn = 1
            super().save(*args, **kwargs)
        if self.status == 'started':
            if 1 < self.current_turn < self.turn_count:
                self.crown_balance = change_game_parameters(SessionModel, self.id)
                self.current_turn += 1
            if self.current_turn == self.turn_count:
                self.status = 'finished'
            super().save(*args, **kwargs)
        if self.status == 'finished':
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PlayerModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='player', verbose_name='Пользователь',
                             null=True)
    session = models.ForeignKey(SessionModel, on_delete=models.SET_NULL, related_name='player', verbose_name='Сессия',
                                null=True, blank=True)
    nickname = models.CharField(max_length=100, verbose_name='Никнейм', default='')

    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль', default='unassigned',
                            editable=True)
    position = models.PositiveSmallIntegerField(verbose_name='Место', default=0, editable=False)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'Игрок {self.nickname}'


class ProducerModel(models.Model):
    player = models.ForeignKey(PlayerModel, on_delete=models.SET_NULL, related_name='producer', null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.IntegerField(default=0)
    billets_produced = models.IntegerField(default=0)
    billets_stored = models.IntegerField(default=0)
    is_bankrupt = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='OK', verbose_name='Статус банкротства', editable=False)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        if self.player is not None:
            return f'Производитель {self.player.nickname}'
        else:
            return f'Производитель id {self.id}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.player.session.producer_starting_balance
        super().save(*args, **kwargs)


ProducerModel.objects.all().exclude()


class BrokerModel(models.Model):
    player = models.ForeignKey(PlayerModel, on_delete=models.SET_NULL, related_name='broker', null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.IntegerField(default=0)
    is_bankrupt = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='OK', verbose_name='Статус банкротства', editable=False)

    class Meta:
        verbose_name = 'Маклер'
        verbose_name_plural = 'Маклеры'

    def __str__(self):
        if self.player is not None:
            return f'Маклер {self.player.nickname}'
        else:
            return f'Маклер id {self.id}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.player.session.broker_starting_balance
        super().save(*args, **kwargs)


class TransactionModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name='transaction')
    producer = models.ForeignKey(ProducerModel, on_delete=models.CASCADE, related_name='transaction')
    broker = models.ForeignKey(BrokerModel, on_delete=models.CASCADE, related_name='transaction')
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveSmallIntegerField(default=0)
    transporting_cost = models.PositiveSmallIntegerField(default=10, editable=False)
    turn = models.PositiveSmallIntegerField(editable=False)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        if self.producer.player is not None and self.broker.player is not None:
            return f'Сделка в сессии {self.session.name} между {self.producer.player.nickname} ' \
               f'и {self.broker.player.nickname}'
        else:
            return f'Сделка в сессии {self.session.name} между id {self.producer.id} и id {self.broker.id}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.turn = self.session.current_turn
            self.transporting_cost = get_transporting_cost(
                self.session.number_of_brokers,
                self.producer.city,
                self.broker.city,
            )
        super().save(*args, **kwargs)
