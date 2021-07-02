import numpy as np
from sko.GA import GA
from sklearn.metrics import mean_squared_error
import random

def demo(x):
    y = np.random.rand(4,3)
    y_test = np.array([7, 8, 9, 10])


    return np.sqrt(mean_squared_error(y_test,np.dot(y, x)))

ga = GA(func = demo, n_dim=3, size_pop = 200,max_iter=500, lb=[-1, -1, -1], ub=[2, 2, 2], precision=[1e-7, 1e-7, 1e-7])
best_x, best_y = ga.run()
print(best_x, best_y)