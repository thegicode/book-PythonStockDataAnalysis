# 야후 파이낸스로 주식 시세 구하기

import yfinance as yf
import matplotlib.pyplot as plt

# 삼성전자 데이터
sec = yf.download('005930.KS', start='2018-05-01', end='2018-12-31')
# 마이크로소프트 데이터
msft = yf.download('MSFT', start='2018-05-01', end='2018-12-31')
tmp_msft = msft.drop(columns='Volume')

print(sec.tail())
print(tmp_msft.tail())

print("")

print(sec.index)
print(tmp_msft.index)

print("")

print(sec.columns)
print(tmp_msft.columns)

print("")


# plot(x, y, 마커 형태, [, lable='Label'])
plt.plot(sec.index, sec.Close, 'b', label="Samsung Electronics")
plt.plot(msft.index, msft.Close, 'r--', label="Microsoft")
plt.legend(loc='best')
plt.show()


