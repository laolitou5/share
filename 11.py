from numba import jit
from numba import vectorize, int64
import time
from sklearn.datasets import make_friedman2
import pandas as pd
import numpy as np
import timeit

# @vectorize([pandas.core.frame.DataFrame], target='parallel')

# @jit()
def add_ab(df):
    # a = list(range(500))
    # b = list(range(500))
    # d = list(range(500))
    # e = list(range(500))
    a = df['a'].values
    b = df['b'].values
    d = df['d'].values
    c = df['c'].values
    start = time.time()
    for i in range(50):
        for j in range(50):
            for k in range(50):
                # for l in range(50):
                # m = a*i + b*j + d*k
                # m = list(map(lambda x, y, z: i*x + j*y + k*z, a, b, c))
            # c = []
            # for l in range(500):
            #     c.append(a[l]*i + b[l]*j + d[l]*k)
            #     df['new'] = m

                df['new'] = df[['a', 'b', 'c', 'd']].apply(lambda x:x['a']*i+x['b']*j+x['c']*k, axis=1)
    print(time.time()-start)

X, y = make_friedman2(n_samples=500, noise=0, random_state=0)
df = pd.DataFrame(X, columns=['a', 'b', 'c', 'd'])
print(df)
print(type(df))
add_ab(df)