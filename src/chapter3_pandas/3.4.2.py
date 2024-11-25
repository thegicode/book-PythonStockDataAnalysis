# 일간 변동률(daily percent change)로 주가 비교하기 

import yfinance as yf
import matplotlib.pyplot as plt

# 삼성전자 데이터
sec = yf.download('005930.KS', start='2018-05-01', end='2018-12-31')
# 마이크로소프트 데이터
msft = yf.download('MSFT', start='2018-05-01', end='2018-12-31')
tmp_msft = msft.drop(columns='Volume')

print(type(sec['Close'])) # Series

print("")

sec_dpc = (sec['Close']/sec['Close'].shift(1) -1) * 100
sec_dpc.iloc[0] = 0
print(sec_dpc)

print("")

msft_dpc = (msft['Close']/msft['Close'].shift(1) -1) * 100
msft_dpc.iloc[0] = 0
print(msft_dpc)