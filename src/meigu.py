import akshare as ak
import pandas as pd
import os
import shutil
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from datetime import datetime
import mpl_finance as mpf

#https://pypi.org/project/qhsdk/0.0.2/

def read_data(symbol):
    stock_us_daily_df = ak.stock_us_daily(symbol=symbol, adjust="qfq")
    stock_us_daily_df.reset_index(inplace=True)
    # stock_us_daily_df['date'] = stock_us_daily_df.index.tolist()
    stock_us_weekly_df = cal_week_line(stock_us_daily_df, period_type='W')
    stock_us_weekly_df.reset_index(inplace=True)
    return stock_us_daily_df, stock_us_weekly_df

def read_data_hk(code):
    stock_hk_daily_df = ak.stock_hk_daily(symbol=code, adjust="qfq")
    stock_hk_daily_df.reset_index(inplace=True)
    stock_hk_daily_df.rename(columns={'index':'date'}, inplace=True)

    stock_hk_weekly_df = cal_week_line(stock_hk_daily_df, period_type='W')
    stock_hk_weekly_df.reset_index(inplace=True)

    return stock_hk_daily_df, stock_hk_weekly_df



def cal_week_line(stock_data:pd.DataFrame(), period_type='W'):

    stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y-%m-%d')
    stock_data.set_index('date', inplace=True)

    k_open = pd.DataFrame(stock_data.resample(period_type).first()['open'])
    k_close = pd.DataFrame(stock_data.resample(period_type).last()['close'])
    period_stock_data = k_open.join(k_close)

    k_hight = stock_data.resample(period_type).max()['high']
    period_stock_data = period_stock_data.join(k_hight)

    k_low = stock_data.resample(period_type).min()['low']
    period_stock_data = period_stock_data.join(k_low)

    k_volume = stock_data.resample(period_type).sum()['volume']
    period_stock_data = period_stock_data.join(k_volume)

    # # 股票在有些周一天都没有交易，将这些周去除
    # period_stock_data = period_stock_data[period_stock_data['stockName'].notnull()]
    return period_stock_data


def getcandlecharts(codes, ktype, itime):
    # chinese = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
    """
    plot蜡烛图
    codes:股票code list
    ktype:获取股票的周期，D代表每天，W代表每周，M代表每月
    """
    index = 1
    absolute_path = os.getcwd()
    print('是否存在plot_mg文件:', os.path.exists(os.path.join(absolute_path, '../plot_mg')))
    if os.path.exists(os.path.join(absolute_path, '../plot_mg')):
        shutil.rmtree('../plot_mg')
        os.mkdir('../plot_mg')
    else:
        os.mkdir('../plot_mg')


    for code in codes:
        try:
            print(code)
            stock_daily_df, stock_weekly_df = read_data(code)

            if ktype == 'D':
                shyh = stock_daily_df
                shyh.reset_index(inplace=True)
            if ktype == 'W':
                shyh = stock_weekly_df
            shyh = shyh[shyh.date>=itime]
            if len(shyh) > 0:
                plt.figure(figsize=(20, 12), facecolor='w')
                # num_time = dt.date2num([datetime.strptime(str(ele), '%Y-%m-%d') for ele in shyh.date.tolist()])
                num_time = dt.date2num(shyh.date.tolist())
                shyh['date'] = num_time
                ax = plt.subplot(1, 1, index)
                mpf.candlestick_ochl(ax, zip(shyh.date, shyh.open, shyh.close, shyh.high, shyh.low), width=2,
                                     colorup="r", colordown="g", alpha=1.0)
                plt.grid(True)
                plt.xticks(rotation=30)
                plt.title('%s'%code)
                plt.xlabel("Date")
                plt.ylabel("Price")
                ax.xaxis_date()
                plt.savefig('../plot_mg/%s.png'%code)
                plt.close()
        except Exception as e:
            print('error', code)


def getcandlecharts_hk(codes, ktype, itime):
    # chinese = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
    """
    plot蜡烛图
    codes:股票code list
    ktype:获取股票的周期，D代表每天，W代表每周，M代表每月
    """
    index = 1
    absolute_path = os.getcwd()
    print('是否存在plot_hk文件:', os.path.exists(os.path.join(absolute_path, '../plot_hk')))
    if os.path.exists(os.path.join(absolute_path, '../plot_hk')):
        shutil.rmtree('../plot_hk')
        os.mkdir('../plot_hk')
    else:
        os.mkdir('../plot_hk')


    for code in codes:
        try:
            print(code)
            stock_daily_df, stock_weekly_df = read_data_hk(code)

            if ktype == 'D':
                shyh = stock_daily_df
                shyh.reset_index(inplace=True)
            if ktype == 'W':
                shyh = stock_weekly_df
            shyh = shyh[shyh.date>=itime]
            if len(shyh) > 0:
                plt.figure(figsize=(20, 12), facecolor='w')
                # num_time = dt.date2num([datetime.strptime(str(ele), '%Y-%m-%d') for ele in shyh.date.tolist()])
                num_time = dt.date2num(shyh.date.tolist())
                shyh['date'] = num_time
                ax = plt.subplot(1, 1, index)
                mpf.candlestick_ochl(ax, zip(shyh.date, shyh.open, shyh.close, shyh.high, shyh.low), width=1.6,
                                     colorup="r", colordown="g", alpha=1.0)
                plt.grid(True)
                plt.xticks(rotation=30)
                plt.title('%s'%code)
                plt.xlabel("Date")
                plt.ylabel("Price")
                ax.xaxis_date()
                plt.savefig('../plot_hk/%s.png'%code)
                plt.close()
        except Exception as e:
            print('error', code)


def bbands_plot(code, ktype, itime):
    """boll线"""

    absolute_path = os.getcwd()
    print('是否存在boll_plot_mg文件:', os.path.exists(os.path.join(absolute_path, '../boll_plot_mg')))
    if os.path.exists(os.path.join(absolute_path, '../boll_plot_mg')):
        shutil.rmtree('../boll_plot_mg')
        os.mkdir('../boll_plot_mg')
    else:
        os.mkdir('../boll_plot_mg')


    for ele in code:
        # try:
            print(ele)
            stock_us_daily_df, stock_us_weekly_df = read_data(ele)
            if ktype == 'D':
                df = stock_us_daily_df
                df['date'] = df.index.tolist()
            if ktype == 'W':
                df = stock_us_weekly_df
            df.rename(columns={'date':'trade_date'}, inplace=True)
            df = df.sort_values(by='trade_date', ascending=True)
            upper, middle, lower = talib.BBANDS(df['close'].values, timeperiod=25, nbdevup=2, nbdevdn=2, matype=0)
            df['boll_upper'] = upper
            df['boll_middle'] = middle
            df['boll_lower'] = lower
            df = df[df.trade_date >= itime]
            df.set_index('trade_date', inplace=True)
            df.sort_index(inplace=True)

            plt.plot(df.close, "k", label='closed')
            plt.plot(df.boll_upper, label='upper')
            plt.plot(df.boll_middle, label='middle')
            plt.plot(df.boll_lower, label='lower')
            # tick_spacing = 7
            plt.xticks(rotation=60)
            plt.legend()
            plt.grid(True)
            plt.title('%s' % ele)
            plt.xlabel("Date")
            plt.ylabel("boll")
            plt.savefig('../boll_plot_mg/%s.png' % ele)
            plt.close()
        # except Exception as e:
        #     print('error:', ele)


if __name__ == '__main__':

    data = pd.read_csv('meiguo_.csv')
    category = list(set(data['category'].tolist()))
    print(category)
    data = data[data.category=='半导体']
    ktype = 'W' #D, W
    itime = '20200601'
    codes = data.symbol.tolist()
    #k 线
    getcandlecharts(codes, ktype, itime)
    # ktype = 'D'  # D, W
    # #boll 线
    # bbands_plot(codes, ktype, itime)

    # #港股
    # # current_data_df = ak.stock_hk_spot()
    # # current_data_df.to_csv('ganggu.csv', index=False)
    # df_hk = pd.read_csv('ganggu.csv',converters={'symbol': str})
    # codes = df_hk.symbol.tolist()
    # ktype = 'W' #D, W
    # itime = '20200601'
    # getcandlecharts_hk(codes, ktype, itime)

    #中概股