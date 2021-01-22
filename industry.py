# from pytdx.hq import TdxHq_API
# # from pytdx.exhq import TdxExHq_API
# api = TdxHq_API()
#
# with api.connect('119.147.212.81', 7709):
#     data = api.get_security_bars(9, 0, '000001', 0, 10)
#     data = api.to_df(api.get_security_bars(9, 0, '000001', 0, 10))
#     data = api.get_index_bars(5, 1, '000001', 1, 2)
#     data = api.get_security_quotes([(0, '000001')])
#     data = api.get_company_info_category(TDXParams.MARKET_SZ, '000001')
#     data = api.get_instrument_info(0, 100)
#     print(data)

key = '75f7cbe506f185ba42bf382701b21f5e599482881eda3dd639fd8eb2'

import tushare as ts
pro = ts.pro_api(key)
import numpy as np
import scipy.stats
import pandas as pd

class Dog(object):

    def __init__(self, start, end):
        self.start=start
        self.end=end

    def KL_divergence(self, p,q):
        """通过kl散度判断p和q的分布的相似度/距离"""
        return scipy.stats.entropy(p, q)

    def JS_divergence(self, p, q):
        """通过js散度判断p和q的分布的相似度/距离"""
        M = (p + q) / 2
        return 0.5 * scipy.stats.entropy(p, M) + 0.5 * scipy.stats.entropy(q, M)

    def data(self):
        """全部股票数据"""
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        return data

    def code_day_data(self, code):
        """获取确定code下指定时间段的日线数据"""
        df = pro.daily(ts_code=code, start_date=self.start, end_date=self.end)
        return df

    def industry_statistics(self, df):
        """按照行业 vol 统计信息"""
        industry_list = list(set(df['industry'].tolist()))
        # df_industry_statistics = pd.DataFrame()
        # code_list = []
        # vol_list = []
        # industry_ = []
        for ele in industry_list:
            df_industry_statistics = pd.DataFrame()
            code_list = []
            vol_list = []
            industry_ = []
            print(ele)
            codes = df[df.industry == ele]['ts_code'].tolist()
            for k in codes:
                code_list.append(k)
                vol_list.append(pro.daily(ts_code=k, start_date=self.start, end_date=self.end)['vol'].sum())
                industry_.append(ele)
            df_industry_statistics['code'] = code_list
            df_industry_statistics['vol'] = vol_list
            df_industry_statistics['industry'] = industry_
            # df_industry_statistics.to_csv('%s_vol.csv'%ele)
            print(df_industry_statistics)
            print(df_industry_statistics['vol'].sum())
            exit(-1)
        return df_industry_statistics.groupby('industry').sum()




if __name__ == '__main__':
    D = Dog('20210119', '20210120')
    data = D.data()
    # code = '000001.SZ'
    # df = code_day_data(code, start_time, end_time)
    data = D.industry_statistics(data)