#encoding='utf8'
#当股价上升而OBV线下降，表示买盘无力，股价可能会回跌。
#股价下降时而OBV线上升，表示买盘旺盛，逢低接手强股，股价可能会止跌回升。

import tushare as ts
import talib

def diff_(l):
	diff = [0]
	for i in range(1, len(l)):
		diff.append(l[i] - l[i-1])
	
	return diff


def data_d(code):

	df = ts.get_k_data(code, start='2018-01-08', ktype='D')
	df["obv"] = talib.OBV(df.close,df.volume)
	
	return df


def data_w(code):

	df = ts.get_k_data(code, start='2020-01-08', ktype='W')
	df["obv"] = talib.OBV(df.close,df.volume)
	
	return df	
if __name__ == '__main__':

	code = '601952'

	df_w = data_w(code)
	df_w['obv_diff'] = diff_(df_w.obv.tolist())
	print('周线')
	print(df_w[['date','open', 'close','obv', 'obv_diff']].tail(10))
	
		
	df_d = data_d(code)
	df_d['obv_diff'] = diff_(df_d.obv.tolist())
	print('日线')
	print(df_d[['date','open', 'close','obv', 'obv_diff']].tail(50))