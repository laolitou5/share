from dateutil.parser import parse 
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import signal
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from statsmodels.tsa.seasonal import seasonal_decompose
plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})

# Import as Dataframe

def additive_multiplicative_decomposition(df):


    # Multiplicative Decomposition 
    #result_mul = seasonal_decompose(df['value'], model='multiplicative',extrapolate_trend='freq')

    # Additive Decomposition
    result_add = seasonal_decompose(df['value'], model='additive',extrapolate_trend='freq')

    # Plot
    plt.rcParams.update({'figure.figsize': (10,10)})
    #result_mul.plot().suptitle('Multiplicative Decompose', fontsize=22)
    result_add.plot().suptitle('Additive Decompose', fontsize=22)
    #plt.savefig('kk.png')
    #plt.close()
    plt.show()
    itype  = ''
    if itype == 'mul':
        return result_mul.trend, result_mul.seasonal, result_mul.resid
    elif itype == 'add':
        return result_add.trend, result_add.seasonal, result_add.resid
    
def test_for_stationarity(df):
    from statsmodels.tsa.stattools import adfuller, kpss
    
    # ADF Test  
    result = adfuller(df.value.values, autolag='AIC')
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    for key, value in result[4].items():
        print('Critial Values:')
        print(f'   {key}, {value}')

    # KPSS Test
    result = kpss(df.value.values, regression='c')
    print('\nKPSS Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    for key, value in result[3].items():
        print('Critial Values:')
        print(f'   {key}, {value}')
        
def detrend_time_series(df):

    # Using scipy: Subtract the line of best fit
    detrended = signal.detrend(df.value.values)
    plt.plot(detrended)
    plt.title('Drug Sales detrended by subtracting the least squares fit', fontsize=16)
    plt.show()
    
    # Using statmodels: Subtracting the Trend Component
    result_mul = seasonal_decompose(df['value'], model='multiplicative', extrapolate_trend='freq')
    detrended = df.value.values - result_mul.trend
    plt.plot(detrended)
    plt.title('Drug Sales detrended by subtracting the trend component', fontsize=16)
    plt.show()
    
def deseasonalize_time_series(df):

    # Time Series Decomposition
    result_mul = seasonal_decompose(df['value'], model='multiplicative', extrapolate_trend='freq')

    # Deseasonalize
    deseasonalized = df.value.values / result_mul.seasonal

    # Plot
    plt.plot(deseasonalized)
    plt.title('Drug Sales Deseasonalized', fontsize=16)
    plt.plot()
    plt.show()
    
    
def test_seasonality_of_time_series(df):

    # Draw Plot
    plt.rcParams.update({'figure.figsize':(9,5), 'figure.dpi':120})
    autocorrelation_plot(df.value.tolist())
    plt.show()
    
def autocorrelation_partialAutocorrelation(df):

    # Calculate ACF and PACF upto 50 lags
    # acf_50 = acf(df.value, nlags=50)
    # pacf_50 = pacf(df.value, nlags=50)

    # Draw Plot
    fig, axes = plt.subplots(1,2,figsize=(16,3), dpi= 100)
    plot_acf(df.value.tolist(), lags=50, ax=axes[0])
    plot_pacf(df.value.tolist(), lags=50, ax=axes[1])
    plt.show()
    

    
if __name__ == '__main__':

    #https://www.machinelearningplus.com/time-series/time-series-analysis-python/
    
    #df = pd.read_csv('000404.SZ.csv')
    
 
  
  
    df = pd.read_csv('a10.csv', parse_dates=['date'], index_col='date')
    dff = df.iloc[:10,:]
    df = pd.concat([df.iloc[:10, :], df.iloc[12:,:]])
    
    #df.index = df.index.astype(object)
    #df.sort_index(inplace=True)

    additive_multiplicative_decomposition(df)
    #test_for_stationarity(df)
    #detrend_time_series(df)
    #deseasonalize_time_series(df)
    #test_seasonality_of_time_series(df)
    #autocorrelation_partialAutocorrelation(df)