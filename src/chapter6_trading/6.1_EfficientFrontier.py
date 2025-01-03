"""시총 상위 4 종목으로 효율적 투자선 구하기"""

import os
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from src.MarketDB import MarketDB 

mk = MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2021-01-01', '2024-11-29')['close']
# print(df)

# 1. 일간 변동률
daily_ret = df.pct_change() # 백분율 변화율
# print(daily_ret)

# 2. 연간 수익률, 미국 1년 평균 개장일 252일
annual_ret = daily_ret.mean() * 252 # 연간수익률 : 일별 평균 수익률 * 연간 거래일 수(252일) 
# print("annual_ret\n", annual_ret)

# 3. 일간 리스크, 일간 변동률의 공분산 (Covariance)
daily_cov = daily_ret.cov() # 모든 자산 쌍의 공분산을 계산하여 공분산 행렬(Covariance Matrix)을 반환
# print(daily_cov)

# 4. 연간 공분산
annual_cov = daily_cov * 252

port_ret = []
prot_risk = []
port_weights = []

for _ in range(2000):
    # 2. 4개의 랜덤 숫자로 구성된 배열을 생성
    weights = np.random.random(len(stocks))
    # 3. 2에서 구한 4개의 랜덤 숫자를 랜험 숫자의 총합으로 나눠 종목 비중의 합이 1이 되도록 조정
    weights /= np.sum(weights)

    # 4. 랜덤하게 생성한 종목별 비중 배열과 종목별 연간 수익룰을 곱해 해당 포트폴리오 전체 수익률을 구한다.
    returns = np.dot(weights, annual_ret)
    # 5. 
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    prot_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': prot_risk}
# 7. 
for i, s in enumerate(stocks):
    # 8. 
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
# 9.
df = df[['Returns', 'Risk'] + [s for s in stocks]]

df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier') 
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show() 