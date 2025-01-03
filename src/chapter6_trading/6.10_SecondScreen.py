import os
import sys
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 

# 데이터 불러오기
mk = MarketDB()
df = mk.get_daily_price('TIGER 200', '2023-01-04')

# EMA 및 MACD 계산
ema60 = df.close.ewm(span=60).mean()
ema130 = df.close.ewm(span=130).mean() 
macd = ema60 - ema130
signal = macd.ewm(span=45).mean()
macdhist = macd - signal

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna()

# Stochastic 계산
# 1. 14일 동안 최대값
ndays_high = df.high.rolling(window=14, min_periods=1).max()
# 2. 14일 동안 최소값
ndays_low = df.low.rolling(window=14, min_periods=1).min()
# 3. 빠른 선 %K
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
# 4. 느린 선 %D : 3일 동안 %K의 평균
slow_d = fast_k.rolling(window=3).mean()

df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()

# 캔들차트 및 지표 추가
apds = [
    mpf.make_addplot(df['ema130'], color='cyan', label='EMA130'),  # EMA130 추가
    mpf.make_addplot(df['fast_k'], panel=1, color='blue', label='%K'),  # %K 추가
    mpf.make_addplot(df['slow_d'], panel=1, color='black', label='%D')  # %D 추가
]

# 캔들차트 플롯
mpf.plot(
    df,
    type='candle',
    addplot=apds,
    title='Triple Screen Trading - Second Screen',
    style='yahoo',
    volume=False,
    panel_ratios=(3, 1),  # 패널 크기 비율
    ylabel='Price',
    ylabel_lower='Stochastic',
    figratio=(9, 7),
    figscale=1.2
)
