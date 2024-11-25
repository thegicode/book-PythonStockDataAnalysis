"""
# 3.6 회귀 분석과 상관관계

## 3.6.2 지수화(Indexation) 비교 
- 현재 종가를 특정 시점의 종가로 나누어 변동률을 구한다.
- 연습 : 다우존스 지수와 KOSPI의 지수화 비교

"""

import yfinance as yf
import matplotlib.pyplot as plt

dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

#  금일 다우존스 지수를 2000년 1월 4일 다우존스 지수로 나눈 뒤 100을 곱한다.
d = (dow.Close / dow.Close['2000-01-04']) * 100

#  금일 코스피 지수를 2000년 1월 4일 코스피 지수로 나눈 뒤 100을 곱한다.
k = (kospi.Close / kospi.Close['2000-01-04']) * 100

plt.figure(figsize=(9, 5))
plt.plot(d.index, d, 'r--', label="Dow Jones Industrial")
plt.plot(k.index, k, 'b', label="KOSPI")
plt.grid(True)
plt.legend(loc='best')
plt.show()