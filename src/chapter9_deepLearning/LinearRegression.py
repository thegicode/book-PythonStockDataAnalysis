import matplotlib.pylab as plt
import tensorflow as tf


### 9.3.1 선형 모델

# ① y = 1 * x + 1 데이터 준비
x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 4, 5, 6]

# ② 가중치 w를 임의의 값 0.7로 초기화, 초기값과 실제 w값의 차이가 적을수록 학습에 걸리는 시간도 줄어든다.
w = tf.Variable(0.7)
# ③ 가중치 b를 임의의 값 0.7로 초기화, 초기값과 실제 b값의 차이가 적을수록 학습에 걸리는 시간도 줄어든다.
b = tf.Variable(0.7)
# ④ 학습률은 보통 0.01 ~ 0.001 사이의 값으로 설정
# 학습률이 너무 크면 비용이 무한대로 늘어나는 오버슈팅 현상이 발생하면서 학습이 제대로 이루어지지 않고,
# 학습률이 너무 작으면 학습에 걸리는 시간이 오래 걸리므로 적절한 학습률을 설정하는 것이 중요하다.
learn_rate = 0.01


### 9.3.2 경사 하강 알고리즘 gradient descent algorithm

print(f'step|    w|    b| cost')
print(f'----|-----|-----|-----')

# ⑦ 1회부터 1100회까지 반복해서 학습
for i in range(1, 1101): 
    #  ⑧ 내부의 계산 과정을 tape에 기록해두면, 나중에 tape.gradient() 함수를 이용해서 미분값을 구할 수 있다.
    with tf.GradientTape() as tape:
        # ⑨ 가설은 w * x + b로 정한다
        hypothesis = w * x_data + b
        # ⑩ 손실 비용을 오차제곱평균으로 구한다. 
        cost = tf.reduce_mean((hypothesis - y_data)**2) # tf.losses.mean_squared_error(y, y_hat)도 동일
    # 11. w와 b에 대해 손실을 미분해서 dw, db 값을 구한다.
    dw, db = tape.gradient(cost, [w, b])

    # 12. 텐서플로의 a.assign_sub(b)는 파이썬의 a = a - b와 동일한 연산을 수행한다. 
    # w값에서 '학습룰 * dw'를 뺀 값을 새로운 w값으로 설정
    w.assign_sub(learn_rate * dw) # a = a - b
    b.assign_sub(learn_rate * db) 
    
    if i in [1, 3, 5, 10, 1000, 1100]:
        print(f"{i:4d}| {w.numpy():.2f}| {b.numpy():.2f}| {cost:.2f}")
        plt.figure(figsize=(7, 7))
        plt.title(f'[Step {i:d}]  h(x) = { w.numpy():.2f}x + {b.numpy():.2f}')
        plt.plot(x_data, y_data, 'o') # ⑥
        plt.plot(x_data, w * x_data + b, 'r', label='hypothesis') # ⑦
        plt.xlabel('x_data')
        plt.ylabel('y_data')
        plt.xlim(0, 6)
        plt.ylim(1, 7)
        plt.legend(loc='best')
        plt.show()

