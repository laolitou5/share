
import tushare as ts
import talib
import matplotlib.pyplot as plt

import baostock as bs
import pandas as pd 
import re

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
	#print(result)
	#print(result[result.code_name == '三维通信'])
	#print(result.columns)
	print(set(result['industry'].tolist()))
	codes = result[result.industry=='轻工制造'].code.tolist()
	codes_ = []
	for ele in codes:
		codes_.append(re.findall('\d+', ele)[0])
	#print(codes_)
		
	#df = ts.get_industry_classified()
	#print(df)
	#print(df[df.code == '300760'])
	#df_industry_list = list(set(df.c_name.tolist()))
	#print(df_industry_list)
	#exit(-1)
	#codes_ = df[df.c_name == '生物制药'].code.tolist()
	#print(df[df.c_name == '水泥行业'])
	
	return codes_


def plot(code_list):

	#print(code_list)
	#code_list = ['002581']
	for ele in code_list:
		print(ele)
		try:
			df=ts.get_k_data(ele,start='1990-06-12',end='2020-06-03')
			#提取收盘价
			closed=df['close'].values
			#upper,middle,lower=talib.BBANDS(closed,matype=talib.MA_Type.T3)
			upper,middle,lower = talib.BBANDS(closed,timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
			
			#print upper,middle,lower
			plt.plot(closed[-180:], "k", label = 'closed')
			plt.plot(upper[-180:], label = 'upper')
			plt.plot(middle[-180:], label='middle')
			plt.plot(lower[-180:], label='lower')
			plt.legend()
			plt.grid()
			plt.savefig('boll_plot/%s.png'%ele)
			plt.close()
			
			diff1=upper-middle
			diff2=middle-lower
		except Exception as e:
			print(e)
		
if __name__ == '__main__':
	codes = indu_code()
	#print(codes)
	plot(codes)
#print diff1
#print diff2