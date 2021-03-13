class TransactionNormal:
    def __init__(self, producer: object, broker: object, terms: dict):
        self.producer = producer
        self.broker = broker
        self.terms = terms

    transaction_limit = 2000

    def approve_by_limit(self) -> bool:
        return self.terms['quantity'] * self.terms['price'] < self.transaction_limit

    def form_transaction(self) -> dict:
        if self.approve_by_limit():
            deal = {
                'producer': self.producer,
                'broker': self.broker,
                'terms': self.terms
            }
            return deal
        deal = {
            'producer': self.producer,
            'broker': self.broker,
            'terms': {
                'quantity': 0,
                'price': 0,
                'transporting_cost': self.terms['transporting_cost']
            }
        }
        return deal
