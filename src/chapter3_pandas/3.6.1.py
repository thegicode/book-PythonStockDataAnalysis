"""
# 3.6 회귀 분석과 상관관계

## 3.6.1 KOSPI와 다우존스 지수 비교
- 결론: 지수의 기준값이 달라, 두 지수 중 어느 쪽이 더 좋은 성과를 냈는지 한눈에 파악하기 어렵다.

"""

import yfinance as yf
import matplotlib.pyplot as plt

dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

plt.figure(figsize=(9, 5))
plt.plot(dow.index, dow.Close, 'r--', label="Dow Jones Industrial")
plt.plot(kospi.index, kospi.Close, 'b', label="KOSPI")
plt.grid(True)
plt.legend(loc='best')
plt.show()