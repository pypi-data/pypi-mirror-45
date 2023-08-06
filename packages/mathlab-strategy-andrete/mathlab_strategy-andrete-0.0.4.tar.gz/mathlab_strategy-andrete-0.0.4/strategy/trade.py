from decimal import Decimal
from enum import Enum

from .ticker import Symbol
from .volume import Volume
from .common import Instructions, Instruction, Status


class Side(Enum):
    BUY = 'buy'
    SELL = 'sell'


class placeOrder(Instruction):
    def __init__(self, symbol, side, volume, status, price=None):
        Instructions().add(self)
        self.symbol = symbol.get_key()
        self.side = side.value
        self.volume = volume
        self.status = status.get()
        self.price = price

    def get_symbol(self):
        return self.symbol

    def get_side(self):
        return self.side

    def get_volume(self):
        return self.volume

    def get_status(self):
        return self.status
        

class placeLimitOrder(placeOrder):
    def __init__(
        self, symbol: Symbol, side: Side, volume: Volume, status: Status, price: Decimal
    ):
        super().__init__(symbol, side, volume, status, price)


class placeMarketOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        super().__init__()
        self.symbol = symbol
        self.side = side
        self.volume = volume


class placeMakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume, status: Status):
        super().__init__(symbol, side, volume, status)


class placeTakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume, status: Status):
        super().__init__(symbol, side, volume, status)
