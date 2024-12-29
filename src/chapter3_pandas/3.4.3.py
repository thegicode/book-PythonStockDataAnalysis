# 주가 일간 변동률 히스토그램 

import yfinance as yf
import matplotlib.pyplot as plt

# 삼성전자 데이터
sec = yf.download('005930.KS', start='2018-05-01', end='2018-12-31')
# 마이크로소프트 데이터
msft = yf.download('MSFT', start='2018-05-01', end='2018-12-31')

sec_dpc = (sec['Close']/sec['Close'].shift(1) -1) * 100
sec_dpc.iloc[0] = 0

msft_dpc = (msft['Close']/msft['Close'].shift(1) -1) * 100
msft_dpc.iloc[0] = 0

plt.hist(sec_dpc, bins=18)
plt.grid(True)
plt.show()

print(sec_dpc.describe())

plt.hist(msft_dpc, bins=18)
plt.grid(True)
plt.show()

print(msft_dpc.describe())


