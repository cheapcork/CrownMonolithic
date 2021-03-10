class AbstractManufacturer:
    # FIXME Сделать абстрактным
    #  Method resolution order: посмотреть, как работают свойства у обычных и абстрактных классов
    def __init__(self, balance):
        self.balance = balance
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

    def count_fixed_costs(self) -> float:
        """Считает постоянные затраты производителя"""
        pass

    def count_variable_costs(self) -> int:
        """Считает переменные затраты производителя"""
        pass

    def count_negotiation_costs(self) -> int:
        """Считает цену переговоров"""
        return len(self.transactions) * 20

    def count_logistics_costs(self) -> int:
        """Считает расходы на транспортировку заготовок"""
        pass

    def count_proceeds(self) -> int:
        """Считает выручку от продажи заготовок"""
        pass

    def make_deal(self, deal: dict) -> None:
        """Проводит сделку с неким маклером"""
        self.transactions.append(deal)
        return

    def store_billets(self) -> None:
        pass

    @property
    def billets_left(self) -> int:
        """Заготовки, оставшиеся на складе производителя"""
        pass

    def count_storage_costs(self) -> int:
        """Считает расходы на хранение заготовок"""
        pass

    def update_machine(self, machine_quality, rent_duration) -> None:
        self.machine = (machine_quality, rent_duration)
        return

    def produce(self, billet_amount, billet_material_quality=None) -> None:
        """Устанавливает на производство заготовки"""
        pass


class ManufacturerNormal(AbstractManufacturer):
    # TODO Переопределить метод __init__ для нормала
    #  Скомпоновать методы по нормалу и харду, изначально задать их как абстрактные методы
    #  Хранилища на нормале работают по-другому

    def count_fixed_costs(self) -> float:
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

    def count_variable_costs(self) -> int:
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

    def count_storage_costs(self) -> int:
        billet_count = 0
        for billet_bunch_stored in self.billets_stored:
            billet_count += billet_bunch_stored[0]
        return billet_count * 50

    def count_logistics_costs(self) -> int:
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['billets'] * transaction['terms']['transporting_cost']
        return costs

    def count_proceeds(self) -> int:
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['billets'] * transaction['terms']['price']
        return proceeds

    @property
    def billets_left(self) -> int:
        billets_available = self.billets_produced[0]
        if self.billets_stored:
            billets_available += self.billets_stored[0][0]
        billets_requested = 0
        for transaction in self.transactions:
            billets_requested += transaction['terms']['billets'][0]
        billets_left = billets_available - billets_requested
        return billets_left

    def store_billets(self) -> None:
        if self.billets_left > 0:
            if self.billets_stored:
                self.billets_stored[0][0] = self.billets_left
                return
            else:
                self.billets_stored.append(self.billets_left)
        return


class ManufacturerHard(AbstractManufacturer):
    pass
