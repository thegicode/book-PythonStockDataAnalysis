"""시총 상위 4 종목으로 효율적 투자선 구하기"""

import os
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 

mk = MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2021-01-01', '2024-11-29')['close']

daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252

port_ret = []
prot_risk = []
port_weights = []
sharpe_ratio = [] 

for _ in range(2000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    prot_risk.append(risk)
    port_weights.append(weights)
    # ① 포트폴리오의 수익률을 리스크로 나눈 값을 샤프 지수 리스트에 추가
    sharpe_ratio.append(returns/risk) 

portfolio = {'Returns': port_ret, 'Risk': prot_risk, 'Sharpe': sharpe_ratio}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
# ② 샤프 지수 칼럼을 데이터프레임에 추가
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]] 
print(df)

# ③
max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]  
# ④
min_risk = df.loc[df['Risk'] == df['Risk'].min()]  

print(max_sharpe)
print(min_risk)

# ⑤ 포트폴리오의 샤프 지수에 따라 컬러맵을 'viridis'로 표시하고 테두리는 검정(k)로 표시
df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
    edgecolors='k', figsize=(11,7), grid=True)  
# ⑥ 샤프지수가 가장 큰 포트폴리오를 300 크기의 *로 표시
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', 
    marker='*', s=300)  
# ⑦ 리스크가 가장 작은 포트폴리오를 200 크기의 붉은 X로 표시
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', 
    marker='X', s=200)  
plt.title('Portfolio Optimization') 
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show()