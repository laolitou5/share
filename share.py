
import tushare as ts
import pandas as pd
import re
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_finance as mpf
import shutil
# import datetime
from datetime import datetime
import matplotlib.dates as dt
# df_area = ts.get_area_classified()
# print(df_area[df_area.area == '深圳'])
# print(df_area[df_area.name == '深圳燃气'])
#
# df_concept = ts.get_concept_classified()
# print(df_concept[df_concept.code == '601139'])
#
# df_industry = ts.get_industry_classified()
# print(df_industry[df_industry.code == '601139'])
#
# # print(ts.get_hist_data('hs300'))
# print('风险警示板分类:\n', ts.get_st_classified())

def indu_code():
	import baostock as bs

	# 登陆系统
	lg = bs.login(user_id="anonymous", password="123456")
	# 显示登陆返回信息
	print('login respond error_code:'+lg.error_code)
	print('login respond  error_msg:'+lg.error_msg)

	# 获取行业分类数据
	rs = bs.query_stock_industry()
	#rs = bs.query_stock_basic(code_name="中信建投")
	print('rs', rs)
	print('query_stock_industry error_code:'+rs.error_code)
	print('query_stock_industry respond  error_msg:'+rs.error_msg)

	# 打印结果集
	industry_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		industry_list.append(rs.get_row_data())
	result = pd.DataFrame(industry_list, columns=rs.fields)
	#print(result[result.code_name == '通信'])
	#print(result.columns)
	print(set(result['industry'].tolist()))

	codes = result[result.industry=='电气设备'].code.tolist()

    #
	codes = result.code.tolist()
	codes_ = []
	for ele in codes:
		codes_.append(re.findall('\d+', ele)[0])

	return codes_
	


def raising_limit(df):

    """
    按照行业，统计涨停次数大于10的股票代码
    :param df:
    :return:
    """
    code_times_dict = {}
    for ele in df.index.values:
        try:
            dt = ts.get_hist_data(ele, start='2019-01-01', end='2019-09-04')
            times_of_over_10 = dt[dt.p_change >= 9.9].shape[0]
            if times_of_over_10 > 10:
                code_times_dict[ele] = times_of_over_10

        except AttributeError:
            print(ele)
    print(code_times_dict)
    return code_times_dict


def youji_share_concept(df):

    """
    优绩share，
    :param df:
    :return:
    """

    code_up_dict = {}
    dt = ts.get_cashflow_data(2019, 2)
    c_name = list(set(df.c_name.tolist()))
    # print(len(c_name))
    for ele in c_name:
        df_filter = df[df.c_name == ele]
        for ele_code in df_filter.code:
            print(dt[dt.code == ele_code])


def youji_share_industry(dff):

    # dt = ts.get_cashflow_data(2019, 2)
    # td = ts.get_profit_data(2019, 2)
    df = pd.DataFrame()
    df_report = ts.get_report_data(2019, 2)
    df_profit = ts.get_profit_data(2019, 2)
    # df_operation = ts.get_operation_data(2019, 2)
    df_growth = ts.get_growth_data(2019, 2)
    # df_debtpaying = ts.get_debtpaying_data(2019, 2)
    df_cashflow = ts.get_cashflow_data(2019, 2)


    # c_name = list(set(df.c_name.tolist()))
    # print(c_name)
    # exit(-1)
    roe_ = []
    eps_yoy_ = []
    net_profit_ratio_ = []
    gross_profit_rate_ = []
    nprg_ = []
    mbrg_ = []
    cf_sales_ = []
    code_ = []
    # ttt = []
    for ele in ['供水供气']:
        df_filter = dff[dff.c_name == ele]
        for ele_code in df_filter.code:
            try:
                code_.append(ele_code)
                print(re.sub(r'\[|\]', '', str(df_report[df_report.code == ele_code].roe.values)))
                roe_.append(re.sub(r'\[|\]', '', str(df_report[df_report.code == ele_code].roe.values)))
                eps_yoy_.append(re.sub(r'\[|\]', '',str(df_report[df_report.code == ele_code].eps_yoy.values)))
                net_profit_ratio_.append(re.sub(r'\[|\]', '',str(df_profit[df_profit.code == ele_code].net_profit_ratio.values)))
                gross_profit_rate_.append(re.sub(r'\[|\]', '',str(df_profit[df_profit.code == ele_code].gross_profit_rate.values)))
                mbrg_.append(re.sub(r'\[|\]', '',str(df_growth[df_growth.code == ele_code].mbrg.values)))
                nprg_.append(re.sub(r'\[|\]', '',str(df_growth[df_growth.code == ele_code].nprg.values)))
                cf_sales_.append(re.sub(r'\[|\]', '',str(df_cashflow[df_cashflow.code == ele_code].cf_sales.values)))
            except IndexError:
                print(ele_code)

    # df['净资产收益率'] = roe_
    # df['每股收益同比'] = eps_yoy_
    df['code'] = code_
    df['净利率'] = net_profit_ratio_
    df['毛利率'] = gross_profit_rate_
    df['主营业务收入增长率'] = mbrg_
    df['净利润增长率'] = nprg_
    df['经营现金净流量对销售收入比率'] = cf_sales_

    df.to_csv('shuiqi.csv', encoding='gb18030', index=False)


    return 0

def cashflow_(code):

    df = ts.get_today_all()
    pe = df.per.values
    name = df.name.vaues
    pb = df.pb.values

    return pe, name, pb


def code_(code):

    df = ts.get_today_all()
    
    #总市值过滤
    df = df[df.mktcap > 1e+6]  # 100亿

    pro = ts.pro_api('0db19111fce68418f078a49fafe2465e53579a965d13d7f0e723ad3f')
    data_all = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    industry_code = data_all[data_all.symbol == code].industry.tolist()
    print(industry_code)
    industry_code_list = data_all[data_all.industry.isin(industry_code)].symbol.tolist()

    getcandlecharts(industry_code_list)

    dff = df[df.code.isin(industry_code_list)]
    print(dff)

    dff.to_csv('%s.csv'%code, encoding='gb18030', index=False)


    return 0


def index_(code):

    pro = ts.pro_api('0db19111fce68418f078a49fafe2465e53579a965d13d7f0e723ad3f')
    data_all = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    industry_code = data_all[data_all.symbol == code].industry.tolist()
    industry_code_list = data_all[data_all.industry.isin(industry_code)].symbol.tolist()
    num = len(industry_code_list)

    pf = pd.DataFrame()
    name = []
    data = []

    name.append('name_')
    data.append(data_all[data_all.symbol == code].name.tolist()[0])
    # df_concept = ts.get_concept_classified()
    # concept = df_concept[df_concept.code == code].c_name.values.tolist()
    # print(concept)
    # concept = ['基因概念']
    # industry = '医药生物'
    # name_code = df_concept[df_concept.code == code].name.values[0]
    name.append('name_industry')
    data.append(industry_code[0])

    name.append('code')
    data.append(code)


    df = pd.read_csv('0910.csv', encoding='gb18030', index_col=False)

    #pe及其位置
    # code_list = df_concept[df_concept.c_name.isin(concept)].code.tolist()
    pe_list_sort = sorted(df[df.code.isin(industry_code_list)].per.tolist(), reverse=True)
    pe = df[df.code.isin([code])].per.tolist()[0]
    pe_pos = pe_list_sort.index(pe)

    name.append('pe')
    data.append(pe)
    name.append('pe_industry_rank')
    data.append(str(pe_pos)+"//%s"%num)

    #pb及其位置
    # code_list = df_concept[df_concept.c_name.isin(concept)].code.tolist()
    pb_list_sort = sorted(df[df.code.isin(industry_code_list)].pb.tolist(), reverse=True)
    pb = df[df.code.isin([code])].pb.tolist()[0]
    pb_pos = pb_list_sort.index(pb)
    name.append('pb')
    data.append(pb)
    name.append('pb_industry_rank')
    data.append(str(pb_pos) +"//%s"%num)

    #毛利率
    df_profit_1 = ts.get_profit_data(2019, 1)
    df_profit_2 = ts.get_profit_data(2019, 2)

    g_1 = re.sub(r'\[|\]', '', str(df_profit_1[df_profit_1.code == code].gross_profit_rate.tolist()))
    g_2 = re.sub(r'\[|\]', '', str(df_profit_2[df_profit_2.code == code].gross_profit_rate.tolist()))

    g_1_list_sort = sorted(df_profit_1[df_profit_1.code.isin(industry_code_list)].gross_profit_rate.tolist(), reverse=True)
    g_2_list_sort = sorted(df_profit_2[df_profit_2.code.isin(industry_code_list)].gross_profit_rate.tolist(), reverse=True)

    g_1_pos = g_1_list_sort.index(float(g_1))
    g_2_pos = g_2_list_sort.index(float(g_2))

    name.append('2019年1季度_毛利率')
    data.append(g_1)
    name.append('2019年1季度_毛利率_industry_rank')
    data.append(str(g_1_pos)+"//%s"%num)
    name.append('2019年2季度_毛利率')
    data.append(g_2)
    name.append('2019年2季度_毛利率_industry_rank')
    data.append(str(g_2_pos)+"//%s"%num)

    #现金流
    df_cashflow_11 = ts.get_cashflow_data(2018, 1)
    df_cashflow_12 = ts.get_cashflow_data(2018, 2)
    df_cashflow_13 = ts.get_cashflow_data(2018, 3)
    df_cashflow_14 = ts.get_cashflow_data(2018, 4)
    df_cashflow_1 = ts.get_cashflow_data(2019, 1)
    df_cashflow_2 = ts.get_cashflow_data(2019, 2)
    df_cf_nm_11 = re.sub(r'\[|\]', '', str(df_cashflow_11[df_cashflow_11.code == code].cf_nm.tolist()))
    df_cf_nm_12 = re.sub(r'\[|\]', '', str(df_cashflow_12[df_cashflow_12.code == code].cf_nm.tolist()))
    df_cf_nm_13 = re.sub(r'\[|\]', '', str(df_cashflow_13[df_cashflow_13.code == code].cf_nm.tolist()))
    df_cf_nm_14 = re.sub(r'\[|\]', '', str(df_cashflow_14[df_cashflow_14.code == code].cf_nm.tolist()))
    df_cf_nm_1 = re.sub(r'\[|\]', '', str(df_cashflow_1[df_cashflow_1.code == code].cf_nm.tolist()))
    df_cf_nm_2 = re.sub(r'\[|\]', '', str(df_cashflow_2[df_cashflow_2.code == code].cf_nm.tolist()))

    name.append('2018年1季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_11)
    name.append('2018年2季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_12)
    name.append('2018年3季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_13)
    name.append('2018年4季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_14)
    name.append('2019年1季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_1)
    name.append('2019年2季度_经营现金净流量与净利润的比率')
    data.append(df_cf_nm_2)

    #增长
    df_growth_11 = ts.get_growth_data(2018, 1)
    df_growth_12 = ts.get_growth_data(2018, 2)
    df_growth_13 = ts.get_growth_data(2018, 3)
    df_growth_14 = ts.get_growth_data(2018, 4)
    df_growth_21 = ts.get_growth_data(2019, 1)
    df_growth_22 = ts.get_growth_data(2019, 2)

    grow11 = re.sub(r'\[|\]', '', str(df_growth_11[df_growth_11.code.isin([code])].mbrg.values))
    grow12 = re.sub(r'\[|\]', '', str(df_growth_12[df_growth_12.code.isin([code])].mbrg.values))
    grow13 = re.sub(r'\[|\]', '', str(df_growth_13[df_growth_13.code.isin([code])].mbrg.values))
    grow14 = re.sub(r'\[|\]', '', str(df_growth_14[df_growth_14.code.isin([code])].mbrg.values))
    grow21 = re.sub(r'\[|\]', '', str(df_growth_21[df_growth_21.code.isin([code])].mbrg.values))
    grow22 = re.sub(r'\[|\]', '', str(df_growth_22[df_growth_22.code.isin([code])].mbrg.values))

    name.append('2018年1季度_主营业务收入增长率 ')
    data.append(grow11)
    name.append('2018年2季度_主营业务收入增长率 ')
    data.append(grow12)
    name.append('2018年3季度_主营业务收入增长率 ')
    data.append(grow13)
    name.append('2018年4季度_主营业务收入增长率 ')
    data.append(grow14)
    name.append('2019年1季度_主营业务收入增长率 ')
    data.append(grow21)
    name.append('2019年2季度_主营业务收入增长率 ')
    data.append(grow22)

    pf['name'] = name
    pf['data'] = data
    pf.to_csv('%s.csv'%code, encoding='gb18030', index=False)


def getcandlecharts(codes):
    # chinese = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
    index = 1
    absolute_path = os.getcwd()
    print(os.path.exists(os.path.join(absolute_path, 'test')))
    if os.path.exists(os.path.join(absolute_path, 'test')):
        shutil.rmtree('test')
        os.mkdir('test')
    else:
        os.mkdir('test')
    print(codes, len(codes))

    try:
        for code in codes:
            #print(code)
            #plt.figure(figsize=(10, 8), facecolor='w')
            shyh = ts.get_k_data(code, start='2019-01-01', ktype='W')
            # print(shyh)
			
            if len(shyh) >0 :
                #print(shyh.shape)
                plt.figure(figsize=(10, 8), facecolor='w')
                mat_shyh = shyh.values
                num_time = dt.date2num([datetime.strptime(ele, '%Y-%m-%d') for ele in mat_shyh[:, 0]])
                mat_shyh[:, 0] = num_time
                ax = plt.subplot(1, 1, index)
                mpf.candlestick_ochl(ax, mat_shyh,width=0.6, colorup="r", colordown="g", alpha=1.0)
                plt.grid(True)
                plt.xticks(rotation=30)
                plt.title('%s'%code)
                plt.xlabel("Date")
                plt.ylabel("Price")
                ax.xaxis_date()
                plt.savefig('test/%s.png'%code)
                plt.close()
    except TypeError:
        print (code)

def share_fre():
    path = r'C:\Users\lizhaoxing\Desktop\SentimentAnalysis\lstm\share.csv'
    df_1 = pd.read_csv(path, encoding='gb18030')
    df_1_filter = df_1[['code', 'dividCashPsBeforeTax', 'dividPayDate']].drop_duplicates(['code'], keep='first', inplace=False).dropna(how = 'any',axis = 0)
    df_1_code = df_1_filter.code.tolist()
    code_ = []
    # print(df_1_filter)
    # ts.get_hist_data(ele, start='2019-01-01', end='2019-09-04')
    time__ = []
    code__ = []
    pp = []
    vv = []
    r = []
    for ele in df_1_code:
        try:
            code_ = re.search(r'\d+', ele).group(0)
            time_ = df_1_filter[df_1_filter.code == ele]['dividPayDate'].tolist()[0]
            p = df_1_filter[df_1_filter.code == ele]['dividCashPsBeforeTax'].tolist()[0]
            v = ts.get_hist_data(code_, start=time_, end=time_)['close'].values[0]
            x = p/v

            code__.append(code_)
            time__.append(time_)
            pp.append(p)
            vv.append(v)
            r.append(x)
        except (IndexError, TypeError):
            print(ele, time_)
    fd = pd.DataFrame()
    fd['code'] = code__
    fd['time'] = time__
    fd['price'] = vv
    fd['分红/10'] = pp
    fd['分红/10/股票价格'] = r
    fd.to_csv('out.csv', encoding='gbk', index=False)


if __name__ == '__main__':

    # df = ts.get_stock_basics()
    # print(df)
    # raising_limit(df)

    # df_concept = ts.get_concept_classified()
    # # print(df_concept)
    # youji_share_concept(df_concept)



    # df_area = ts.get_area_classified()
    # df_concept = ts.get_concept_classified()
    # print(df_concept[df_concept.code == '600291'])
    # df_industry = ts.get_industry_classified()
    # # print(df_industry[df_industry.code == '601139'].c_name)
    # youji_share_industry(df_industry)

    # code_1 = '601099'
    # df_industry = ts.get_industry_classified()
    # industry = df_industry[df_industry.code == code_1].c_name.values[0]
    # print(industry)
    # code_list = df_industry[df_industry.c_name == industry].code.tolist()
    # # print(code_list)
    #

    # code_()
    #code = '600738'
    # index_(code)

    #获得code行业的k线
    #code_(code)

    #通过分红发现价值
    #share_fre()

	codes_list = indu_code()
	getcandlecharts(codes_list)

    # pro = ts.pro_api('0db19111fce68418f078a49fafe2465e53579a965d13d7f0e723ad3f')
    # data_all = pro.query('stock_basic', exchange='', list_status='L',
    #                      fields='ts_code,symbol,name,area,industry,list_date')
    # print(data_all[data_all.industry == '酒店餐饮'])
    # lvyou_code_list = data_all[data_all.industry == '酒店餐饮'].symbol.tolist()
    # print(set(data_all.industry.tolist()))
    # for ele in lvyou_code_list:
    #     index_(ele)










