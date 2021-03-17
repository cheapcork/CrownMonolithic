from .producer import ProducerNormal
from .broker import BrokerNormal
from .crown import CrownNormal
from .transaction import TransactionNormal as Transaction
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

t1 = Transaction(producer_1.id, broker_1.id, terms_1).form_transaction()
t2 = Transaction(producer_2, broker_1, terms_2).form_transaction()
t3 = Transaction(producer_3, broker_1, terms_3).form_transaction()
t4 = Transaction(producer_4, broker_1, terms_4).form_transaction()
t5 = Transaction(producer_5, broker_2, terms_5).form_transaction()
t6 = Transaction(producer_6, broker_2, terms_6).form_transaction()
t7 = Transaction(producer_7, broker_2, terms_7).form_transaction()
t8 = Transaction(producer_8, broker_3, terms_8).form_transaction()
t9 = Transaction(producer_9, broker_3, terms_9).form_transaction()
t10 = Transaction(producer_10, broker_3, terms_10).form_transaction()

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
market_transactions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

