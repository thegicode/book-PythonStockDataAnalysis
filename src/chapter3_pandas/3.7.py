"""
# 3.7 상관계수에 따른 리스크 완화

## 3.7.4 다우존스 지수와 KOSPI 회귀 분석
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats

dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

df = pd.DataFrame({'X': dow['Close'], "Y": kospi['Close']})
df = df.bfill() 
df = df.ffill() 

# 다우존스 지수 X와 KOSPU 지수 Y로 선형회귀 모델 갹체 regr을 생성한다.
regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'

plt.figure(figsize=(7, 7))
plt.plot(df.X, df.Y, '.') # 산점도를 작은 원으로 나타낸다.
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r') # 산점도를 붉은 색으로 그린다.
plt.legend(['DOW × KOSPI', regr_line])
plt.title(f"DOW × KOSPI (R = {regr.rvalue:.2f})")
plt.xlabel("Dow Jones Industrial Average")
plt.ylabel("KOSPI")
plt.show()
