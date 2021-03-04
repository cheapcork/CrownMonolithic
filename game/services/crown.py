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

