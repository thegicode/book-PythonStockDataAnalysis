# 최대 손실 낙폭 
# MDD = (최저점 - 최고점) / 최저점

# KOSPI의 MDD 구하기

import yfinance as yf
import matplotlib.pyplot as plt

# KOSPI 지수 심볼 '^KS11'
kospi = yf.download('^KS11', start='2004-01-04')

# 1년 동안의 개장일
window = 252

# 1년 기간 단위로 최고치 peak
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()

# drawdown: 최고치 peak 대비 현재 Kospi 종가가 얼마나 하락했는지
drawdown = kospi['Adj Close']/peak - 1.0

# drawdown에서 1년 기간 단위로 최저치 max_dd
# 마이너스값이기 때문에 최저치가 바로 최대 손실 낙폭이 된다.
max_dd = drawdown.rolling(window, min_periods=1).min()

print(max_dd.min())
# -0.5453665130144085

print(max_dd[max_dd==-0.5453665130144085])
# 2008년 10월 24일부터 2009년 10월 22일까지 1년(252일) 동안 주어진 max_dd과 일치

plt.plot(drawdown.index, drawdown, 'b', label="KOSPI DD")
plt.plot(max_dd.index, max_dd, 'r--', label="KOSPI MDD")
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()
