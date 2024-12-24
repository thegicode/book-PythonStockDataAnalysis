import numpy as np
import matplotlib.pyplot as plt

def relu(x):
    # 1. 넘파의 maximum() 함수는 인수로 주어진 수 중에서 가장 큰 수를 변환
    # 따라서 x가 0보다 작거나 같을 때 0을 반환하고, x가 0보다 크면 x를 반환
    return  np.maximum(0, x)

# 2. 
x = np.arange(-10, 10, 0.1)
print(x)

# 3.
y = relu(x)
print(y)

plt.plot(x, y)
plt.title('tanh function')
plt.show()