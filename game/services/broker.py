class Broker:

    # TODO Можно поколдовать над методом и сделать зависимость от режима игры
    def __init__(self, balance, is_bankrupt=False):
        self.balance = balance
        self.shipments_spruce = []
        self.shipments_oak = []
        self.shipments_redwood = []
        self.is_bankrupt = is_bankrupt
        self.shipments_normal = []
        # В транзакции будут записываться только одобренные маклером сделки, которые проходят все возможные проверки
        self.transactions = []

    fixed_costs = 1000
    # FIXME Сейчас расчёт затрат и выручки по материалам идёт отдельными методами. Можно либо оставить
    #  методы, как есть, а можно объединить.
    #  Объединить их можно, если сделать склад для харда в виде кортежа из 3х списков

    def add_shipments(self) -> None:
        """Отправляет на склад маклера заготовки согласно их материалу"""
        for transaction in self.transactions:
            shipment = transaction['terms']['billets']
            if shipment[1] == 0.5:
                self.shipments_spruce.append(shipment)
                return
            elif shipment[1] == 0.7:
                self.shipments_oak.append(shipment)
                return
            elif shipment[1] == 1:
                self.shipments_redwood.append(shipment)
                return
            elif shipment[1] == 'normal':
                self.shipments_normal.append(shipment)
                return
            raise AttributeError

    def make_deal(self, deal: dict) -> None:
        self.transactions.append(deal)
        return

    def count_proceeds_spruce(self, market_price) -> float:
        """Считает выручку маклера при продаже заготовок из ели"""
        proceeds = 0
        for shipment in self.shipments_spruce:
            proceeds += shipment[0] * shipment[1] * shipment[2] * market_price
        return proceeds

    def count_proceeds_oak(self, market_price) -> float:
        """Считает выручку маклера при продаже заготовок из дуба"""
        proceeds = 0
        for shipment in self.shipments_oak:
            proceeds += shipment[0] * shipment[1] * shipment[2] * market_price
        return proceeds

    def count_proceeds_redwood(self, market_price) -> float:
        """Считает выручку маклера при продаже заготовок из красного дерева"""
        proceeds = 0
        for shipment in self.shipments_redwood:
            proceeds += shipment[0] * shipment[1] * shipment[2] * market_price
        return proceeds

    def count_proceeds_normal(self, market_price) -> float:
        """Считает выручку маклера при игре на нормал"""
        if self.shipments_normal[0][1] != 'normal':
            raise AttributeError
        proceeds = 0
        for shipment in self.shipments_normal:
            proceeds += shipment[0] * market_price
        return proceeds

    def count_purchase_costs_normal(self) -> int:
        """Считает расходы маклера на покупку заготовок"""
        if self.shipments_normal[0][1] != 'normal':
            raise AttributeError
        costs = 0
        deals = []
        for transaction in self.transactions:
            deals.append((transaction['terms']['billets'][0], transaction['terms']['price']))
        for deal in deals:
            costs += deal[0] * deal[1]
        return costs

    def count_purchase_costs_spruce(self) -> int:
        pass


