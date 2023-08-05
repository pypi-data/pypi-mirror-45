from datetime import datetime
from decimal import Decimal
from typing import List

import pandas
import talib
import dateutil.parser as dp

from .chainable import Chainable
from .framework import Strategy
from .market_data import MarketData
from .ticker import Pair
from .common import Interval, Instructions
from .candle import Close
from .technical_analysis import MA
from .trade import Side
from .currency import Currency
from .indicator import SMA

# from .okex_trade import OkexTrade


class BacktestResult():
    pass


class BacktestConfig(Chainable):
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

        # self.trade = OkexTrade("ETHUSD")


class Backtest():
    def __init__(self, config: BacktestConfig):
        self.config = config

    def set_config(self, config: BacktestConfig) -> None:
        self.config = config

    def get_config(self) -> BacktestConfig:
        return self.config

    def run(self, strategy: Strategy):
        net_asset_list = []
        net_asset = {
                        Currency('USD').name: 10,
                        Currency('USD').name + '_equity': 0.,
                        'equity': 0.
                    }
        for pair in self.config.pairs:
            net_asset[pair.quote_currency.name] = 10
            net_asset[pair.quote_currency.name + '_equity'] = 0.
        # net_asset_list.append([self.config.start, net_asset.copy()])

        ohlcs = {}
        for pair in self.config.pairs:
            ohlcs[pair] = MarketData().ohlc_history(
                pair, self.config.interval,
                self.config.start, self.config.end
            )
        #for pair, ohlc in ohlcs.items():
        #    print(ohlc, type(ohlc))
        #    r = talib.SMA(ohlc['close'], 100)
        #    print(r, type(r))
        df = pandas.concat({
            pair: pandas.concat([
                ohlc[['open', 'close']],
                SMA(ohlc['close'], 100).rename('ma_close_100')
                #talib.SMA(ohlc['close'], 100).rename('ma_close_100')
            ], axis=1)
            for pair, ohlc in ohlcs.items()
        }, axis=1)
        #print(df.iloc[:100])

        for index, row in df.iterrows():
            close_dict = {}
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
                close_dict[str(item[0][0])] = close

            try:
                strategy.on_tick()
            except Exception as e:
                print(e)
            for instruction in Instructions().get_all():
                pair = instruction.get_symbol().split('@')[0]
                side = instruction.get_side()
                status = instruction.get_status()
                print(index, close.get_key(), ma)
                print(instruction.symbol, instruction.side)
                print(pair)
                quote_name, base_name = pair.split('/')
                close = close_dict[instruction.get_symbol()].get_value()
                if instruction.side == Side.BUY:
                    net_asset[quote_name] += 1
                    net_asset[base_name] -= 1 * close
                elif instruction.side == Side.SELL:
                    net_asset[quote_name] -= 1
                    net_asset[base_name] += 1 * close
            net_asset['equity'] = 0
            net_asset['USD_equity'] = net_asset['USD']
            for pair in self.config.pairs:
                quote = pair.quote_currency.name
                close = close_dict[str(pair)].get_value()
                net_asset[quote + '_equity'] = close * net_asset[quote]

            for key in net_asset:
                if '_equity' in key:
                    net_asset['equity'] += net_asset[key]
            net_asset_list.append([index, net_asset.copy()])
            Instructions().clear()
        x, y = [], []
        for time, dic in net_asset_list:
            #x.append(dp.parse(time))
            x.append(time)
            # x.append(dp.parse(time).strftime('%d %H:%M'))
            y.append(dic['equity'])
            print(time, dic['equity'])
        '''
        import matplotlib.pyplot as plt
        plt.xlabel('datetime')
        plt.ylabel('net asset')
        plt.title('backtest')
        plt.gcf().autofmt_xdate()
        plt.xticks(rotation=90)
        plt.plot_date(x, y, color='b', linestyle='-', marker=',', label='okex')
        plt.legend(loc='best')
        plt.show()
        '''
