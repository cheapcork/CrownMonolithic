from game.services.broker import AbstractBroker


class BrokerNormal(AbstractBroker):
    """
    Класс маклера для версии "Нормал"
    """

    def __init__(self, balance):
        self.id = 0
        self.balance = balance
        self.shipment = 0
        self.transactions = []
        self.is_bankrupt = False
        self.status = 'OK'

    fixed_costs = 1000

    def add_shipments(self) -> None:
        """
        Отправляет заготовки на транспортировку Короне
        """
        for transaction in self.transactions:
            self.shipment += transaction['terms']['quantity']
        return

    def make_deal(self, deal: dict) -> None:
        """
        Совершает сделку с производителем
        """
        self.transactions.append(deal)
        return

    def count_purchase_costs(self) -> int:
        """Считает затраты маклера на совершение сделок"""
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['quantity'] * transaction['terms']['price']
        return costs

    def count_proceeds(self, market_price) -> float:
        """Считает выручку от продажи заготовок"""
        return self.shipment * market_price

    def turn_balance_detail(self) -> dict:
        """
        Показывает детализацию баланса за ход
        """
        return {
            'purchace_costs': self.count_purchase_costs(),
            'proceeds': self.count_proceeds()
        }


transaction_example = {
    'producer': 0,
    'broker': 0,
    'terms': {
        'quantity': 0,
        'material': 0,
        'machine': ('chinese', 'oak', 3),
        'price': 0
    }
}
