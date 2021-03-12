from producer import ProducerNormal
from broker import BrokerNormal
from crown import CrownNormal
from transaction import TransactionNormal
basic_balance = 4000
broker_balance = 8000

producer_1 = ProducerNormal(basic_balance)
producer_2 = ProducerNormal(basic_balance)
producer_3 = ProducerNormal(basic_balance)
producer_4 = ProducerNormal(basic_balance)
producer_5 = ProducerNormal(basic_balance)
producer_6 = ProducerNormal(basic_balance)
producer_7 = ProducerNormal(basic_balance)
producer_8 = ProducerNormal(basic_balance)
producer_9 = ProducerNormal(basic_balance)
producer_10 = ProducerNormal(basic_balance)

producer_1.produce(10)
producer_2.produce(12)
producer_3.produce(8)
producer_4.produce(15)
producer_5.produce(13)
producer_6.produce(14)
producer_7.produce(10)
producer_8.produce(11)
producer_9.produce(15)
producer_10.produce(16)


broker_1 = BrokerNormal(8000)
broker_2 = BrokerNormal(8000)
broker_3 = BrokerNormal(8000)

crown = CrownNormal(broker_balance)


terms_1 = {
    'quantity': 10,
    'price': 100,
    'transporting_cost': 10
}

terms_2 = {
    'quantity': 12,
    'price': 200,
    'transporting_cost': 15
}

terms_3 = {
    'quantity': 8,
    'price': 160,
    'transporting_cost': 10
}

terms_4 = {
    'quantity': 15,
    'price': 150,
    'transporting_cost': 20
}

terms_5 = {
    'quantity': 13,
    'price': 210,
    'transporting_cost': 20
}

terms_6 = {
    'quantity': 14,
    'price': 170,
    'transporting_cost': 15
}

terms_7 = {
    'quantity': 10,
    'price': 120,
    'transporting_cost': 10
}

terms_8 = {
    'quantity': 11,
    'price': 180,
    'transporting_cost': 10
}

terms_9 = {
    'quantity': 5,
    'price': 400,
    'transporting_cost': 15
}

terms_10 = {
    'quantity': 16,
    'price': 190,
    'transporting_cost': 10
}

t1 = {
    'producer': producer_1,
    'broker': broker_1,
    'terms': terms_1
}

t2 = {
    'producer': producer_2,
    'broker': broker_1,
    'terms': terms_2
}

t3 = {
    'producer': producer_3,
    'broker': broker_1,
    'terms': terms_3
}

t4 = {
    'producer': producer_4,
    'broker': broker_1,
    'terms': terms_4
}

t5 = {
    'producer': producer_5,
    'broker': broker_2,
    'terms': terms_5
}

t6 = {
    'producer': producer_6,
    'broker': broker_2,
    'terms': terms_6
}

t7 = {
    'producer': producer_7,
    'broker': broker_2,
    'terms': terms_7
}

t8 = {
    'producer': producer_8,
    'broker': broker_3,
    'terms': terms_8
}

t9 = {
    'producer': producer_9,
    'broker': broker_3,
    'terms': terms_9
}

t10 = {
    'producer': producer_10,
    'broker': broker_3,
    'terms': terms_10
}

market_transactions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

producer_1.make_deal(t1)
producer_2.make_deal(t2)
producer_3.make_deal(t3)
producer_4.make_deal(t4)
producer_5.make_deal(t5)
producer_6.make_deal(t6)
producer_7.make_deal(t7)
producer_8.make_deal(t8)
producer_9.make_deal(t9)
producer_10.make_deal(t10)
broker_1.make_deal(t1)
broker_1.make_deal(t2)
broker_1.make_deal(t3)
broker_1.make_deal(t4)
broker_2.make_deal(t5)
broker_2.make_deal(t6)
broker_2.make_deal(t7)
broker_3.make_deal(t8)
broker_3.make_deal(t9)
broker_3.make_deal(t10)

producers = [producer_1, producer_2, producer_3, producer_4, producer_5, producer_6, producer_7, producer_8, producer_9,
             producer_10]
brokers = [broker_1, broker_2, broker_3]


def count_turn(producer_list: list, broker_list: list, transaction_list: list):
    """Пересчитывает ход на нормале"""
    market_volume = 0
    for transaction in transaction_list:
        market_volume += transaction['terms']['quantity']
    market_price = crown.count_market_price(market_volume)
    # Пересчёт постоянных затрат
    for producer in producer_list:
        producer.balance -= producer.count_fixed_costs()
        if producer.balance < 0:
            print(f'{producer} is bankrupt! Fixed')
            producer_list.pop(producer_list.index(producer))
    for broker in broker_list:
        broker.balance -= broker.fixed_costs
        if broker.balance < 0:
            print(f'{broker} is bankrupt! Fixed')
            broker_list.pop(broker_list.index(broker))

    # Пересчёт переменных затрат
    for producer in producer_list:
        variable_costs_summarized = producer.count_variable_costs() + producer.count_negotiation_costs() \
                                    + producer.count_logistics_costs()
        producer.balance -= variable_costs_summarized
        if producer.balance < 0:
            print(f'{producer} is bankrupt! Variable')
            producer_list.pop(producers.index(producer))
    for broker in broker_list:
        broker.balance -= broker.count_purchase_costs()
        if broker.balance < 0:
            print(f'{broker} is bankrupt! Variable')
            broker_list.pop(broker_list.index(broker))

    # Расчёт прибыли
    for producer in producer_list:
        producer.balance += producer.count_proceeds()
    for broker in broker_list:
        broker.add_shipments()
        broker.balance += broker.count_proceeds(market_price)

    # Расчёт расходов на хранение и отправка на хранение заготовок
    for producer in producer_list:
        producer.balance -= producer.count_storage_costs()
        if producer.balance < 0:
            print(f'{producer} is bankrupt! Storage')
            producer_list.pop(producer_list.index(producer))
            continue
        producer.store_billets()

    crown.update_balance(market_volume)
    for producer in producer_list:
        print(producer.balance, producer.billets_stored)
    for broker in broker_list:
        print(broker.balance)
    results = {
        'producers': producer_list,
        'brokers': broker_list,
        'crown_balance': crown.balance
    }
    return results


print(count_turn(producers, brokers, market_transactions))
