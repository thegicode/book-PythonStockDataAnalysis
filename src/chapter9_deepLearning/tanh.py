import numpy as np
import matplotlib.pyplot as plt

def tahn(x):
    return  (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

# 1. x값으로 -10부터 9.9까지 0.1 간격의 소수로 이루어진 배열
x = np.arange(-10, 10, 0.1)
print(x)

y = tahn(x)
print(y)

plt.plot(x, y)
plt.title('tanh function')
plt.show()