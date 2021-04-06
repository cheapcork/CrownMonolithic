from game.services.producer import AbstractProducer


class ProducerNormal(AbstractProducer):

    def __init__(self, balance):
        self.id = 0
        self.balance = balance
        self.billets_produced = 0
        self.billets_stored = 0
        self.transactions = []
        self.is_bankrupt = False
        self.status = 'OK'

    def count_fixed_costs(self) -> float:
        if self.billets_produced <= 10:
            return 600
        elif self.billets_produced <= 20:
            return 1000
        elif self.billets_produced <= 30:
            return 1400
        elif self.billets_produced <= 50:
            return 2000
        elif self.billets_produced <= 100:
            return 4000
        else:
            return 15000

    def count_variable_costs(self) -> int:
        if self.billets_produced <= 10:
            return 110 * self.billets_produced
        elif self.billets_produced <= 20:
            return 100 * self.billets_produced
        elif self.billets_produced <= 30:
            return 85 * self.billets_produced
        elif self.billets_produced <= 50:
            return 70 * self.billets_produced
        elif self.billets_produced <= 100:
            return 60 * self.billets_produced

    def count_storage_costs(self) -> int:
        return self.billets_stored * 50

    def count_logistics_costs(self) -> int:
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['quantity'] * transaction['terms']['transporting_cost']
        return costs

    def count_negotiation_costs(self) -> int:
        return len(self.transactions) * 20

    def make_deal(self, deal: dict) -> None:
        self.transactions.append(deal)
        return

    def count_proceeds(self) -> int:
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['quantity'] * transaction['terms']['price']
        return proceeds

    @property
    def billets_left(self) -> int:
        billets_requested = 0
        for transaction in self.transactions:
            billets_requested += transaction['terms']['quantity']
        billets_left = self.billets_stored + self.billets_produced - billets_requested
        return billets_left

    def store_billets(self) -> None:
        self.billets_stored = self.billets_left
        self.billets_produced = 0
        return

    def produce(self, billet_amount) -> None:
        self.billets_produced = billet_amount
        return


