import os
import sys
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 

mk = MarketDB()
df = mk.get_daily_price('TIGER 200', '2023-01-04')

# EMA와 MACD 계산
ema60 = df.close.ewm(span=60).mean()   # 종가의 60일 지수 이동평균
ema130 = df.close.ewm(span=130).mean() # 종가의 130일 지수 이동평균
macd = ema60 - ema130                  # MACD선
signal = macd.ewm(span=45).mean()      # 신호선(MACD의 45일 지수 이동평균)
macdhist = macd - signal               # MACD 히스토그램

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()

# 캔들차트 그리기
apds = [
    mpf.make_addplot(df['ema130'], color='cyan', label='EMA130'),
    mpf.make_addplot(df['macdhist'], type='bar', color='magenta', panel=1, ylabel='MACD-Hist'),
    mpf.make_addplot(df['macd'], color='blue', panel=1, ylabel='MACD'),
    mpf.make_addplot(df['signal'], color='green', linestyle='--', panel=1)
]

mpf.plot(
    df,
    type='candle',
    addplot=apds,
    title='Triple Screen Trading - First Screen',
    style='yahoo',
    volume=False,
    panel_ratios=(3, 1),
    ylabel='Price',
    tight_layout=True,
    figratio=(9, 7),
    figscale=1.2
)
