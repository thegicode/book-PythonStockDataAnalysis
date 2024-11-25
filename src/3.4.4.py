# 일간 변동률 누적합(Cumulative Sum) 구하기

import yfinance as yf
import matplotlib.pyplot as plt

# SK하이닉스 데이터
sec = yf.download('000660.KS', start='2024-01-01')
# 마이크로소프트 데이터
msft = yf.download('MSFT', start='2024-01-01')

sec_dpc = (sec['Close']/sec['Close'].shift(1) -1) * 100
sec_dpc.iloc[0] = 0

msft_dpc = (msft['Close']/msft['Close'].shift(1) -1) * 100
msft_dpc.iloc[0] = 0

sec_dpc_cs = sec_dpc.cumsum()
print(sec_dpc_cs) 
#  + 32%

msft_dpc_cs = msft_dpc.cumsum()
print(msft_dpc_cs)
#  + 12%

plt.plot(sec.index, sec_dpc_cs, 'b', label="SK Hynix")
plt.plot(msft.index, msft_dpc_cs, 'r--', label="Microsoft")
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()
