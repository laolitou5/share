import tushare as ts
import talib
from stock import Stock
import time
import pandas as pd
import re
#规则，macd值是正的还是负的无所谓，macd_diff必须是正的，macd_diff_diff最好是正的，周线macd的各个值最后一行没什么参考价值，除非是一周结束

def data_m(code):
	df = ts.get_k_data(code, start='2010-03-10', ktype='M')
	#print(df)
	df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
	#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
	#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

	df.dropna(inplace=True)
	return df
	

def data_w(code):


	try:
		df = ts.get_k_data(code, start='2019-01-08', ktype='w')
		df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
		#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
		#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

		df.dropna(inplace=True)
	except AttributeError:
		print(0)
	return df
	
def data_d(code):

	#买卖原则为：
	#index = DIF-DEA均为正，买入信号参考。
	#index= DIF-DEA均为负，卖出信号参考。

	df = ts.get_k_data(code, start='2000-01-08', ktype='D')
	df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
	df['macd_index'] = df["MACD_macd"] - df["MACD_macdsignal"]
	df['macd_index_diff'] = diff_(df['macd_index'].tolist())
	df['SAR'] = talib.SAR(df.high, df.low, acceleration=0.05, maximum=0.2)
	df['SAR_diff'] = diff_(df['SAR'].tolist())
	df['SAR_close_diff'] = df['SAR'] - df.close
	#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
	#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

	df.dropna(inplace=True)
	return df[['date','close','volume','MACD_macd', 'MACD_macdsignal',  'macd_index_diff',  'macd_index', 'SAR',  'SAR_diff',  'SAR_close_diff']]
	
def diff_(l):
	diff = [0]
	for i in range(1, len(l)):
		diff.append(l[i] - l[i-1])
	
	return diff

	
def macd_diff_1_2(df):
	
	df['macd_diff'] = diff_(df['MACD_macd'].tolist())
	df['macd_diff_diff'] = diff_(df['macd_diff'].tolist())
	return df
	
def alpha_pos(df, col_name, num):
	dff = df.tail(num)
	
	
	if dff[dff[col_name]>0].shape[0] == num:
		return True
	else:
		return False
		
def alpha_neg(df, col_name, num):

	dff = df.tail(num)
	
	if dff[dff[col_name]<0].shape[0] == num:
		return True
	else:
		return False
		
def main1(codes, ss):
	#考虑 月线macd是正的，周线macd是正的，日线macd是正的
	#df = ts.get_industry_classified()
	#df_industry_list = list(set(df.c_name.tolist()))
	#print(df_industry_list)
	#exit(-1)
# 	codes = df[df.c_name == ss].code.tolist()
#
# 	#codes = ['603916', '601952', '600598', '600196', '600369', '300759', '300753', '300529', '603881', '002001', '603367', '002567', '002468', '603669', '300250', '600298', '002271', '600410', '300738', '002597','600380', '601139', '002311', '600313', '600251', '002470', '603018', '603590', '300748','300760', '002959', '002846', '603890', '600720', '300048', '002929', '002706', '600114', '600521', '300702', '002791', '002847', '300511', '002332', '300803', '600325', '300224', '603520', '300122', '300573', '600585']
# 	codes = ['000725','300253','300058','002395', '002481','603688','000810', '002230', '300136','002714','600903','300173','300073','600104','300454','300578','601318',
# '300676','000002','300312','600519','002177','600031','601888','002142','300357','000063','300015','002415','002157','600507','600703','000789','002036','000876','600012',
# '300322','603978','300465','300465','002434','603078','000601','000997','002050','601066','300429','300433','002302','600761','300304','601799','601799','002236','688268',
# '002971','600127','300130','300052','300417','000915','600459','002409', '300457','300346','002792','002385','300256','600143','002007','002127','300416','300750','300347','002414',
# '300695','300482','002456','002371','300468','600305','300236','002458','600171','000158','300223','601555','300805','600988','600547','600350','000610','600276','300115','002475',
# '519674','300653','300572','600406','300385','002030','600063','300580','603786','002838','603559','300820','300001','300033','601236','601236','600909','603093','603982','300643',
# '002023','603160','300348','603986','002299','300661','002124','002384','000955','603601','600418','601696','300817','000700','600498','002422','300026','600789','002975',
# '002180','600161','300762','601990','002223','300607','002233','300793','601816','600585','300573','300122','603520','300224','600325','300803','300511','002847','002791','300702','600521',
# '002706','002929','300048','603890','002846','300760','300748','603018','002470','600251','600313','300738','600410','002271','600298','300250','603669','002567','603367','603881','300529',
# '600211','300246','600114','600598','601952','002959','603309','603916','000710','600380','603109','002185','002311','600720','603590','600196','002332','600741','603068','002317','300753','300759','600369','002597','002001',
# '002468','601139']
	c = []
	for code in codes:
		print('搜索：',code)
		try:
	
			df_m = data_m(code)
			df_m_ = macd_diff_1_2(df_m)
			#print('月线macd')
			#print(df_m_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(10))
			
			df_w = data_w(code)
			df_w_ = macd_diff_1_2(df_w)
			#print('周线macd')
			#print(df_w_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(10))
			
			df_d = data_d(code)
			# print(df_d)
			df_d_ = macd_diff_1_2(df_d)
		except (AttributeError, KeyError) as k:
			print('error', code)
		#print('日线macd')
		#print(df_d_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(50))
		try:
			#print(df_w_.shape)
			print(alpha_pos(df_w_, 'macd_diff',2))
			print(alpha_pos(df_d_, 'macd_diff', 2))
			#print(alpha_pos(df_w_, 'macd_diff', 2))
			
			if alpha_pos(df_w_, 'macd_diff',2) and alpha_neg(df_w_, 'MACD_macd',2):# and alpha_pos(df_d_, 'macd_diff', 2)alpha_neg(df_m_, 'MACD_macd', 2) and alpha_pos(df_m_, 'macd_diff', 2) and 
				print('True：', code)
				c.append(code)
		except NameError:
			print(0)
	print('候选：', c)
	
	
def main2(df, ss):

	codes = df[df.c_name == ss].code.tolist()
	c = []
	print(codes)
	
	for code in codes:
		print('搜索：',code)
		try:
	
			df_m = data_m(code)
			df_m_ = macd_diff_1_2(df_m)
			#print('月线macd')
			#print(df_m_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(10))
			
			df_w = data_w(code)
			df_w_ = macd_diff_1_2(df_w)
			#print('周线macd')
			#print(df_w_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(10))
			
			df_d = data_d(code)
			df_d_ = macd_diff_1_2(df_d)
		except (AttributeError, KeyError) as k:
			print('error', code)
		#print('日线macd')
		#print(df_d_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(50))
		try:
			#print(df_m_.shape)
			#print(alpha_2(df_m_, 2))
			
			if alpha_pos(df_w_, 2) and alpha_1(df_w_, 2) and alpha_neg(df_d_, 2) and alpha_pos(df_w_, 2):
				print('True：', code)
				c.append(code)
		except NameError:
			print(0)
	print('候选：', c)
	

	
codes = ['603916', '601952', '600598', '600196', '600369', '300759', '300753', '300529', '603881', '002001', '603367', '002567', '002468', '603669', '300250', '600298', '002271', '600410', '300738', '002597','600380', '601139', '002311', '600313', '600251', '002470', '603018', '603590', '300748','300760', '002959', '002846', '603890', '600720', '300048', '002929', '002706', '600114', '600521', '300702', '002791', '002847', '300511', '002332', '300803', '600325', '300224', '603520', '300122', '300573', '600585']
	
def sar(code):

	codes = ['000725','300253','300058','002395', '002481','603688','000810', '002230', '300136','002714','600903','300173','300073','600104','300454','300578','601318',
'300676','000002','300312','600519','002177','600031','601888','002142','300357','000063','300015','002415','002157','600507','600703','000789','002036','000876','600012',
'300322','603978','300465','300465','002434','603078','000601','000997','002050','601066','300429','300433','002302','600761','300304','601799','601799','002236','688268',
'002971','600127','300130','300052','300417','000915','600459','002409', '300457','300346','002792','002385','300256','600143','002007','002127','300416','300750','300347','002414',
'300695','300482','002456','002371','300468','600305','300236','002458','600171','000158','300223','601555','300805','600988','600547','600350','000610','600276','300115','002475',
'519674','300653','300572','600406','300385','002030','600063','300580','603786','002838','603559','300820','300001','300033','601236','601236','600909','603093','603982','300643',
'002023','603160','300348','603986','002299','300661','002124','002384','000955','603601','600418','601696','300817','000700','600498','002422','300026','600789','002975',
'002180','600161','300762','601990','002223','300607','002233','300793','601816','600585','300573','300122','603520','300224','600325','300803','300511','002847','002791','300702','600521',
'002706','002929','300048','603890','002846','300760','300748','603018','002470','600251','600313','300738','600410','002271','600298','300250','603669','002567','603367','603881','300529',
'600211','300246','600114','600598','601952','002959','603309','603916','000710','600380','603109','002185','002311','600720','603590','600196','002332','600741','603068','002317','300753','300759','600369','002597','002001',
'002468','601139']	

	for code in codes:
	
		df = ts.get_k_data(code, start='2020-01-08', ktype='D')
		#print(df)
		df['SAR'] = talib.SAR(df.high, df.low, acceleration=0.05, maximum=0.2)
		df['SAR_close_diff'] = df['SAR'] - df.close
		
		
		#df[df.SAR_close_diff < -3])
		print(code)
		print(df.tail(5))
	#df.to_csv('600114.csv', index=False)

codes = ['000725','300253','300058','002395', '002481','603688','000810', '002230', '300136','002714','600903','300173','300073','600104','300454','300578','601318',
'300676','000002','300312','600519','002177','600031','601888','002142','300357','000063','300015','002415','002157','600507','600703','000789','002036','000876','600012',
'300322','603978','300465','300465','002434','603078','000601','000997','002050','601066','300429','300433','002302','600761','300304','601799','601799','002236','688268',
'002971','600127','300130','300052','300417','000915','600459','002409', '300457','300346','002792','002385','300256','600143','002007','002127','300416','300750','300347','002414',
'300695','300482','002456','002371','300468','600305','300236','002458','600171','000158','300223','601555','300805','600988','600547','600350','000610','600276','300115','002475',
'519674','300653','300572','600406','300385','002030','600063','300580','603786','002838','603559','300820','300001','300033','601236','601236','600909','603093','603982','300643',
'002023','603160','300348','603986','002299','300661','002124','002384','000955','603601','600418','601696','300817','000700','600498','002422','300026','600789','002975',
'002180','600161','300762','601990','002223','300607','002233','300793','601816','600585','300573','300122','603520','300224','600325','300803','300511','002847','002791','300702','600521',
'002706','002929','300048','603890','002846','300760','300748','603018','002470','600251','600313','300738','600410','002271','600298','300250','603669','002567','603367','603881','300529',
'600211','300246','600114','600598','601952','002959','603309','603916','000710','600380','603109','002185','002311','600720','603590','600196','002332','600741','603068','002317','300753','300759','600369','002597','002001',
'002468','601139']


def indu_code():
	import baostock as bs

	# 登陆系统
	lg = bs.login(user_id="anonymous", password="123456")
	# 显示登陆返回信息
	print('login respond error_code:' + lg.error_code)
	print('login respond  error_msg:' + lg.error_msg)

	# 获取行业分类数据
	rs = bs.query_stock_industry()
	# rs = bs.query_stock_basic(code_name="中信建投")
	print('rs', rs)
	print('query_stock_industry error_code:' + rs.error_code)
	print('query_stock_industry respond  error_msg:' + rs.error_msg)

	# 打印结果集
	industry_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		industry_list.append(rs.get_row_data())
	result = pd.DataFrame(industry_list, columns=rs.fields)
	# print(result[result.code_name == '通信'])
	# print(result.columns)
	print(set(result['industry'].tolist()))
	codes = result[result.industry == '传媒'].code.tolist()
	codes_ = []
	for ele in codes:
		codes_.append(re.findall('\d+', ele)[0])
	# print(codes_)

	# import tushare as ts
	# df = ts.get_industry_classified()
	# print(df[df.code == '300760'])
	# df_industry_list = list(set(df.c_name.tolist()))
	# print(df_industry_list)
	# codes_ = df[df.c_name == '生物制药'].code.tolist()
	# print(df[df.c_name == '水泥行业'])

	return codes_

if __name__ == "__main__":

	#codes = ts.get_stock_basics().index.values.tolist()
	#codes = ['600145']
	# pro = ts.pro_api('0db19111fce68418f078a49fafe2465e53579a965d13d7f0e723ad3f')
	# data_all = pro.query('stock_basic', exchange='', list_status='L',
	# 					 fields='ts_code,symbol,name,area,industry,list_date')
	#
	# #df = ts.get_industry_classified()
	# print(data_all)
	#df = ts.get_k_data('300738', start='2018-01-08', ktype='D')
	#print(df[df.code=='002271'])
	#print(df)
	#exit(-1)
	
	#df_industry_list = list(set(df.c_name.tolist()))
	#print(df_industry_list)
	#main1(df, '电子信息')
	#sar('002597')
	#code = '002468'
	#df_d = data_d(code)
	#print(df_d.tail(60))

	codes = indu_code()
	main1(codes, '')

	exit(-1)

	#实时抓取数据
	s = Stock('sz002597')
	print(s)
	f = open('sz002597_521.txt', 'w')
	while(True):
		res = s.fitPrice(' ')
		print(res)
		f.write(str(res))
		f.write('\n')
		time.sleep(30)
	f.close()

