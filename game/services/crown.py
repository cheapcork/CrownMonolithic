class CrownNormal:
    def __init__(self, broker_starting_balance, num_of_brokers):
        self.balance = broker_starting_balance * num_of_brokers / 4

    def count_market_price(self, market_volume):
        """Подсчитывает рыночную стоимость одной заготовки """
        if market_volume == 0:
            return 160
        return self.balance / market_volume

    def update_balance(self, market_volume):
        """Обновляет баланс Короны на следующий ход"""
        if market_volume < 90:
            self.balance *= 1.1
        else:
            self.balance *= 0.97
        return


class CrownHard:

    cost_price = {
        'spruce': 185,
        'oak': 215,
        'redwood': 265
    }

    material_market_volume = {
        'spruce': 50,
        'oak': 40,
        'redwood': 10
    }

    def __init__(self, broker_starting_balance):
        self.starting_balance = broker_starting_balance / 4

    def count_market_prices(self, market_volume: dict) -> dict:
        """Возвращает словарь с рыночными ценами по материалам"""
        pass
