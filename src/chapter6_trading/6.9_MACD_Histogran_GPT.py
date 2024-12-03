import os
import sys
from matplotlib import pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 


mk = MarketDB()
df = mk.get_daily_price('SK하이닉스', '2024-01-04')

# MACD 및 Signal Line 계산
short_window = 12
long_window = 26
signal_window = 9

df['EMA12'] = df['close'].ewm(span=short_window, adjust=False).mean()
df['EMA26'] = df['close'].ewm(span=long_window, adjust=False).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['Signal'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
df['MACD_Histogram'] = df['MACD'] - df['Signal']

# MACD 히스토그램 기울기 계산
df['MACD_Histogram_Slope'] = df['MACD_Histogram'].diff()

# 매수/매도 신호 정의
df['Buy_Signal'] = (df['MACD_Histogram'] < 0) & (df['MACD_Histogram_Slope'] > 0)
df['Sell_Signal'] = (df['MACD_Histogram'] > 0) & (df['MACD_Histogram_Slope'] < 0)

# 히스토그램의 기울기 변화에 따라 매수/매도 신호를 추가로 시각화
plt.figure(figsize=(14, 10))

# Close Price Plot
plt.subplot(3, 1, 1)
plt.plot(df['close'], label="Close Price", color="blue")
plt.title("Close Price")
plt.legend()

# MACD Plot
plt.subplot(3, 1, 2)
plt.plot(df['MACD'], label="MACD Line", color="green")
plt.plot(df['Signal'], label="Signal Line", color="red")
plt.bar(df.index, df['MACD_Histogram'], label="MACD Histogram", color="blue", alpha=0.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.scatter(df.index[df['Buy_Signal']], df['MACD'][df['Buy_Signal']], marker='^', color='red', label='Buy Signal', s=50)
plt.scatter(df.index[df['Sell_Signal']], df['MACD'][df['Sell_Signal']], marker='v', color='blue', label='Sell Signal', s=50)
plt.title("MACD, Signal Line, and MACD Histogram with Buy/Sell Signals")
plt.legend()

# 히스토그램 기울기 변화 시각화
plt.subplot(3, 1, 3)
plt.plot(df['MACD_Histogram'], label="MACD Histogram", color="blue")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.scatter(df.index[df['Buy_Signal']], df['MACD_Histogram'][df['Buy_Signal']], marker='^', color='red', label='Buy Signal', s=50)
plt.scatter(df.index[df['Sell_Signal']], df['MACD_Histogram'][df['Sell_Signal']], marker='v', color='blue', label='Sell Signal', s=50)
plt.plot(df['MACD_Histogram'], label="MACD Histogram Slope", linestyle='--', color="orange", alpha=0.7)
plt.title("MACD Histogram with Slope-Based Buy/Sell Signals")
plt.legend()

plt.tight_layout()
plt.show()