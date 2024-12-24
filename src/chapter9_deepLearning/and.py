def AND(x1, x2):
    w1 = 0.5
    w2 = 0.5
    theta = 0.7
    if w1 * x1 + w2 * x2 > theta:
        return 1
    else:
        return 0

print(AND(0, 0))
# 0

print(AND(0, 1))
# 0

print(AND(1, 0))
# 0

print(AND(1, 1))
# 1