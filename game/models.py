from django.db import models
from game.services.db_logic_interface import change_game_parameters

ROLES = (
    ('producer', 'Производитель'),
    ('broker', 'Маклер')
)

GAME_TYPES = (
    ('normal', 'Стандартная'),
    ('hard', 'Сложная')
)

SESSION_STATUSES = (
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
    ('NF', "Неверфол"),
    ('TT', "Тортуга"),
    ('WS', "Вемшир"),
    ('IV', "Айво"),
    ('AD', "Алендор"),
    ('ET', "Этруа"),)

DISTANCES = (

)


class SessionModel(models.Model):
    """
    Модель игровой сессии вместе со всеми настройками
    """
    name = models.CharField(max_length=150)
    game_type = models.CharField(max_length=15, choices=GAME_TYPES, default='normal')
    number_of_players = models.CharField(max_length=20, choices=PLAYER_NUMBER_PRESET, default='12-14')
    number_of_brokers = models.PositiveSmallIntegerField(editable=False)
    crown_balance = models.PositiveSmallIntegerField(editable=False, default=0)
    turn_count = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=15, choices=SESSION_STATUSES, default='created', editable=True)
    broker_starting_balance = models.PositiveSmallIntegerField(editable=False)
    producer_starting_balance = models.PositiveSmallIntegerField(editable=False)
    transaction_limit = models.PositiveSmallIntegerField(default=2000, editable=False)
    current_turn = models.PositiveSmallIntegerField(verbose_name='Текущий ход', default=0, editable=True)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def save(self, *args, **kwargs):
        # Настройка начальных параметров сессии в зависимости от количества игроков
        if not self.pk:
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
        if self.status == 'created':
            self.status = 'started'
            self.crown_balance = self.broker_starting_balance * self.number_of_brokers / 4
            super().save(*args, **kwargs)
        if self.status == 'started':
            change_game_parameters(SessionModel, self.id)
            if self.current_turn < self.turn_count:
                self.current_turn += 1
            else:
                self.status = 'finished'
            super().save(*args, **kwargs)
        if self.status == 'finished':
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PlayerModel(models.Model):
    nickname = models.CharField(max_length=150, verbose_name='Ник пользователя')
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name='player', verbose_name='Сессия')
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль')
    position = models.PositiveSmallIntegerField(verbose_name='Место', editable=False, default=0)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'Игрок {self.nickname}'


class ProducerModel(models.Model):
    player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='producer',
                               limit_choices_to={'role': 'producer'})
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.PositiveIntegerField(default=0)
    billets_produced = models.PositiveIntegerField(default=0)
    billets_stored = models.PositiveIntegerField(default=0)
    is_bankrupt = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f'Производитель {self.player.nickname}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.player.session.producer_starting_balance
        super().save(*args, **kwargs)


class BrokerModel(models.Model):
    player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='broker',
                               limit_choices_to={'role': 'broker'})
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.PositiveIntegerField(default=0)
    is_bankrupt = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Маклер'
        verbose_name_plural = 'Маклеры'

    def __str__(self):
        return f'Маклер {self.player.nickname}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.player.session.broker_starting_balance
        super().save(*args, **kwargs)


class TransactionModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name='transaction')
    turn = models.PositiveSmallIntegerField()
    producer = models.ForeignKey(ProducerModel, on_delete=models.CASCADE, related_name='transaction')
    broker = models.ForeignKey(BrokerModel, on_delete=models.CASCADE, related_name='transaction')
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveSmallIntegerField(default=0)
    transporting_cost = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'Сделка в сессии {self.session.name} между {self.producer.player.nickname} ' \
               f'и {self.broker.player.nickname}'
