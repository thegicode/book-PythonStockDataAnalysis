import numpy as np
import matplotlib.pyplot as plt

def softmax(x):
    return  np.exp(x) / np.sum(np.exp(x))

y = softmax([1, 1, 2])
print(y)
# [0.21194156 0.21194156 0.57611688]

