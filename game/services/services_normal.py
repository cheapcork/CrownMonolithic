from manufacturer import Manufacturer
from broker import Broker
from crown import Crown

crown = Crown(6000)
man_1 = Manufacturer(4000)
man_2 = Manufacturer(4000)
man_3 = Manufacturer(4000)
man_4 = Manufacturer(4000)
broker_1 = Broker(8000)
broker_2 = Broker(8000)

man_1.produce(15, 'normal')
man_2.produce(10, 'normal')
man_3.produce(30, 'normal')
man_4.produce(11, 'normal')

deal_1 = {
    'terms': {
        'billets': (15, 'normal', 'normal'),
        'price': 150,
        'transporting_cost': 10
    }
}

deal_2 = {
    'terms': {
        'billets': (10, 'normal', 'normal'),
        'price': 100,
        'transporting_cost': 10
    }
}

deal_3_1 = {
    'terms': {
        'billets': (15, 'normal', 'normal'),
        'price': 50,
        'transporting_cost': 10
    }
}

deal_3_2 = {
    'terms': {
        'billets': (5, 'normal', 'normal'),
        'price': 110,
        'transporting_cost': 10
    }
}

deal_4 = {
    'terms': {
        'billets': (8, 'normal', 'normal'),
        'price': 88,
        'transporting_cost': 10
    }
}

man_1.make_deal(deal_1)
man_2.make_deal(deal_2)
man_3.make_deal(deal_3_1)
man_3.make_deal(deal_3_2)
man_4.make_deal(deal_4)

broker_1.make_deal(deal_1)
broker_2.make_deal(deal_2)
broker_1.make_deal(deal_3_1)
broker_2.make_deal(deal_3_2)
broker_2.make_deal(deal_4)

manufacturers = [man_1, man_2, man_3, man_4]
brokers = [broker_1, broker_2]
deals = [deal_1, deal_2, deal_3_1, deal_3_2, deal_4]


def count_manufacturer_normal(manufacturer):
    costs_production = manufacturer.count_fixed_costs_normal() + manufacturer.count_variable_costs_normal()
    costs_trading = manufacturer.count_logistics_costs() + manufacturer.count_negotiation_costs()
    proceeds = manufacturer.count_proceeds()
    costs_storage = manufacturer.count_storage_costs()

    balance_1 = manufacturer.balance - costs_production
    if balance_1 < 0:
        return f"{manufacturer} банкрот!"
    balance_2 = balance_1 - costs_trading
    if balance_2 < 0:
        return f"{manufacturer} банкрот!"
    balance_3 = balance_2 + proceeds
    if balance_3 < 0:
        return f"{manufacturer} банкрот!"
    balance_4 = balance_3 - costs_storage
    if balance_4 < 0:
        return f"{manufacturer} банкрот!"
    manufacturer.balance = balance_4
    manufacturer.store_billets_normal()
    billets_stored = manufacturer.billets_stored
    return f'{manufacturer} был пересчитан. Баланс: {manufacturer.balance}.На складе: {billets_stored}'


def count_broker_normal(broker, market_price):
    broker.add_shipments()
    balance_1 = broker.balance - broker.fixed_costs
    if balance_1 < 0:
        return f'{broker} банкрот!'
    balance_2 = balance_1 - broker.count_purchase_costs_normal()
    if balance_2 < 0:
        return f'{broker} банкрот!'
    broker.balance = balance_2 + broker.count_proceeds_normal(market_price)
    return f'{broker} был пересчитан. Баланс: {broker.balance}.'


def count_crown(crown_state, market_deals):
    trade_volume = 0
    for deal in market_deals:
        trade_volume += deal['terms']['billets'][0]
    return crown_state.count_market_price_normal(trade_volume)


def test_normal(mans, brs):
    for man in mans:
        print(count_manufacturer_normal(man))
    for br in brs:
        print(count_broker_normal(br, count_crown(crown, deals)))


test_normal(manufacturers, brokers)
