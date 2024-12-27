import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../')) 
sys.path.append(project_root)  

from src.MarketDB import MarketDB 

### 9.4.3 주가 예측

mk = MarketDB()
# raw_df = mk.get_daily_price('메리츠금융지주', '2020-11-26', '2024-12-26')
# raw_df = mk.get_daily_price('TIGER 미국채10년선물', '2020-11-26', '2024-12-26')
raw_df = mk.get_daily_price('삼성전자', '2020-11-26', '2024-12-26')


data_size = 5

def MinMaxScaler(data):
    """최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)

dfx = raw_df[['open','high','low','volume', 'close']]
dfx = MinMaxScaler(dfx) # 0~1 사잇값으로 변환 
# print(dfx.info) # OHLCV 가격 정보
dfy = dfx[['close']] 


### 9.4.4 데이터넷 준비하기

x = dfx.values.tolist()
y = dfy.values.tolist()

data_x = []
data_y = []
window_size = 10 
# 이전 10일 동안 OHLCV 데이터를 이용하여 다음 날 종가를 예측
# _x : 이전 10일 동안 OHLCV 데이터
# _y : 다음 10일 동안 OHLCV 데이터
for i in range(len(y) - window_size):
    _x = x[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
    _y = y[i + window_size]     # 다음 날 종가
    data_x.append(_x)
    data_y.append(_y)
print(_x, "->", _y)


### 9.4.5 훈련용 데이터셋과 테스트용 데이터셋 분리

# 훈련용 데이터셋
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[0 : train_size])
train_y = np.array(data_y[0 : train_size])

# 테스트용 데이터셋
test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size : len(data_x)])
test_y = np.array(data_y[train_size : len(data_y)])


### 9.4.6 모델 생성하기
# 시퀜셜 모델 객체를 생성
model = Sequential() 
# window_size를 10으로 설정했으므로 (10, 5) 입력 형태를 가지는 LSTM층을 추가, 전체 유닛 개수는 10개, 활성화함수는 relu
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, data_size)))
# 드롭아웃을 10%로 지정. 드롭아웃층은 입력값의 일부분을 선택해서 그 값을 0으로 치환하여 다음층으로 출력함으로써 훈련 데이터를 늘리지 않고도 과적합을 방지할 수 있다. 
model.add(Dropout(0.1)) 
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
# 유닛이 하나인 출력층을 추가
model.add(Dense(units=1))
model.summary()

# 최적화 도구는 adam을 사용, 손실 함수는 평균 제곱 오차(MSE)를 사용
model.compile(optimizer='adam', loss='mean_squared_error')
# 훈련용 데이터셋으로 모델 학습. epochs는 전체 데이터셋에 대한 학습 횟수, batch_size는 한 번에 제공되는 훈련 데이터 개수
model.fit(train_x, train_y, epochs=60, batch_size=30)
# 테스트 데이터셋을 이용하여 에측치 데이터셋을 생성
pred_y = model.predict(test_x)

# Visualising the results
plt.figure()
plt.plot(test_y, color='red', label='real SEC stock price')
plt.plot(pred_y, color='blue', label='predicted SEC stock price')
plt.title('SEC stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()


### 9.4.8 예측치와 실제 종가 비교

# raw_df.close[-1] : dfy.close[-1] = x : pred_y[-1]
# print("Tomorrow's SEC price :", raw_df.close[-1] * pred_y[-1] / dfy.close[-1], 'KRW')
print("Tomorrow's SEC price :", raw_df.close.iloc[-1] * pred_y[-1] / dfy.close.iloc[-1], 'KRW')
