import os
import sys
from matplotlib import pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 


mk = MarketDB()
df = mk.get_daily_price('ACE 미국S&P500', '2024-01-04')

df['MA20'] = df['close'].rolling(window=20).mean()  
df['stddev'] = df['close'].rolling(window=20).std() 
df['upper'] = df['MA20'] + (df['stddev'] * 2)  
df['lower'] = df['MA20'] - (df['stddev'] * 2)  
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])  

# ① SK하이닉스의 종가, 고가, 저가, 거래량을 이용해 일중 강도 II를 구한다.
df['II'] = (2*df['close']-df['high']-df['low'])/(df['high']-df['low'])*df['volume'] 
# ② 21일간의 일중 강도 II 합을 21일간의 거래량 합으로 나누어 일중 강도율 II%를 구한다.
df['IIP21'] = df['II'].rolling(window=21).sum()/df['volume'].rolling(window=21).sum()*100  
df = df.dropna()

plt.figure(figsize=(9, 9))

plt.subplot(3, 1, 1)
plt.title('ACE 미국S&P500 Bollinger Band(20 day, 2 std) - Reversals')
plt.plot(df.index, df['close'], 'b', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'], 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

# ③ 3열 1행의 세 번째 그리드에 일중 강도율을 그린다.
plt.subplot(3, 1, 3)  
# ④ 녹색 실선으로 21일 일중 강도율을 표시한다.
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')  
plt.grid(True)
plt.legend(loc='best')

plt.show()