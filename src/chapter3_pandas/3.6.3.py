"""
# 3.6 회귀 분석과 상관관계

## 3.6.3 산점도 Scatter plot 분석
- 산점도란 독립변수 x와 종속변수 y의 상관관계를 확인할 때 쓰는 그래프
- 미국 시장과 국내 시장의 상관관계를 알아보고자 x를 다우존스 지수로, y를 KOSPI 지수로 정했다.
- 결론 
    - 점의 분포가 y = x인 직선 형태에 가까울수록 직접적인 관계가 있다고 볼 수 있다.
    - 산점도 그래프만 봐서는 정확한 분석이 어려우므로 선형 회귀 분석으로 더 정확히 분석해보자.
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

print(len(dow), len(kospi)) 
# 6262 6136

# 산점도를 그리려면 x,y의 사이즈가 동일해야 한다.
df = pd.DataFrame({'Dow': dow['Close'], "KOSPI": kospi['Close']})
print(df)

## 산점도를 그리면 NaN을 제거해야 한다.
df = df.bfill()  # 역방향으로 결측값 채우기
df = df.ffill()  # 순방향으로 결측값 채우기

print(df)

plt.figure(figsize=(7, 7))
plt.scatter(df['Dow'], df['KOSPI'], marker=".")
plt.xlabel("Dow Jones Industrial Average")
plt.ylabel("KOSPI")
plt.show()
