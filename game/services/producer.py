class AbstractProducer:
    # (Ель, Дуб, Красное дерево)
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

    def count_fixed_costs(self) -> float:
        """Считает постоянные затраты производителя"""
        pass

    def count_variable_costs(self) -> int:
        """Считает переменные затраты производителя"""
        pass

    def count_negotiation_costs(self) -> int:
        """Считает цену переговоров"""
        pass

    def count_logistics_costs(self) -> int:
        """Считает расходы на транспортировку заготовок"""
        pass

    def count_proceeds(self) -> int:
        """Считает выручку от продажи заготовок"""
        pass

    def make_deal(self, deal: dict) -> None:
        """Проводит сделку с неким маклером"""
        pass

    def store_billets(self) -> None:
        pass

    def billets_left(self) -> int:
        """Заготовки, оставшиеся на складе производителя"""
        pass

    def count_storage_costs(self) -> int:
        """Считает расходы на хранение заготовок"""
        pass
