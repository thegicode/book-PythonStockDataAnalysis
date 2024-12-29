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

# 선형 회귀 분석
regr = stats.linregress(df['DOW'], df["KOSPI"])

# 결과 출력
print(regr)


# LinregressResult(
#                  slope=np.float64(0.05991912851129757),  기울기
#                  intercept=np.float64(686.4233316136774), y절편
#                  rvalue=np.float64(0.8191730265666882), r값(상관계수)
#                  pvalue=np.float64(0.0),      p값
#                  stderr=np.float64(0.0005431918325983483),  표준편차
#                  intercept_stderr=np.float64(10.97618022475815))

# y = 686 + 0.059 * x