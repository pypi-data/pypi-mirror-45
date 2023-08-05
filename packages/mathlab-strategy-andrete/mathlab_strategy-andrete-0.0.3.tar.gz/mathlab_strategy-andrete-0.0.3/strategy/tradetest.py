from datetime import datetime
from decimal import Decimal
from typing import List

import pandas
import talib

from .chainable import Chainable
from .framework import Strategy
from .market_data import MarketData
from .ticker import Pair
from .common import Interval, Instructions
from .candle import Close
from .technical_analysis import MA
from .trade import *

from .okex_trade import OkexTrade

class TradetestResult():
    pass


class TradetestConfig(Chainable):
    def __init__(
        self, pairs: List[Pair], interval: Interval,
        start: datetime, end: datetime,
        maker_fee: Decimal, taker_fee: Decimal
    ):
        self.pairs = pairs
        self.interval = interval
        self.start = start
        self.end = end
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee


class Tradetest():
    def __init__(self, config: TradetestConfig):
        self.config = config
        self.trade = OkexTrade("ETHUSD")

    def set_config(self, config: TradetestConfig) -> None:
        self.config = config

    def get_config(self) -> TradetestConfig:
        return self.config

    def run(self, strategy: Strategy):
        ohlcs = {}
        for pair in self.config.pairs:
            ohlcs[pair] = MarketData().ohlc_history(
                pair, self.config.interval,
                self.config.start, self.config.end
            )
        df = pandas.concat({
            pair: pandas.concat([
                ohlc[['open', 'close']],
                talib.SMA(ohlc['close'], 100).rename('ma_close_100')
            ], axis=1)
            for pair, ohlc in ohlcs.items()
        }, axis=1)

        trade_counts = 0
        for index, row in df.iterrows():
            for item in row.iteritems():
                close = Close(
                        pair=item[0][0],
                        interval=self.config.interval
                )
                if item[0][1] == 'close':
                    close.set_value(item[1])
                elif item[0][1] == 'ma_close_100':
                    ma = MA(
                        close,
                        100
                    )
                    ma.set_value(item[1])
            try:
                strategy.on_tick()
            except Exception as e:
                print(e)
            for instruction in Instructions().get_all():
                pair = instruction.get_symbol().split('@')[0].replace('/', '')
                side = instruction.get_side()
                status = instruction.get_status()
                print(index, type(instruction), pair, side, status)

                way = None
                if isinstance(instruction, placeTakerOrder):
                    way = "taker"
                elif isinstance(instruction, placeMakerOrder):
                    way = "taker"

                if way is None:
                    continue

                trade_counts += 1
                if side == "buy":
                    if status == "long":
                        print(index, "open long...")
                        self.trade.enter_long(way, 1)
                    elif status == "short":
                        print(index, "open short...")
                        self.trade.enter_short(way, 1)
                elif side == "sell":
                    if status == "long":
                        print(index, "exit long...")
                        self.trade.exit_long(way, 0)
                    elif status == "short":
                        print(index, "exit short...")
                        self.trade.exit_short(way, 0)

            Instructions().clear()
            if trade_counts > 3:
                break
