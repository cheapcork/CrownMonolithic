class AbstractBroker:

    material = {
        'spruce': 0.5,
        'oak': 0.7,
        'redwood': 1
    }

    machine_quality = {
        'chinese': 0.5,
        'korean': 0.6,
        'german': 1
    }

    def add_shipments(self) -> None:
        """Отправляет заготовки на продажу Короне"""
        pass

    def make_deal(self, deal: dict) -> None:
        """Совершает сделку с производителем"""
        pass
