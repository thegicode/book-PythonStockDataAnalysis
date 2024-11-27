"""
5.1 야후 파이낸스와 네이버 금융 비교하기
data visualization를 거치면 단순히 시각적으로 보기 좋을 뿐만 아니라, 수치만 봤을 때에는 알 수 없었떤 정보를 발견할 수도 있다.

5.1.1 야후 파이낸스 데이터의 문제점
야후 파이앤스 과거 데이터가 잘못되어 있다.
"""

import yfinance as yf
import matplotlib.pyplot as plt

df = yf.download('005930.KS', start='2017-01-01')


plt.figure(figsize=(9, 6))

# 2행 1열 영역에서 첫 번째 영역을 선택한다.
plt.subplot(2, 1, 1)

plt.title('Samsung Electronics (Yahoo Fianace)')

# 삼성전자 종가 (Close)를 청록샐 실선으로 표시한다.
plt.plot(df.index, df['Close'], 'c', label='Close')

# 삼성전자의 수정 종가(Adj Close)를 파란색 점선으로 표시힌다.
plt.plot(df.index, df['Adj Close'], 'b--', label='Adj Clsoe')

plt.legend(loc='best')

# 2행 1열의 영역에서 두 번째 영역을 선택한다.
plt.subplot(2, 1, 2)

# 삼성전자 거래량을 바 차트로 그린다.
plt.bar(df.index, df['Volume'], color='g', label='Volume')

plt.legend(loc='best')
plt.show()

