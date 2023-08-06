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
from .common import Interval, Instructions, MarketType
from .candle import Close
from .technical_analysis import MA, STD
from .trade import Side
from .currency import Currency
from .indicator import Indicator


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


class Backtest():
    def __init__(self, config: BacktestConfig):
        self.config = config

    def set_config(self, config: BacktestConfig) -> None:
        self.config = config

    def get_config(self) -> BacktestConfig:
        return self.config

    def run(self, strategy: Strategy):
        bt_status_list = []
        bt_status = {
                        Currency('ETH').name: Decimal("10000"),
                        Currency('ETH').name + '_equity': Decimal("0."),
                        'equity': Decimal("0."),
                        'buy_volume': Decimal("0."),
                        'sell_volume': Decimal("0."),
                        'buy_trade_cnt': 0,
                        'sell_trade_cnt': 0,
                    }
        for pair in self.config.pairs:
            bt_status[pair.quote_currency.name] = Decimal("0")
            bt_status[pair.quote_currency.name + '_equity'] = Decimal("0.")
            bt_status[pair.quote_currency.name + '_trade'] = 0
            bt_status[pair.quote_currency.name + '_close'] = 0

        ohlcs = {}
        for pair in self.config.pairs:
            ohlcs[pair] = MarketData().ohlc_history(
                pair, self.config.interval,
                self.config.start, self.config.end,
                MarketType.Spot
            ).sort_index(ascending=True)
        df = pandas.concat({
            pair: pandas.concat([
                ohlc[['open', 'close']],
                Indicator.SMA(ohlc['close'], 20).rename('ma_close_20'),
                Indicator.STD(ohlc['close'], 20).rename('std_close_20')
                #talib.SMA(ohlc['close'], 100).rename('ma_close_100')
            ], axis=1)
            for pair, ohlc in ohlcs.items()
        }, axis=1)

        fee_open = 0

        for index, row in df.iterrows():
            close_dict = {}
            for item in row.iteritems():
                close = Close(
                        pair=item[0][0],
                        interval=self.config.interval
                    )
                if item[0][1] == 'close':
                    close.set_value(item[1])
                elif item[0][1] == 'ma_close_20':
                    ma = MA(
                        close,
                        20
                    )
                    ma.set_value(item[1])
                elif item[0][1] == 'std_close_20':
                    std = STD(
                        close,
                        20
                    )
                    std.set_value(item[1])
                close_dict[str(item[0][0])] = close

            try:
                strategy.on_tick()
            except Exception as e:
                print('strategy error {}'.format(e))
            for instruction in Instructions().get_all():
                pair = instruction.get_symbol().split('@')[0]
                side = instruction.get_side()
                status = instruction.get_status()
                # print(index, close.get_key(), ma)
                quote_name, base_name = pair.split('/')
                close = close_dict[instruction.get_symbol()].get_value()
                volume = instruction.volume
                # print(index, close, type(volume))
                # print(instruction.symbol, instruction.side, instruction.volume)

                if side == "buy":
                    if fee_open == 1:
                        bt_status[quote_name] += volume
                        bt_status[base_name] -= (volume + self.config.taker_fee) * close
                    else:
                        bt_status[quote_name] += volume
                        bt_status[base_name] -= volume * close
                    bt_status['buy_volume'] += volume
                    bt_status['buy_trade_cnt'] += 1
                elif side == "sell":
                    if fee_open == 1:
                        bt_status[quote_name] -= (volume + self.config.taker_fee)
                        bt_status[base_name] += volume * close
                    else:
                        bt_status[quote_name] -= volume
                        bt_status[base_name] += volume * close 
                    bt_status['sell_volume'] += volume
                    bt_status['sell_trade_cnt'] += 1
                    
            bt_status['equity'] = Decimal("0")
            bt_status['ETH_equity'] = bt_status['ETH']
            for pair in self.config.pairs:
                quote = pair.quote_currency.name
                close = close_dict[str(pair)].get_value()
                bt_status[quote + '_equity'] = close * bt_status[quote]

            for key in bt_status:
                if '_equity' in key:
                    bt_status['equity'] += bt_status[key]
            bt_status_list.append([index, bt_status.copy()])
            Instructions().clear()
        x, y = [], []
        for time, dic in bt_status_list:
            #x.append(dp.parse(time))
            x.append(time)
            # x.append(dp.parse(time).strftime('%d %H:%M'))
            y.append(dic['equity'])
        print(len(bt_status_list), len(x), len(y))
        if len(bt_status_list) == 0:
            print('no data')
            return 
        bt_status_final = bt_status_list[-1][1]
        print('final result')
        print('equity:{}\nbuy_volume:{}\nsell_volume:{}\n\
                buy_trade_cnt:{}\nsell_trade_cnt:{}'.format(
                    bt_status_final['equity'],
                    bt_status_final['buy_volume'], 
                    bt_status_final['sell_volume'], 
                    bt_status_final['buy_trade_cnt'], 
                    bt_status_final['sell_trade_cnt'] 
                    )
                )
        print('drawdown', Indicator.Drawdown(y))
        import matplotlib.pyplot as plt
        plt.xlabel('datetime')
        plt.ylabel('net asset:ETH')
        plt.title('backtest')
        plt.gcf().autofmt_xdate()
        plt.xticks(rotation=90)
        plt.plot_date(x, y, color='b', linestyle='-', marker=',', label='okex')
        plt.legend(loc='best')
        plt.show()
