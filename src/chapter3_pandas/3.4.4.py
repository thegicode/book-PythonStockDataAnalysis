# 일간 변동률 누적합(Cumulative Sum) 구하기

import yfinance as yf
import matplotlib.pyplot as plt

# 삼성 데이터
# sec = yf.download('000660.KS', start='2018-05-04')
sec = yf.download('005930.KS', start='2018-05-04')
# 마이크로소프트 데이터
msft = yf.download('MSFT', start='2018-05-04')

# 일간 변동률
sec_dpc = (sec['Close']/sec['Close'].shift(1) -1) * 100
sec_dpc.iloc[0] = 0

msft_dpc = (msft['Close']/msft['Close'].shift(1) -1) * 100
msft_dpc.iloc[0] = 0

# 일간 변동률 누적합
sec_dpc_cs = sec_dpc.cumsum()
print(sec_dpc_cs) 
#  + 25%

msft_dpc_cs = msft_dpc.cumsum()
print(msft_dpc_cs)
#  + 178%

plt.plot(sec.index, sec_dpc_cs, 'b', label="Samsung")
plt.plot(msft.index, msft_dpc_cs, 'r--', label="Microsoft")
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()
