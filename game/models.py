from django.db import models

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
    ('Neverfall', "Неверфол"),
    ('Tortuga', "Тортуга"),
    ('Wemshire', "Вемшир"),
    ('Ivo', "Айво"),
    ('Alendor', "Алендор"),
    ('Etroi', "Этруа"),)


class Session(models.Model):
    """
    Модель игровой сессии вместе со всеми настройками
    """
    name = models.CharField(max_length=150)
    game_type = models.CharField(max_length=15, choices=GAME_TYPES, default='normal')
    number_of_players = models.CharField(max_length=20, choices=PLAYER_NUMBER_PRESET, default='12-14')
    number_of_brokers = models.PositiveSmallIntegerField(editable=False)
    turn_count = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=15, choices=SESSION_STATUSES, default='created', editable=False)
    broker_starting_balance = models.PositiveSmallIntegerField(editable=False)
    producer_starting_balance = models.PositiveSmallIntegerField(editable=False)
    transaction_limit = models.PositiveSmallIntegerField(default=2000, editable=False)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    # TODO
    #  Придумать, каким образом менять статусы сессии
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
        super().save(*args, **kwargs)

class Player(models.Model):
    nickname = models.CharField(max_length=150)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='player')
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль')
    position = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Producer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='producer')
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.PositiveIntegerField()
    billets_produced = models.PositiveIntegerField()
    billets_stored = models.PositiveIntegerField()
    # FIXME подключить Postgres, чтобы можно было пользоваться полем
    #  На самом деле, даже не факт, что это поле нам понадобится
    #  transactions = models.JSONField()
    is_bankrupt = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Broker(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='broker')
    city = models.CharField(max_length=20, choices=CITIES, verbose_name='Расположение')
    balance = models.PositiveIntegerField()
    is_bankrupt = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Маклер'
        verbose_name_plural = 'Маклеры'
