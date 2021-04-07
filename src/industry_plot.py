#
key = '75f7cbe506f185ba42bf382701b21f5e599482881eda3dd639fd8eb2'

import tushare as ts
pro = ts.pro_api(key)
import numpy as np
import scipy.stats
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr
from share import getcandlecharts
import shutil
import talib
import mpl_finance as mpf
from datetime import datetime
import matplotlib.dates as dt
import os
import matplotlib.pyplot as plt
from kk import additive_multiplicative_decomposition
from datetime import datetime, timedelta
from opendatatools import swindex
import re
import time
    

class Dog(object):

    def __init__(self, start, end, tm):
        """
        获取数据的开始时间和结束时间
        start:获取股票的起始时间，尽量靠前
        end: 获取股票的最新时间
        tm: 画图的起始时间
        """
        self.start=start
        self.end=end
        self.tm = tm


    def KL_divergence(self, p,q):
        """通过kl散度判断p和q的分布的相似度/距离"""
        return scipy.stats.entropy(p, q)


    def JS_divergence(self, p, q):
        """通过js散度判断p和q的分布的相似度/距离"""
        M = [(p[i]+q[i])/2 for i in range(len(q))]
        return 0.5 * scipy.stats.entropy(p, M) + 0.5 * scipy.stats.entropy(q, M)


    def ipearsonr(self, x, y):
        """Pearson correlation coefficient and p-value for testing non-correlation."""
        return pearsonr(x, y)


    def data(self):
        """沪深港通资金流向"""
        # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,total_mv,circ_mv')
        # data = pro.daily_basic(ts_code='002414.SZ', trade_date='20210208')
        data_1 = pro.moneyflow_hsgt(start_date='20180125', end_date='20210208')
        data_2 = pro.hsgt_top10(trade_date='20210205', market_type='1')
        return data_2


    def __code_day_data(self, code):
        """获取确定code下指定时间段的日线数据"""
        df = pro.daily(ts_code=code, start_date=self.start, end_date=self.end)
        return df


    def __code_week_data(self, code):
        """获取确定code下指定时间段的周线数据"""
        df = pro.weekly(ts_code=code, start_date=self.start, end_date=self.end, fields='ts_code,trade_date,open,high,low,close,vol,amount')
        return df

    def code_data(self, code, ktype):
        """
        根据ktype类型获取数据
        ktype=='D',获取日数据
        ktype==‘W’, 获取周数据
        ktype=='M', 获取月数据
        """

        if ktype == 'W':
            df = self.__code_week_data(code)
        elif ktype == 'D':
            df = self.__code_day_data(code)
        elif ktype == 'M':
            df = self.__code_month_data(code)

        return df


    def __code_month_data(self, code):
        """获取确定code下指定时间段的周线数据"""
        df = pro.monthly(ts_code=code, start_date=self.start, end_date=self.end,
                         fields='ts_code,trade_date,open,high,low,close,vol,amount')
        return df


    def industry_statistics(self, df):
        """按照行业 vol 统计信息"""
        industry_list = list(set(df['industry'].tolist()))
        df_industry_statistics = pd.DataFrame()
        code_list = []
        vol_list = []
        industry_ = []
        for ele in industry_list:
            print(ele)
            codes = df[df.industry == ele]['ts_code'].tolist()
            for k in codes:
                code_list.append(k)
                vol_list.append(pro.daily(ts_code=k, start_date=self.start, end_date=self.end)['vol'].sum())
                industry_.append(ele)
        df_industry_statistics['code'] = code_list
        df_industry_statistics['vol'] = vol_list
        df_industry_statistics['industry'] = industry_
        df_industry_statistics.to_csv('industry.csv')
        return df_industry_statistics.groupby('industry').sum()

    def shenwan_industry(self):
        """申万一级行业分类 ：https://www.cnblogs.com/ttrrpp/p/12715790.html"""

        df, msg = swindex.get_index_list()
        indu = df[df.section_name == '一级行业']

        return indu

    def diff_(self, l):
        diff = [0]
        for i in range(1, len(l)):
            diff.append(l[i] - l[i - 1])

        return diff

    def bx_add_closePrice(self):
        df_1 = pd.read_csv('data/bs_hist_merge.csv', converters={'code': str})
        df_1['date'] = df_1[['date']].apply(lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), axis=1)
        k = list(set(df_1.symbol.tolist()))
        kk = []
        s = 0
        for ele in k:
            s += 1
            df = self.code_data(ele, 'D')[['ts_code', 'trade_date', 'close']]
            df['trade_date'] = df[['trade_date']].apply(lambda x: datetime.strptime(x['trade_date'], '%Y%m%d'), axis=1)
            df.rename(columns={'ts_code':'symbol', 'trade_date':'date'}, inplace=True)
            df2 = pd.merge(df_1, df, on=['symbol', 'date'])
            kk.append(df2)
            print(s)

        d = pd.concat(kk)
        d.to_csv('data/bs_hist_merge_new.csv', index=False)

    def data_sar(self, code, ktype):

        # 买卖原则为：
        # index = DIF-DEA均为正，买入信号参考。
        # index= DIF-DEA均为负，卖出信号参考。

        df = self.code_data(code, ktype)
        df.rename(columns={'ts_code': 'code', 'trade_date': 'date'}, inplace=True)
        df = df.sort_values(by='date', ascending=True)
        df['date'] = df[['date']].apply(lambda x: datetime.strptime(x['date'], '%Y%m%d'), axis=1)

        # df["MACD_macd"], df["MACD_macdsignal"], df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26,
        #                                                                          signalperiod=9)
        # df['macd_index'] = df["MACD_macd"] - df["MACD_macdsignal"]
        # df['macd_index_diff'] = self.diff_(df['macd_index'].tolist())
        df['SAR'] = talib.SAR(df.high, df.low, acceleration=0.04, maximum=0.2)
        df['SAR_diff'] = self.diff_(df['SAR'].tolist())
        df['SAR_close_diff'] = df['SAR'] - df.close
        # df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        # df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

        df.dropna(inplace=True)
        return df[['date', 'close', 'SAR','SAR_diff', 'SAR_close_diff']]


    def shenwan_industry_code(self, df_s, indu):
        """indu: 行业"""

        df = self.shenwan_industry()
        index_code = df[df.index_name == indu].index_code.tolist()[0]
        df1, msg1 = swindex.get_index_cons(index_code)

        d1 = pd.merge(df1, df_s, left_on='stock_code', right_on='code')
        return d1.symbol.tolist()




    def bx_in_out(self, start_time, end_time):

        """
        plot bar
        start_time 和 end_time 间 申万一级行业的资金变化
        """

        df_all = pd.read_csv('../data/bs_hist_merge_new.csv', converters={'code': str})
        df_all['date'] = df_all[['date']].apply(lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), axis=1)
        df_all['shareholding'] = df_all[['shareholding']].apply(lambda x:float(re.sub(r',', '', str(x['shareholding']))), axis=1)
        df_s = df_all[df_all['date'] == start_time]
        df_e = df_all[df_all['date'] == end_time]
        indu = self.shenwan_industry()

        s_vol = []
        e_vol = []
        indu_name = []
        for ele in indu[['index_code', 'index_name']].values:
            df1, msg1 = swindex.get_index_cons(ele[0])
            d1 = pd.merge(df1, df_s, left_on = 'stock_code', right_on='code')
            d2 = pd.merge(df1, df_e, left_on = 'stock_code', right_on = 'code')
            indu_name.append(ele[1])
            s_vol.append(d1.shareholding.sum()/1e+8)
            e_vol.append(d2.shareholding.sum()/1e+8)

        bar_width = 0.3

        plt.bar(x=range(len(indu_name)), height=s_vol, label=start_time, color='steelblue', alpha=0.8, width=bar_width)
        # 将X轴数据改为使用np.arange(len(x_data))+bar_width,
        # 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了
        plt.bar(x=np.arange(len(indu_name)) + bar_width, height=e_vol, label=end_time, color='indianred', alpha=0.8, width=bar_width)
        # 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
        for x1, yy in enumerate(s_vol):
            plt.text(x1, yy + 1, indu_name[x1], ha='center', va='bottom', fontsize=8, rotation=60)
        for x1, yy in enumerate(e_vol):
            plt.text(x1 + bar_width, yy + 1, str(' '), ha='center', va='bottom', fontsize=5, rotation=60)

        # 设置标题
        plt.title("北向资金变化")
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 为两条坐标轴设置名称
        plt.xlabel("行业")
        plt.ylabel("总量")
        # 显示图例
        plt.legend()
        plt.savefig("industry.jpg")
        plt.show()

    def bx_in_out_indu(self, start_time, end_time):

        """
        plot bar
        start_time 和 end_time 间 申万一级行业的资金变化
        """

        df_all = pd.read_csv('data/bs_hist_merge_new.csv', converters={'code': str})
        df_all['date'] = df_all[['date']].apply(lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), axis=1)
        df_all['shareholding'] = df_all[['shareholding']].apply(
            lambda x: float(re.sub(r',', '', str(x['shareholding']))), axis=1)
        df_s = df_all[(df_all['date'] >= start_time)&(df_all['date']<=end_time)]
        indu = self.shenwan_industry()

        s = []
        for ele in indu[['index_code', 'index_name']].values:
            df1, msg1 = swindex.get_index_cons(ele[0])
            df1.rename(columns={'stock_code':'code'}, inplace=True)
            d1 = pd.merge(df1[["code", "stock_name"]], df_s, on='code')
            d2 = pd.DataFrame(d1.groupby(['date'])['shareholding'].sum())
            d2.rename(columns={'shareholding':ele[1]}, inplace=True)
            s.append(d2)
        result = pd.concat(s, axis=1)
        print(result)
        result[['银行', '化工', '电气设备', '有色金属', '钢铁']].plot()
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.show()
        
        
    def bx_in_out_stock(self, start_time, end_time):

        """
        plot bar
        start_time 和 end_time 间 申万一级行业的资金变化
        """

        df_all = pd.read_csv('data/bs_hist_merge_new.csv', converters={'code': str})
        df_all['date'] = df_all[['date']].apply(lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), axis=1)
        df_all['shareholding'] = df_all[['shareholding']].apply(
            lambda x: float(re.sub(r',', '', str(x['shareholding']))), axis=1)
        df_s = df_all[(df_all['date'] >= start_time)&(df_all['date']<=end_time)]

        # df_s.sort_values(by='col1', ascending=True, inplace)
        return df_s.head(10) 



    def generate_date_series(self, itime, nums):

        """产生连续时间序列"""
        times_list = []
        ss = datetime.strptime(itime, '%Y%m%d')
        for i in range(nums):
            sss = ss - timedelta(hours=24*i)
            times_list.append(sss)

        return times_list



    def getcandlecharts(self, codes, ktype):
        # chinese = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
        """
        plot蜡烛图
        codes:股票code list
        ktype:获取股票的周期，D代表每天，W代表每周，M代表每月
        """
        index = 1
        absolute_path = os.getcwd()
        print('是否存在plot文件:', os.path.exists(os.path.join(absolute_path, '../plot')))
        if os.path.exists(os.path.join(absolute_path, '../plot')):
            shutil.rmtree('../plot')
            os.mkdir('../plot')
        else:
            os.mkdir('../plot')


        for code in codes:
            try:
                print(code)
                shyh = self.code_data(code, ktype)
                shyh.rename(columns={'ts_code': 'code', 'trade_date': 'date'}, inplace=True)
                shyh = shyh[shyh.date>=self.tm]
                if len(shyh) > 0:
                    plt.figure(figsize=(20, 12), facecolor='w')
                    num_time = dt.date2num([datetime.strptime(ele, '%Y%m%d') for ele in shyh.date.tolist()])
                    shyh['date'] = num_time
                    ax = plt.subplot(1, 1, index)
                    mpf.candlestick_ochl(ax, zip(shyh.date, shyh.open, shyh.close, shyh.high, shyh.low), width=0.6,
                                         colorup="r", colordown="g", alpha=1.0)
                    plt.grid(True)
                    plt.xticks(rotation=30)
                    plt.title('%s'%code)
                    plt.xlabel("Date")
                    plt.ylabel("Price")
                    ax.xaxis_date()
                    plt.savefig('../plot/%s.png'%code)
                    plt.close()
            except Exception as e:
                print('error', code)
            
    def trend(self, code, itype):
        """trend"""

        absolute_path = os.getcwd()
        print('是否存在trend_plot文件:', os.path.exists(os.path.join(absolute_path, 'trend_plot')))
        if os.path.exists(os.path.join(absolute_path, 'trend_plot')):
            shutil.rmtree('trend_plot')
            os.mkdir('trend_plot')
        else:
            os.mkdir('trend_plot')

        for ele in code:
            df = self.code_data(ele, itype)
            df = df[df.trade_date >= self.start]
            df.rename(columns={'close': 'value'}, inplace=True)
            df['date'] = self.generate_date_series(self.end, df.shape[0])
            df.sort_index(inplace=True)
            df[['date', 'value']].to_csv('%s.csv' % ele, index=False)
            df = pd.read_csv('%s.csv' % ele, parse_dates=['date'], index_col='date')
            os.remove('%s.csv' % ele)
            additive_multiplicative_decomposition(df, ele)

    def bbands(self, code, ktype):
        """boll 计算"""

        df_list = []
        for ele in code:
            df = self.code_data(ele, ktype)
            df = df.sort_values(by='trade_date', ascending=True)
            upper, middle, lower = talib.BBANDS(df['close'].values, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            df['boll_upper'] = upper
            df['boll_middle'] = middle
            df['boll_lower'] = lower
            df['boll_upper_diff'] = df['boll_upper'].diff().tolist()
            df['boll_lower_diff'] = df['boll_lower'].diff().tolist()
            df['close_diff'] = df['close'].diff().tolist()
            df_list.append(df)
        df = pd.concat(df_list)
        return df

    def bbands_policy1(self, df):
        """boll 策略"""

        codes = list(set(df[df.ts_code].tolist()))
        print(codes)
        hs = []
        for ele in codes:
            print(df[df.ts_code == ele])
            x = df[df.ts_code == ele].tail(5)['boll_upper_diff'].sum()
            y = df[df.ts_code == ele].tail(5)['boll_lower_diff'].sum()
            z = df[df.ts_code == ele].tail(5)['close_diff'].sum()
            if x >0 and y <0 and z>0:
                hs.append(ele)

        return hs



    def bbands_plot(self, code, ktype):
        """boll线"""

        absolute_path = os.getcwd()
        print('是否存在boll_plot文件:', os.path.exists(os.path.join(absolute_path, 'boll_plot')))
        if os.path.exists(os.path.join(absolute_path, 'boll_plot')):
            shutil.rmtree('boll_plot')
            os.mkdir('boll_plot')
        else:
            os.mkdir('boll_plot')


        for ele in code:
            try:
                print(ele)
                df = self.code_data(ele, ktype)
                df = df.sort_values(by='trade_date', ascending=True)
                upper, middle, lower = talib.BBANDS(df['close'].values, timeperiod=25, nbdevup=2, nbdevdn=2, matype=0)
                df['boll_upper'] = upper
                df['boll_middle'] = middle
                df['boll_lower'] = lower
                df = df[df.trade_date >= self.tm]
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
                plt.savefig('boll_plot/%s.png' % ele)
                plt.close()
            except Exception as e:
                print('error:', ele)

    def code_add_price(self):

        now = datetime.now()
        aDay = timedelta(days=-1)
        now = now + aDay
        tm = now.strftime('%Y-%m-%d')

        df = pd.read_csv('data/%s.csv'%tm, converters = {'code':str})
        print(df)
        codes = df['symbol'].tolist()
        k = []
        for ele in codes:
            try:
                k.append(self.code_data(ele, 'D')['close'].values[0])
                time.sleep(0.2)
            except Exception as e:
                print(ele)
                print('error:', e)
                k.append(-1)
        df['close'] = k
        df.to_csv('data/%s_new.csv'%tm, index=False)

        

def main(start_time, end_time, tm, indu, ktype):


    D = Dog(start_time, end_time, tm)
    # D.bx_add_closePrice('2021-02-19')
    # exit(-1)
    # 为每日添加close数据
    # D.code_add_price()
    # exit(-1)
    # # D.bx_add_closePrice()
    # exit(-1)
    df = D.shenwan_industry()
    #申万一级各个行业北向资金流动图
    # D.bx_in_out('20210315', '20210323')
    # exit(-1)
    # D.bx_in_out_indu('20210201', '20210218')
    # exit(-1)
    #根据最新的行业北向资金变化获得codes
    df_s = pd.read_csv('../data/2021-03-23_new.csv', converters={'code': str})
    k = D.shenwan_industry_code(df_s, indu)

    for ele in k:
        print(ele)
        df = D.data_sar(ele, ktype)
        print(df)
        exit(-1)

    # exit(-1)


    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    industrys = list(set(data['industry'].tolist()))
    # code = data[data.industry == indu].ts_code.tolist()

    code = ['600305.SH', '601615.SH', '300122.SZ', '603866.SH', '300207.SZ', '603786.SH', '603658.SH', '601877.SH',
            '601799.SH', '601598.SH', '600885.SH', '600754.SH', '300724.SZ', '300496.SZ', '300463.SZ', '300327.SZ',
            '300253.SZ', '002557.SZ', '000860.SZ', '000921.SZ', '000400.SZ', '002970.SZ', '002960.SZ', '002920.SZ',
            '002918.SZ', '002891.SZ', '002851.SZ', '002833.SZ', '002831.SZ', '002812.SZ', '002798.SZ', '002791.SZ',
            '002747.SZ', '002727.SZ', '002706.SZ', '002690.SZ', '002625.SZ', '002614.SZ', '002607.SZ', '002539.SZ',
            '002475.SZ', '002463.SZ', '002444.SZ', '002439.SZ', '002430.SZ', '002414.SZ', '002371.SZ', '002352.SZ',
            '002335.SZ', '002241.SZ', '002182.SZ', '002142.SZ', '002129.SZ', '002127.SZ', '002120.SZ', '002110.SZ',
            '002080.SZ', '002050.SZ', '002027.SZ', '000999.SZ', '000923.SZ', '000778.SZ', '000717.SZ', '000710.SZ',
            '000547.SZ', '000426.SZ', '000028.SZ']

    # plot 蜡烛图
    D.getcandlecharts(k, ktype)
    print(ktype)
    # exit(-1)
    # trend 图
    # D.trend(k, ktype)
    #boll plot线
    # D.bbands_plot(k, ktype)
    exit(-1)
    #boll
    # D.bbands(code, ktype)


#['600305.SH','601615.SH', '300122.SH', '603866.SH', '300207.SH', '603786.SH','603658.SH','601877.SH','601799.SH','601598.SH', '600885.SH','600754.SH',
# '300724.SZ','300496.SZ', '300463.SZ', '300327.SZ', '300253.SZ', '002557.SZ', '000860.SZ', '000921.SZ', '000400.SZ', '002970.SZ', '002960.SZ', '002920.SZ',
# '002918.SZ', '002891.SZ','002851.SZ','002833.SZ','002831.SZ', '002812.SZ','002798.SZ', '002791.SZ', '002747.SZ', '002727.SZ','002706.SZ', '002690.SZ',
# '002625.SZ','002614.SZ','002607.SZ','002539.SZ', '002475.SZ', '002463.SZ', '002444.SZ', '002439.SZ', '002430.SZ', '002414.SZ','002371.SZ', '002352.SZ',
# '002335.SZ','002241.SZ', '002182.SZ', '002142.SZ','002129.SZ','002127.SZ','002120.SZ', '002110.SZ', '002080.SZ', '002050.SZ', '002027.SZ','000999.SZ',
# '000923.SZ', '000778.SZ', '000717.SZ', '000710.SZ', '000547.SZ', '000426.SZ', '000028']


 # ['玻璃', '多元金融', '林业', '特种钢', '中成药', '造纸', '橡胶', '超市连锁', '船舶', '批发业', '石油开采', '轻工机械', '水运', '农用机械', '水泥', '运输设备',
# '路桥', '电气设备', '石油贸易', '专用机械', '红黄酒', '小金属', '建筑工程', '化学制药', '互联网', '饲料', '家用电器', '出版业', '港口', '公路', '电器连锁', None,
# '汽车配件', '保险', '机场', '医疗保健', '纺织机械', '环境保护', '航空', '焦炭加工', '房产服务', '广告包装', '化工原料', '园区开发', '文教休闲', '石油加工', '全国地产',
# '铜', '通信设备', '软件服务', '仓储物流', '生物制药', '农药化肥', '影视音像', '摩托车', '证券', '矿物制品', '供气供热', '水力发电', 'IT设备', '纺织', '汽车整车',
# '化工机械', '铅锌', '啤酒', '火力发电', '酒店餐饮', '机床制造', '综合类', '汽车服务', '食品', '医药商业', '新型电力', '日用化工', '服饰', '钢加工', '乳制品',
# '其他建材', '半导体', '软饮料', '商品城', '银行', '普钢', '水务', '家居用品', '电信运营', '种植业', '旅游景点', '其他商业', '空运', '塑料', '农业综合', '元器件',
# '染料涂料', '煤炭开采', '百货', '化纤', '装修装饰', '黄金', '旅游服务', '铝', '铁路', '白酒', '渔业', '区域地产', '电器仪表', '陶瓷', '机械基件', '公共交通',
# '工程机械', '商贸代理']

#一飞冲天：
#w底：
#主升浪：600674.SH

#https://pypi.org/project/akshare/0.2.18/


if __name__ == '__main__':

    #为每日添加收盘价
    # main('20210219', '20210219', '20200901', '新型电力', 'D')


    # k = '000404.sz'
    # # df = D.max_min(k)
    # df = D.code_week_data(k)
    # print(df)
    # exit(-1)D
    # d1 = pro.daily(ts_code=k, start_date="20200601", end_date="20210130")
    main('19900101', '20210329', '20201201', '非银金融', 'D')
    # main()
    # import numpy as np


    # from requests_html import HTMLSession
    # session = HTMLSession()
    # url = 'https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz'
    # r = session.get(url)
    # sel = '#mutualmarket-result > tbody'
    # results = get_text_link_from_sel(sel)
    # print(results)

    # new()

