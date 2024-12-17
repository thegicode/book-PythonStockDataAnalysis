import backtrader as bt
from datetime import datetime
import yfinance as yf

# 1. MyStrategy 클래스 정의
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    # 1. 주문 order 상태에 변화가 있을 때마다 자동으로 실행
    # 주문 상태는 완료 Completed, 취소 Canceled, Margin, 거절 Rejected
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 2. 주문 상태가 완료 Completed이면 매수인지 매도인지 확인하여 상세 주문 정보를 출력
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY  : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('ORDER ERROR')

        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

    # 3. 텍스트 메시지를 인수로 받아서 셸 화면에 주문 일자와 함께 출력
    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

# 2. yfinance를 사용해 데이터 다운로드
ticker = '005930.KS'
start_date = '2023-01-01'
end_date = '2024-12-17'

data = yf.download(ticker, start=start_date, end=end_date)
data_feed = bt.feeds.PandasData(dataname=data)

# 3. 백테스트 실행
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data_feed)

cerebro.broker.setcash(10000000)
# 4. 수수료 commission는 매수, 매도가 발새앟ㄹ 때마다 차감된다. 
cerebro.broker.setcommission(commission=0.0014)
# 5. size는 매매 주문을 적용할 주식수를 나타내며, 특별히 지정하지 않으면 1
# PercentSizer를 사용하면 포트폴리오 자산에 대한 퍼센트로 지정할 수 있는데, 
# 100으로 지정하면 수수료를 낼 수 없어서 ORDER MARGIN이 발생하므로, 수수료를 차감한 퍼센트로 지정해야 한다. 
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')

# 6. 주가를 표시할 때 캔들스틱 차트로 표시한다.
cerebro.plot(style='candlestick')
