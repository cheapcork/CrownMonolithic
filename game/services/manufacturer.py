class Manufacturer:
    # TODO можно развести роли маклера и производителя в БД по разным моделям,
    #  а у моделей игроков сделать ссылки на модели
    #  Пусть модели обрабатывают свои данные сами, а финальный результат будет отфильтрован и отсортирован

    def __init__(self, balance):
        self.balance = balance
        # FIXME Возможен баг, когда вместо числа методы будут отдавать умноженные строки
        self.billets_produced = (0, 0, 0)
        self.billets_stored = []
        self.machine = (0, 0)
        # Предполагается, что данные транзакции прошли все необходимые проверки, как то:
        # 1) На сумму сделки
        # 2) На наличие заготовок у производителя
        # 3) На наличие денег у маклера
        self.transactions = []

    # (Ель, Дуб, Красное дерево)
    material = {
        'spruce': 0.5,
        'oak': 0.7,
        'redwood': 1
    }

    def count_fixed_costs_hard(self) -> float:
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

    def count_fixed_costs_normal(self) -> float:
        """Считает постоянные затраты производителя в обычной игре"""
        if self.billets_produced[1] != 'normal':
            raise AttributeError
        if self.billets_produced[0] <= 10:
            return 600
        elif self.billets_produced[0] <= 20:
            return 1000
        elif self.billets_produced[0] <= 30:
            return 1400
        elif self.billets_produced[0] <= 50:
            return 2000
        elif self.billets_produced[0] <= 100:
            return 4000

    def count_variable_costs_hard(self) -> int:
        """Считает переменные затраты согласно материалу, из которого производятся заготовки"""
        if type(self.billets_produced[1]) != int:
            raise AttributeError
        if self.billets_produced[1] == self.material['spruce']:
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
        elif self.billets_produced[1] == self.material['oak']:
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
        elif self.billets_produced[1] == self.material['redwood']:
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

    def count_variable_costs_normal(self) -> int:
        """Считает переменные затраты производителя в обычной игре"""
        if self.billets_produced[1] != 'normal':
            raise AttributeError
        if self.billets_produced[0] <= 10:
            return 110 * self.billets_produced[0]
        elif self.billets_produced[0] <= 20:
            return 100 * self.billets_produced[0]
        elif self.billets_produced[0] <= 30:
            return 85 * self.billets_produced[0]
        elif self.billets_produced[0] <= 50:
            return 70 * self.billets_produced[0]
        elif self.billets_produced[0] <= 100:
            return 60 * self.billets_produced[0]

    def count_negotiation_costs(self) -> int:
        """Считает цену переговоров"""
        return len(self.transactions) * 20

    # FIXME Можно ожидать баги в случае, если при обрыве одной из сделок у производителя
    #  будем считать, что остальные сделки прошли успешно. В таком случае нужно будет добавлять пересчёт
    #  производителя с учётом новых параметров
    def count_logistics_costs(self) -> int:
        """Считает расходы на транспортировку заготовок. Для нормала работает таким же образом"""
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['billets'][0] * transaction['terms']['transporting_cost']
        return costs

    def count_proceeds(self) -> int:
        """Считает выручку от продажи заготовок"""
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['billets'][0] * transaction['terms']['price']
        return proceeds

    def make_deal(self, deal: dict) -> None:
        """Проводит сделку с неким маклером"""
        self.transactions.append(deal)
        return

    # TODO Придумать, каким образом считать оставшиеся на конец хода заготовки.
    #  Нужно придумать проверку на тип заготовок
    #  Также нужно придумать, каким образом можно хранить заготовки
    def store_billets_hard(self) -> None:
        pass

    @property
    def billets_left_hard(self) -> int:
        billets_left = []
        billets_available = [self.billets_produced]
        for billet_type in self.billets_stored:
            billets_available.append(billet_type)
        billets_requested = []
        for transaction in self.transactions:
            billets_requested.append(transaction['terms']['billets'])

        spruce_billets_available_indexes = [index for index, material_value in enumerate(billets_available)
                                            if material_value[0] == self.material['spruce']]
        oak_billets_available_indexes = [index for index, material_value in enumerate(billets_available)
                                         if material_value[0] == self.material['oak']]
        redwood_billets_available_indexes = [index for index, material_value in enumerate(billets_available)
                                             if material_value[0] == self.material['redwood']]
        spruce_billets_requested_indexes = [index for index, material_value in enumerate(billets_requested)
                                            if material_value[0] == self.material['spruce']]
        oak_billets_requested_indexes = [index for index, material_value in enumerate(billets_requested)
                                         if material_value[0] == self.material['oak']]
        redwood_billets_requested_indexes = [index for index, material_value in enumerate(billets_requested)
                                             if material_value[0] == self.material['redwood']]
        pass

    @property
    def billets_left_normal(self) -> int:
        if self.billets_produced[1] != 'normal':
            raise AttributeError
        billets_available = self.billets_produced[0]
        if self.billets_stored:
            billets_available += self.billets_stored[0][0]
        billets_requested = 0
        for transaction in self.transactions:
            billets_requested += transaction['terms']['billets'][0]
        billets_left = billets_available - billets_requested
        return billets_left

    def store_billets_normal(self) -> None:
        """Складывает непроданные производителем заготовки на склад"""
        if self.billets_produced[1] != 'normal':
            raise AttributeError
        if self.billets_left_normal > 0:
            if self.billets_stored:
                self.billets_stored[0][0] = self.billets_left_normal
                return
            else:
                self.billets_stored.append((self.billets_left_normal, 'normal', 'normal'))
        return

    def count_storage_costs(self) -> int:
        """Считает расходы на хранение заготовок"""
        billet_count = 0
        for billet_bunch_stored in self.billets_stored:
            billet_count += billet_bunch_stored[0]
        return billet_count * 50

    def update_machine(self, machine_quality, rent_duration) -> None:
        self.machine = (machine_quality, rent_duration)
        return

    def produce(self, billet_amount, billet_material_quality) -> None:
        """Устанавливает на производство заготовки из указанного материала"""
        if billet_material_quality == 'normal':
            self.billets_produced = (billet_amount, 'normal', 'normal')
            return
        self.billets_produced = (billet_amount, billet_material_quality, self.machine[0])
        return


def count_manufacturer_hard(manufacturer, set_machine: tuple, set_production: tuple, deals: list):
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
        'billets': (10, 0.5, 0.5),
        'price': 160,
        'transporting_cost': 10
    }
},
    {
    'manufacturer': None,
    'broker': None,
    'terms': {
        'billets': (10, 0.5, 1),
        'price': 100,
        'transporting_cost': 20
    }
}
]

# count_manufacturer_hard(man, machine, production, trades)
