def OR(x1, x2):
    w1 = 0.5
    w2 = 0.5
    thetha = 0.2
    if w1 * x1 + w2 * x2 > thetha:
        return 1
    else:
        return 0
    


print(OR(0, 0))
# 0

print(OR(0, 1))
# 1

print(OR(1, 0))
# 1

print(OR(1, 1))
# 1