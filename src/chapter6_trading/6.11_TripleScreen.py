import os
import sys
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd
import numpy as np

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 

symbol = 'ACE 미국나스닥100'

# 데이터 불러오기
mk = MarketDB()
df = mk.get_daily_price(symbol, '2023-01-04')

# EMA 및 MACD 계산
ema60 = df.close.ewm(span=60).mean()
ema130 = df.close.ewm(span=130).mean() 
macd = ema60 - ema130
signal = macd.ewm(span=45).mean()
macdhist = macd - signal
df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna()

df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

# Stochastic 계산
ndays_high = df.high.rolling(window=14, min_periods=1).max()
ndays_low = df.low.rolling(window=14, min_periods=1).min()
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
slow_d = fast_k.rolling(window=3).mean()
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()

# 신호 위치 계산
buy_signals = []
sell_signals = []
for i in range(1, len(df.close)):
    # 1. 130일 이동 지수평균이 상승하고 %D가 20 아래로 떨어지면 빨간색 삼각형으로 매수 신호를 표시
    if df.ema130.values[i-1] < df.ema130.values[i] and \
        df.slow_d.values[i-1] >= 20 and df.slow_d.values[i] < 20:
        buy_signals.append((df.index[i], df.close.values[i]))
    # 2. 130일 이동 지수평균이 하락하고 %D가 80 위로 상승하면 파란색 삼각형으로 매도 신호를 표시
    elif df.ema130.values[i-1] > df.ema130.values[i] and \
        df.slow_d.values[i-1] <= 80 and df.slow_d.values[i] > 80:
        sell_signals.append((df.index[i], df.close.values[i]))


# 매수/매도 신호를 시계열 데이터로 변환 (NaN 사용)
df['buy_signal'] = np.nan
df['sell_signal'] = np.nan

for date, price in buy_signals:
    df.loc[date, 'buy_signal'] = price  # 매수 신호 추가

for date, price in sell_signals:
    df.loc[date, 'sell_signal'] = price  # 매도 신호 추가

# mplfinance 추가 지표
# mplfinance 추가 지표
apds = [
    mpf.make_addplot(df['ema130'], color='cyan', label='EMA130'),  # EMA130 추가
    mpf.make_addplot(df['fast_k'], panel=1, color='blue', label='%K'),  # %K 추가
    mpf.make_addplot(df['slow_d'], panel=1, color='black', label='%D'),  # %D 추가
    mpf.make_addplot(df['macd'], panel=2, color='blue', label='MACD'),  # MACD 추가
    mpf.make_addplot(df['signal'], panel=2, color='green', linestyle='dashed', label='MACD Signal'),  # MACD Signal 추가
    mpf.make_addplot(df['macdhist'], panel=2, type='bar', color='magenta', alpha=0.5, label='MACD-Hist')  # MACD 히스토그램 추가
]

# 매수 신호가 있으면 추가
if not df['buy_signal'].isna().all():
    apds.append(mpf.make_addplot(df['buy_signal'], scatter=True, markersize=50, marker='^', color='red', label='Buy Signal'))

# 매도 신호가 있으면 추가
if not df['sell_signal'].isna().all():
    apds.append(mpf.make_addplot(df['sell_signal'], scatter=True, markersize=50, marker='v', color='blue', label='Sell Signal'))

# mplfinance 차트 플롯
mpf.plot(
    df,
    type='candle',
    addplot=apds,
    title=f'Triple Screen Trading - Second Screen ({symbol})',
    style='yahoo',
    volume=False,
    panel_ratios=(3, 1, 1),  # 패널 크기 비율 (가격, Stochastic, MACD)
    ylabel='Price',
    ylabel_lower='Stochastic',
    figratio=(9, 7),
    figscale=1.2
)
