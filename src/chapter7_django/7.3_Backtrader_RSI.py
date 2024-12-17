import yfinance as yf
from datetime import datetime
import backtrader as bt

# ① MyStrategy 클래스 정의
class MyStrategy(bt.Strategy): 
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)  

    def next(self):  
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

# ② Yahoo Finance 데이터를 yfinance로 가져오기
ticker = '005930.KS'
start_date = '2023-01-01'
end_date = '2024-12-01'

# yfinance를 사용해 데이터 다운로드
data = yf.download(ticker, start=start_date, end=end_date)

# Pandas DataFrame을 Backtrader로 변환
data_feed = bt.feeds.PandasData(dataname=data)

# ③ 백테스트 실행
cerebro = bt.Cerebro()  
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data_feed)

# 초기 투자금 설정
cerebro.broker.setcash(10000000)
cerebro.addsizer(bt.sizers.SizerFix, stake=30)  

# 백테스트 실행 및 결과 출력
print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')

# 결과 차트 출력
cerebro.plot()
