"""
Расчёт игровых параметров на начало хода
"""


class Crown:
    def __init__(self, balance):
        self.crown_balance = balance
        self.balance_spruce = self.crown_balance * 45.1220
        self.balance_oak = self.crown_balance * 41.9512
        self.balance_redwood = self.crown_balance * 12.9268

    def count_market_price(self, number_of_billets) -> int:
        """Считает рыночную стоимость заготовок"""
        market_price = self.crown_balance / number_of_billets
        return market_price

    def update_balance(self) -> None:
        """Обновляет баланс Короны в зависимости от состояния рынка"""
        # TODO Узнать, как происходит обновление состояния рынка
        pass


class Manufacturer:
    # TODO можно развести роли маклера и производителя в БД по разным моделям,
    #  а у моделей игроков сделать ссылки на модели
    #  Пусть модели обрабатывают свои данные сами, а финальный результат будет отфильтрован и отсортирован

    def __init__(self, balance):
        self.balance = balance
        self.is_bankrupt = False
        # Заготовки определяются двумя значениями: (количество, общее качество)
        # FIXME Нужно понять, каким образом делить общее качество заготовок и качество материала
        self.billets_produced = (0, 0)
        self.billets_stored = [(0, 0)]
        # FIXME подстроить под переключение между режимами
        # Станки производителей определяются: (качество, срок аренды)
        self.machine = (0, 0)
        self.transactions = []

    def count_fixed_costs(self) -> float:
        """ Считает постоянные затраты"""
        # TODO Добавить зависимость от срока аренды станка
        rent_coefficient = 0.93 ** self.machine[1]
        base_fixed_costs = 600
        # Для китайских станков
        if self.machine[0] == 0.5:
            if self.billets_produced[0] <= 10:
                return base_fixed_costs + 200
            elif self.billets_produced[0] <= 20:
                return base_fixed_costs + 350
            elif self.billets_produced[0] <= 30:
                return base_fixed_costs + 500
            elif self.billets_produced[0] <= 50:
                return base_fixed_costs + 700
            else:
                raise AttributeError
        # Для корейских станков
        elif self.machine[0] == 0.6:
            if self.billets_produced[0] <= 10:
                return base_fixed_costs + 350
            elif self.billets_produced[0] <= 20:
                return base_fixed_costs + 600
            elif self.billets_produced[0] <= 30:
                return base_fixed_costs + 1000
            elif self.billets_produced[0] <= 50:
                return base_fixed_costs + 1400
            else:
                raise AttributeError
        # Для немецких станков
        elif self.machine[0] == 1:
            if self.billets_produced[0] <= 10:
                return base_fixed_costs + 500
            elif self.billets_produced[0] <= 20:
                return base_fixed_costs + 900
            elif self.billets_produced[0] <= 30:
                return base_fixed_costs + 1300
            elif self.billets_produced[0] <= 50:
                return base_fixed_costs + 1700
            else:
                raise AttributeError

    quality_list = [(0.25, 0.3, 0.5), (0.35, 0.42, 0.7), (0.5, 0.6, 1)]

    def count_variable_costs(self) -> int:
        """Считает переменные затраты. Затраты на материалы и переменные затраты на производство совмещены"""
        if self.billets_produced[1] in self.quality_list[0]:
            if self.billets_produced[0] <= 10:
                return 80 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 75 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 70 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 65 * self.billets_produced[0]
            else:
                raise AttributeError
        elif self.billets_produced[1] in self.quality_list[1]:
            if self.billets_produced[0] <= 10:
                return 110 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 100 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 90 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 80 * self.billets_produced[0]
            else:
                raise AttributeError
        elif self.billets_produced[1] in self.quality_list[2]:
            if self.billets_produced[0] <= 10:
                return 160 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 150 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 135 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 110 * self.billets_produced[0]
            else:
                raise AttributeError

    def count_negotiation_costs(self) -> int:
        """Считает цену переговоров"""
        return len(self.transactions) * 20

    # FIXME Можно ожидать баги в случае, если при обрыве одной из сделок у производителя будем считать, что
    #  остальные сделки прошли
    def count_logistics_costs(self) -> int:
        """Считает расходы на транспортировку заготовок"""
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['billets'] * transaction['terms']['transporting_cost']
        return costs

    def count_proceeds(self) -> int:
        """Считает выручку от продажи заготовок"""
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['billets'] * transaction['terms']['price']
        return proceeds

    # FIXME Может возникнуть баг, когда при производстве ели на немецком станке можно будет её толкнуть как
    #  красное дерево на китайском станке
    def make_deal(self, deal: dict) -> None:
        """Проводит сделку с неким маклером"""
        self.transactions.append(deal)
        return

    # TODO Придумать, каким образом считать оставшиеся на конец хода заготовки.
    #  Нужно придумать проверку на тип заготовок
    #  Также нужно придумать, каким образом можно хранить заготовки
    def billets_left(self) -> None:
        billets_available = []
        billets_sold = 0
        for transaction in self.transactions:
            billets_sold += transaction['terms']['billets']
        billets_available.append(self.billets_produced)
        pass

    def count_storage_costs(self) -> int:
        """Считает расходы на хранение заготовок"""
        billets_count = 0
        for billet_bunch_stored in self.billets_stored:
            billets_count += billet_bunch_stored[0]
        return billets_count * 50

    def update_machine(self, machine_quality, rent_duration) -> None:
        self.machine = (machine_quality, rent_duration)
        return

    def produce(self, billet_amount, billet_material_quality) -> None:
        """Устанавливает на производство заготовки из указанного материала"""
        billet_quality = self.machine[0] * billet_material_quality
        self.billets_produced = (billet_amount, billet_quality)
        return


def count_manufacturer(manufacturer, set_machine: tuple, set_production: tuple, deals: list):
    """Подсчёт результата хода для производителя"""
    manufacturer.update_machine(set_machine[0], set_machine[1])
    manufacturer.produce(set_production[0], set_production[1])
    for deal in deals:
        manufacturer.make_deal(deal)

    costs_production = manufacturer.count_fixed_costs() + manufacturer.count_variable_costs()
    costs_trading = manufacturer.count_logistics_costs() + manufacturer.count_negotiation_costs()
    proceeds = manufacturer.count_proceeds()
    costs_storage = manufacturer.count_storage_costs()

    balance_1 = manufacturer.balance - costs_production
    balance_2 = balance_1 - costs_trading
    balance_3 = balance_2 + proceeds
    balance_4 = balance_3 - costs_storage
    manufacturer.balance = balance_4
    return print(f'{manufacturer} был пересчитан. баланс на начало хода - {manufacturer.balance}')


man = Manufacturer(6000)
machine = (0.5, 2)
production = (20, 0.5)
trades = [{
    'manufacturer': None,
    'broker': None,
    'terms': {
        'billets': 10,
        'quality:': 0.3,
        'price': 160,
        'transporting_cost': 10
    }
},
{
    'manufacturer': None,
    'broker': None,
    'terms': {
        'billets': 10,
        'quality:': 0.3,
        'price': 100,
        'transporting_cost': 20
    }
}
]

count_manufacturer(man, machine, production, trades)
