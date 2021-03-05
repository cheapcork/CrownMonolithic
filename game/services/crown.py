class Crown:
    def __init__(self, balance):
        self.crown_balance = balance
        self.balance_spruce = self.crown_balance * 45.1220
        self.balance_oak = self.crown_balance * 41.9512
        self.balance_redwood = self.crown_balance * 12.9268

    def count_market_price_normal(self, number_of_billets) -> tuple:
        """Считает рыночную стоимость заготовок для обычной версии"""
        market_price_normal = self.crown_balance / number_of_billets
        return market_price_normal

    def count_market_price_spruce(self, number_of_billets) -> tuple:
        """Считает рыночную стоимость заготовок из ели"""
        market_price_spruce = self.balance_spruce / number_of_billets
        return market_price_spruce

    def count_market_price_oak(self, number_of_billets) -> tuple:
        """Считает рыночную стоимость заготовок из дуба"""
        market_price_oak = self.balance_oak / number_of_billets
        return market_price_oak

    def count_market_price_redwood(self, number_of_billets) -> tuple:
        """Считает рыночную стоимость заготовок из красного дерева"""
        market_price_redwood = self.balance_redwood / number_of_billets
        return market_price_redwood

    def update_balance(self) -> None:
        """Обновляет баланс Короны в зависимости от состояния рынка"""
        # TODO Узнать, как происходит обновление состояния рынка
        pass

