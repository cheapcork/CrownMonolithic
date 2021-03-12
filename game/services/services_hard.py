"""
Расчёт игровых параметров на начало хода версии Hard.
Данный алгоритм импортирует классы Короны, маклера, производителя, и производит расчёт согласно утверждённой логике.
"""
from .crown import Crown
from .producer import ProducerHard as Manufacturer
from .broker import Broker


def count_manufacturer_hard(manufacturer, set_machine: tuple, set_production: tuple, deals: list):
    """Подсчёт результата хода для производителя"""
    manufacturer.update_machine(set_machine[0], set_machine[1])
    manufacturer.produce(set_production[0], set_production[1])
    for deal in deals:
        manufacturer.make_deal(deal)

    costs_production = manufacturer.count_fixed_costs() + manufacturer.count_variable_costs()
    costs_trading = manufacturer.count_logistics_costs() + manufacturer.count_negotiation_costs()
    proceeds = manufacturer.count_proceeds()
    costs_storage = manufacturer.count_storage_costs()

    balance_1 = manufacturer.balance - costs_production
    balance_2 = balance_1 - costs_trading
    balance_3 = balance_2 + proceeds
    balance_4 = balance_3 - costs_storage
    manufacturer.balance = balance_4
    return print(f'{manufacturer} был пересчитан. баланс на начало хода - {manufacturer.balance}')


man = Manufacturer(6000)
machine = (0.5, 2)
production = (20, 0.5)
trades = [{
    'manufacturer': None,
    'broker': None,
    'terms': {
        'billets': (10, 0.5, 0.5),
        'price': 160,
        'transporting_cost': 10
    }
},
    {
    'manufacturer': None,
    'broker': None,
    'terms': {
        'billets': (10, 0.5, 1),
        'price': 100,
        'transporting_cost': 20
    }
}
]

# count_manufacturer_hard(man, machine, production, trades)

