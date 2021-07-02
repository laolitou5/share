# coding=utf-8

import talib
import matplotlib.pyplot as plt

import baostock as bs
import pandas as pd 
import re
from meigu import cal_week_line
import time

key = '75f7cbe506f185ba42bf382701b21f5e599482881eda3dd639fd8eb2'
import tushare as ts
pro = ts.pro_api(key)

def indu_code():

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

	print(set(result['industry'].tolist()))
	codes = result[result.industry=='汽车'].code.tolist()
	print(len(codes))
	codes_ = []
	for ele in codes:
		codes_.append(re.findall('\d+', ele)[0])
	
	return codes_
	
def dt(code_list, end_time, ktype):
	s = 0
	l = []
	for ele in code_list:
		try:
			time.sleep(1)
			if ktype == 'D':
				df = pro.daily(ts_code=ele, start_date='19900101', end_date=end_time)
			else:
				df = pro.weekly(ts_code=ele, start_date='19900101', end_date=end_time, fields='ts_code,trade_date,open,high,low,close,vol,amount')
				# df = pro.daily(ts_code=ele, start_date='19900101', end_date=end_time)
				# df.rename(columns={'trade_date':'date', 'vol':'volume'}, inplace=True)
				# df = cal_week_line(df, period_type = ktype)
			df.sort_index(ascending=False, inplace=True)
			closed = df.close.values
			ma5 = talib.SMA(closed,timeperiod=5)[-1]
			ma10 = talib.SMA(closed,timeperiod=10)[-1]
			ma20 = talib.SMA(closed,timeperiod=20)[-1]
			ma30 = talib.SMA(closed,timeperiod=30)[-1]
			ma60 = talib.SMA(closed,timeperiod=60)[-1]
			# print(ma5, ma10, ma20, ma30, ma60)
			if ma5 / ma10 >  ma10 / ma20 and ma10 / ma20 > ma20 / ma30 and ma5 / ma10 >1 and ma20 / ma30 < 1:
				l.append(ele)
		except Exception as e:
			print(e)
	return l
			
if __name__ == '__main__':

	# codes = indu_code()
	codes = ['600737.sh']
	c = dt(codes, '20210625', 'W')
	print(c)
	
		