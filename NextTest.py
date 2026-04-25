class trade:
    symbol: str
    qty: int
    client_order_id: str
    side: str


positions: dict[str, int] = {}


def apply_trade(position, trade) -> position:
    pass
