
key = '75f7cbe506f185ba42bf382701b21f5e599482881eda3dd639fd8eb2'

import tushare as ts
pro = ts.pro_api(key)
import numpy as np
import scipy.stats
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr

class Dog(object):

    def __init__(self, start, end):
        self.start=start
        self.end=end

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




if __name__ == '__main__':
    D = Dog('20201219', '20210120')
    # data = D.data()
    # data = D.industry_statistics(data)
    k = '603058.sh'
    d1 = pro.daily(ts_code=k, start_date="20201219", end_date="20210120")
    kk = '601155.sh'
    d2 = pro.daily(ts_code=kk, start_date="20201001", end_date="20201109")
    print(d1.shape, d2.shape)
    p = D.KL_divergence(d1.close.tolist(), d2.close.tolist())
    pp = D.JS_divergence(d1.close.tolist(), d2.close.tolist())
    pppp = D.ipearsonr(d1.close.tolist(), d2.close.tolist())
    print(p,pp,pppp[0])