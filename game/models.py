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


class Session(models.Model):
    name = models.CharField(max_length=150)
    game_type = models.CharField(max_length=15, choices=GAME_TYPES, default='normal')
    number_of_players = models.CharField(max_length=20, choices=PLAYER_NUMBER_PRESET, default='12-14')
    number_of_brokers = models.PositiveSmallIntegerField(default=3)
    turn_count = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=15, choices=SESSION_STATUSES, default='created')
    broker_starting_balance = models.PositiveSmallIntegerField()
    producer_starting_balance = models.PositiveSmallIntegerField()
    transaction_limit = models.PositiveSmallIntegerField(default=2000)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.game_type == 'normal':
                if self.number_of_players == '12-14':
                    self.broker_starting_balance = 8000
                    self.producer_starting_balance = 4000
                else:
                    self.broker_starting_balance = 12000
                    self.producer_starting_balance = 6000
            elif self.game_type == 'hard':
                self.broker_starting_balance = 12000
                self.producer_starting_balance = 6000
        super(Session, self).save(*args, **kwargs)


class Player(models.Model):
    nickname = models.CharField(max_length=150)
    session = models.ManyToManyField(Session, on_delete=models.CASCADE, related_name='player')
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль')
    position = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Producer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='producer')
