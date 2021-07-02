#
#https://beiyuan.me/python4finance-3/
import numpy as np
import math
import matplotlib.pyplot as plt


x0 = 0.15  # 初始利率
kappa = 3.0  # 回归系数
theta = 0.02  # 长期均值
sigma = 0.1  # 波动性
I = 10000
M = 100
T = 2.0
dt = T / M


def srd_euler():
    xh = np.zeros((M + 1, I))
    x = np.zeros_like(xh)
    xh[0] = x0
    x[0] = x0
    for t in range(1, M + 1):
        xh[t] = (xh[t - 1] +
                 kappa * (theta - np.maximum(xh[t - 1], 0)) * dt +
                 sigma * np.sqrt(np.maximum(xh[t - 1], 0)) *
                 math.sqrt(dt) * np.random.standard_normal(I))
    x = np.maximum(xh, 0)
    return x

x1 = srd_euler()

# plt.hist(x1[-1], bins=50)
# plt.xlabel('value')
# plt.ylabel('frequency')
# plt.show()

plt.plot(x1[:, :10], lw=1.5)
plt.xlabel('time')
plt.ylabel('index level')
plt.show()