#
import numpy as np
import matplotlib.pyplot as plt
import math


S0 = 100
r = 0.05
sigma = 0.25
T = 2.0
# simulation loops
I = 10000
ST = S0*np.exp((r - 0.5*sigma**2) * T +
               sigma * math.sqrt(T) * np.random.standard_normal(I))

ST_2 = S0 * np.random.lognormal((r - 0.5 * sigma ** 2) * T,  # the mean
                          sigma * math.sqrt(T),  # the standard deviation
                          size=I)
#
# plt.hist(ST, bins=50)
# plt.hist(ST_2,bins=50, alpha=0.5)
# plt.xlabel('index level')
# plt.ylabel('frequency')
# plt.legend(['by normal', 'by lognormal'])
# plt.show()

import scipy.stats as scs

def print_statistics(a1, a2):
    ''' Prints selected statistics.

    Parameters
    ==========
    a1, a2: ndarray objects
     results objects from simulation
    '''
    sta1 = scs.describe(a1)
    sta2 = scs.describe(a2)
    print('%14s %14s %14s' %
     ('statistic', 'data set 1', 'data set 2'))
    print(45 * "-")
    print('%14s %14.3f %14.3f' % ('size', sta1[0], sta2[0]))
    print('%14s %14.3f %14.3f' % ('min', sta1[1][0], sta2[1][0]))
    print('%14s %14.3f %14.3f' % ('max', sta1[1][1], sta2[1][1]))
    print('%14s %14.3f %14.3f' % ('mean', sta1[2], sta2[2]))
    print('%14s %14.3f %14.3f' % ('std', np.sqrt(sta1[3]),
                               np.sqrt(sta2[3])))
    print('%14s %14.3f %14.3f' % ('skew', sta1[4], sta2[4]))
    print('%14s %14.3f %14.3f' % ('kurtosis', sta1[5], sta2[5]))



# simulation loops
I = 10000
# simulation interval
M = 50

# T = 2.0
# S0 = 100
# r = 0.05
# sigma = 0.25


dt = T / M
S = np.zeros((M+1, I))
S[0] = S0
for t in range(1, M+1):
    S[t] = S[t-1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                           sigma * math.sqrt(dt) * np.random.standard_normal(I))
ST_3 = S[-1]
# plt.hist(ST, bins=50, alpha=0.5)
# plt.hist(ST_2,bins=50, alpha=0.5)
# plt.hist(ST_3,bins=50, alpha=0.5)
# plt.xlabel('index level')
# plt.ylabel('frequency')
# plt.legend(['by normal', 'by lognormal', 'by GBM'])
print_statistics(ST_3, ST_2)

plt.plot(S[:, :10], lw=1.5)
plt.xlabel('time')
plt.ylabel('index level')
plt.show()


from pylab import plt
plt.style.use('seaborn')
# %matplotlib inline
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad
mpl.rcParams['font.family'] = 'serif'


def dN(x):
    ''' Probability density function of standard normal random variable x. ''' 
    #标准正态随机变量 x 的概率密度函数
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d):
    ''' Cumulative density function of standard normal random variable x. '''
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def d1f(St, K, t, T, r, sigma):#设置函数d1
    ''' Black-Scholes-Merton d1 function.
        Parameters see e.g. BSM_call_value function. '''
    d1 = (math.log(St / K) + (r + 0.5 * sigma ** 2)* (T - t)) / (sigma * math.sqrt(T - t))
    return d1

#
# Valuation Functions
#

#欧式看涨期权函数
def BSM_call_value(St, K, t, T, r, sigma):
    ''' Calculates Black-Scholes-Merton European call option value.

    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility

    Returns
    =======
    call_value : float
        European call present value at t
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T - t)
    call_value = St * N(d1) - math.exp(-r * (T - t)) * K * N(d2)
    return call_value

#欧式看跌期权函数
def BSM_put_value(St, K, t, T, r, sigma):
    ''' Calculates Black-Scholes-Merton European put option value.

    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility

    Returns
    =======
    put_value : float
        European put present value at t
    '''
    put_value = BSM_call_value(St, K, t, T, r, sigma) - St + math.exp(-r * (T - t)) * K
    return put_value


St = 100.00  # initial index level
K = 100.00  # strike level
T = 1.  # call option maturity
r = 0.05  # constant short rate
sigma = 0.2  # constant volatility of diffusion
t=0


print('BSM模型求解的看涨期权价格为：',BSM_call_value(St, K, t, T, r, sigma))
print('BSM模型求解的看跌期权价格为：',BSM_put_value(St, K, t, T, r, sigma))