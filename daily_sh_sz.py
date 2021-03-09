#
import pyhkconnect as hkc
import re
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import shutil
from industry_plot import Dog
from kk import additive_multiplicative_decomposition
from daily_sh_sz import Dog
from real_time_stock import Stock


class Cat(object):

    #https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh&t=sh


    def __init__(self):
        """获取数据的开始时间和结束时间"""

        now = datetime.now()
        aDay = timedelta(days=-1)
        now = now + aDay
        self.tm = now.strftime('%Y-%m-%d')
        # self.D = Dog('10201219', '20210130')
    def sh_data(self):
        dp = hkc.northbound_shareholding_sh()
        return dp

    def sz_data(self):
        dp = hkc.northbound_shareholding_sz()
        return dp

    def get_code(self):
        """sh sz data"""
        #sh data
        df_sh = self.sh_data()
        name = df_sh['name'].tolist()
        codes = []
        symbol = []
        for ele in name:
            a = re.findall('\d+', re.findall('# ?\d+', ele)[0])[0]
            codes.append(a+'.SH')
            symbol.append(a)
        df_sh['symbol'] = codes
        df_sh['code'] = symbol
        df_sh['date'] = [self.tm]*df_sh.shape[0]

        #sz data
        df_sz = self.sz_data()
        name = df_sz['name'].tolist()
        codes = []
        symbol = []
        for ele in name:
            a = re.findall('\d+', re.findall('# ?\d+', ele)[0])[0]
            codes.append(a+'.SZ')
            symbol.append(a)
        df_sz['symbol'] = codes
        df_sz['code'] = symbol
        df_sz['date'] = [self.tm]*df_sz.shape[0]

        df = pd.concat([df_sh, df_sz])

        k = df.symbol.tolist()
        kk = [re.search('[a-zA-Z]+', s).group().lower() + re.search('\d+', s).group() for s in k]
        real_ = Stock(kk)
        df_real = real_.fitPrice()
        df['shareholding_percent'] = df[['shareholding_percent']].apply(lambda x:str(re.sub(r'\%', '', x['shareholding_percent'])), axis=1)
        df['close'] = df_real['close_yesterday'].tolist()
        # pd.concat([df_sh, df_sz])[['date', 'code', 'symbol', 'shareholding', 'shareholding_percent']].to_csv('%s.csv'%self.tm)
        df[["symbol","code","date","shareholding","shareholding_percent", 'close']].to_csv('data/%s_new.csv'%self.tm, index=False)

    def plot_bar(self, df, code_list):

        """shareholding_percent plot """

        absolute_path = os.getcwd()
        print('是否存在shareholding_percent_plot文件:', os.path.exists(os.path.join(absolute_path, 'shareholding_percent_plot')))
        if os.path.exists(os.path.join(absolute_path, 'shareholding_percent_plot')):
            shutil.rmtree('shareholding_percent_plot')
            os.mkdir('shareholding_percent_plot')
        else:
            os.mkdir('shareholding_percent_plot')

        df['date'] = df[['date']].apply(lambda x:datetime.strptime(x['date'], '%Y-%m-%d'), axis=1)
        # df = df[df.date>='20200901']

        # code_list = ['000969.SZ']
        for code in code_list:

            print(code)
            try:
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111)

                dff = df[df.symbol == code]
                dff = dff.sort_values(by='date', ascending=True)
                plt.plot(dff.date.tolist(), dff.shareholding_percent.tolist(), color='blue', linewidth=2.0, linestyle='-')

                plt.title('%s'%code)
                tick_spacing = 1
                plt.xticks(rotation=60)
                plt.xlabel("date")
                plt.ylabel("percent")
                plt.savefig('shareholding_percent_plot/%s.png' % code)
                plt.close()
            except:
                print('error:', code)
                
    def policy_1(self, df):
        """
        策略1：
        """
        df.rename(columns={'shareholding_percent': 'value'}, inplace=True)
        df = df.sort_values(by='date', ascending=True)
        codes = list(set(df.symbol.tolist()))
        for ele in codes:
            dff = df[df.symbol == ele]
            dff = dff.sort_values(by='date', ascending=True)
            m = list(range(dff.shape[0]))
            r = self.D.ipearsonr(m, dff['value'])
            print(ele, r)

    def policy_2(self, dff, fd):
        """
        策略2：
        """
        now = datetime.now()
        aDay = timedelta(days=-8)
        now = now + aDay
        codes = set(fd.symbol.tolist())
        hx_code = []
        for ele in codes:
            k = dff[(dff.symbol == ele)&(dff.date>= str(now))]
            s = k['shareholding_percent'].mean()

            if s >= 5:
                hx_code.append(ele)

        now = datetime.now()
        aDay = timedelta(days=-20)
        now = now + aDay

        out = []
        for ele in hx_code:
            df = dff[(dff.symbol == ele)&(dff.date>= str(now.strftime('%Y-%m-%d')))]
            m = list(range(df.shape[0]))
            r = self.D.ipearsonr(m, df['shareholding_percent'])
            if r[0] > 0.7:
                out.append(ele)

        print(out)

        
    def main(self):
        # df = pd.read_csv('beixiang_his.csv', converters = {'code':str})
        # df['symbol'] = df[['code', 'exchange']].apply(lambda x:str(x['code'])+'.'+str(x['exchange']), axis=1)
        # df[['symbol', 'code', 'date', 'shareholding', 'shareholding_percent']].to_csv('bs_hist.csv', index=False)

        now = datetime.now()
        aDay = timedelta(days=-1)
        now = now + aDay
        tm = now.strftime('%Y-%m-%d')

        df_1 = pd.read_csv('data/bs_hist_merge_new.csv', converters = {'code':str})
        df_2 = pd.read_csv('data/%s_new.csv'%tm, converters = {'code':str})
        df = pd.concat([df_1, df_2])
        df.drop_duplicates(subset=['symbol','date'], keep='last', inplace=True)
        df.to_csv('data/bs_hist_merge_new.csv', index=False)

if __name__ == '__main__':
    C = Cat()
    # df1 = pd.read_csv('bs_hist.csv')
    # df2 = pd.read_csv('2021-02-04.csv', converters = {'symbol':str})
    #
    # l = ['300753.SZ', '002859.SZ', '300207.SZ', '002385.SZ', '002245.SZ', '600261.SH', '601222.SH', '300576.SZ',
    #      '300596.SZ', '300770.SZ', '002074.SZ', '000028.SZ','600875.SH','300136.SZ']
    # ll =["300136.SZ", "603590.SH", "002560.SZ", "300342.SZ", "300865.SZ", "300673.SZ", "300607.SZ","002624.SZ", "002602.SZ", "601222.SZ"]
    # ll = ['300628.SZ', '002714.SZ','603225.SH', '300274.SZ', '300888.SZ', '300012.SZ', '002138.SZ', '603881.SH']
    #充电桩
    l = ['300001.SZ', '600406.SH', '000400.SZ']
    l = ['300253.SZ', '000425.SZ', '002572.SZ', '002126.SZ', '603501.SH', '002372.SZ', '600176.SH', '300308.SZ', '002242.SZ', '600754.SH', '300207.SZ', '000999.SZ', '600529.SH', '300274.SZ', '000423.SZ', '600900.SH', '300015.SZ', '603489.SH', '601138.SH', '601615.SH', '002508.SZ', '300496.SZ', '600305.SH', '002027.SZ', '300059.SZ', '300271.SZ', '000860.SZ', '601877.SH', '002831.SZ', '603939.SH', '603713.SH', '603866.SH', '600201.SH', '002812.SZ', '002008.SZ', '603883.SH', '300450.SZ', '300298.SZ', '002241.SZ', '600066.SH', '300463.SZ', '300285.SZ', '601799.SH', '600885.SH', '000400.SZ', '300383.SZ', '603786.SH', '002439.SZ', '300607.SZ', '300327.SZ', '600801.SH', '601598.SH', '002475.SZ', '300724.SZ', '002371.SZ', '002032.SZ', '601098.SH', '600570.SH', '000625.SZ', '603658.SH', '600298.SH', '600699.SH', '000921.SZ', '000710.SZ', '601318.SH', '002035.SZ', '603288.SH', '002557.SZ']
    #北向plot
    # l =['000710.SZ', '']
    #C.plot_bar(df1, df2.symbol.tolist())
    # C.plot_bar(df1, l)

    #爬取每天北向数据
    C.get_code()
    #每天merge北向数据
    C.main()

    # df = pd.read_csv('2021-02-04.csv', converters = {'symbol':str})
    # dff = pd.read_csv('bs_hist_merge.csv', converters = {'symbol':str})
    # # # C.policy_1(dff)
    # C.policy_2(dff, df)