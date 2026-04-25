import datetime
from decimal import Decimal


class Trade:
    trade_id: int
    symbol: str
    quantity: int
    price: Decimal
    time: datetime.datetime


class Position:
    symbol: str
    quantity: int
    average_cost_basis: Decimal
    realized_p_and_L: Decimal


class Portfolio:
    name: str
    holdings: dict[str, Position]

    def __init__(self, _name_):
        name = _name_
        self.holdings = {}

    def process_trade(self, trade: Trade):
        if trade.symbol not in self.holdings:
            new_position = Position()
            new_position.symbol = trade.symbol
            new_position.average_cost_basis = 0
            new_position.realized_p_and_L = 0
            new_position.quantity = 0
            self.holdings[trade.symbol] = new_position

        self.holdings[trade.symbol].quantity += trade.quantity
        self.holdings[trade.symbol].average_cost_basis += trade.price

    def list_position(self):
        for key, value in self.holdings.items():
            print(
                f"[{key}], quantity: {value.quantity}, cost: {value.average_cost_basis}, P/L: {value.realized_p_and_L}\n")
        print('\n')


p = Portfolio("Nicks")
p.list_position()

t = Trade()
t.trade_id = 4
t.price = 4.45
t.quantity = 5
t.symbol = "IGT"
t.time = datetime.datetime.now()

p.process_trade(t)

t2 = Trade()
t2.trade_id = 6
t2.price = 6.45
t2.quantity = 45
t2.symbol = "IGT"
t2.time = datetime.datetime.now()
p.process_trade(t2)
p.list_position()
