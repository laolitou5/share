
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
#['玻璃', '多元金融', '林业', '特种钢', '中成药', '造纸', '橡胶', '超市连锁', '船舶', '批发业', '石油开采', '轻工机械', '水运', '农用机械', '水泥', '运输设备', '路桥', '电气设备', '石油贸易', '专用机械', '红黄酒', '小金属', '建筑工程', '化学制药', '互联网', '饲料', '家用电器', '出版业', '港口', '公路', '电器连锁', None, '汽车配件', '保险', '机场', '医疗保健', '纺织机械', '环境保护', '航空', '焦炭加工', '房产服务', '广告包装', '化工原料', '园区开发', '文教休闲', '石油加工', '全国地产', '铜', '通信设备', '软件服务', '仓储物流', '生物制药', '农药化肥', '影视音像', '摩托车', '证券', '矿物制品', '供气供热', '水力发电', 'IT设备', '纺织', '汽车整车', '化工机械', '铅锌', '啤酒', '火力发电', '酒店餐饮', '机床制造', '综合类', '汽车服务', '食品', '医药商业', '新型电力', '日用化工', '服饰', '钢加工', '乳制品', '其他建材', '半导体', '软饮料', '商品城', '银行', '普钢', '水务', '家居用品', '电信运营', '种植业', '旅游景点', '其他商业', '空运', '塑料', '农业综合', '元器件', '染料涂料', '煤炭开采', '百货', '化纤', '装修装饰', '黄金', '旅游服务', '铝', '铁路', '白酒', '渔业', '区域地产', '电器仪表', '陶瓷', '机械基件', '公共交通', '工程机械', '商贸代理']
#
def main():
    from share import getcandlecharts
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    industrys = list(set(data['industry'].tolist()))
    code = data[data.industry == '专用机械'].symbol.tolist()
    getcandlecharts(code)





if __name__ == '__main__':
    # D = Dog('20201219', '20210120')
    # k = '603058.sh'
    # d1 = pro.daily(ts_code=k, start_date="20200601", end_date="20210130")
    main()
    # kk = '601155.sh'
    # d2 = pro.daily(ts_code=kk, start_date="20201001", end_date="20201109")
    # #
    # p = D.KL_divergence(d1.close.tolist(), d2.close.tolist())
    # pp = D.JS_divergence(d1.close.tolist(), d2.close.tolist())
    # pppp = D.ipearsonr(d1.close.tolist(), d2.close.tolist())
    # print(p,pp,pppp[0])