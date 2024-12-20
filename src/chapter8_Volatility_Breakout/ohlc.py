from datetime import datetime, timedelta
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


def get_ohlc(code, count):
    # 데이터 불러오기
    mk = MarketDB()
    df = mk.get_daily_price(code, count=count)

    ohlc = df[['open', 'high', 'low', 'close']]

    ohlc = ohlc.sort_index(ascending=False)

    return ohlc

if __name__ == "__main__":

    df = get_ohlc("305080", 10)
    print(df)

