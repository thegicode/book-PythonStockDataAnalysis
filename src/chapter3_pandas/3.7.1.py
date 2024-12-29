import pandas as pd
import yfinance as yf
from scipy import stats

# 데이터 다운로드
dow = yf.download('^DJI', start='2000-01-04')
kospi = yf.download('^KS11', start='2000-01-04')

# 'Close' 데이터 병합
df = pd.DataFrame({'DOW': dow['Close'], "KOSPI": kospi['Close']})

# 결측치 제거
df = df.dropna()

# 상관계수
corr = df.corr()

# 결과 출력
print(corr)

#             DOW     KOSPI
# DOW    1.000000  0.819173
# KOSPI  0.819173  1.000000

### 3.7.2 시리즈로 상관계수 구하기
r_value = df['DOW'].corr(df['KOSPI'])
print(r_value)
# 0.8191730265666881

### 3.7.3 결정계수 R-squared 구하기
# 결정계수는 상관계수를 제곱
r_squared = r_value ** 2
print(r_squared)
# 0.6710444474544279