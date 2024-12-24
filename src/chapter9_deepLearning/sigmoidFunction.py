import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    # 1. 넘파이의 exp(x) 함수는 e^{-x}를 구하는 지수 함수다. 
    # x값이 0으로부터 음수 방향으로 멀어지면 분모(1 + np.exp(-x))의 값이 커지므로 y값은 0에 가까워진다. 
    # x값이 0으로부터 양수 방향으로 멀어지면 exp(-x)가 0에 가까워지므로 y값에 1에 가까워진다. 
    return 1 / (1 + np.exp(-x))

# 2. 
x = np.arange(-10, 10, 0.1)
print(x)

# 3
y = sigmoid(x)
print(y)

plt.plot(x, y)
plt.title('sigmoid function')
plt.show()