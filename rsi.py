import tushare as ts
import talib


def diff_(l):
	diff = [0]
	for i in range(1, len(l)):
		diff.append(l[i] - l[i-1])
	
	return diff

def data_d(code):

	df = ts.get_k_data(code, start='2018-01-08', ktype='D')
	df["RSI"] = talib.RSI(df.close, timeperiod=14)
	return df
	
def data_w(code):

	df = ts.get_k_data(code, start='2018-01-08', ktype='W')
	df["RSI"] = talib.RSI(df.close, timeperiod=14)
	return df
	
	
if __name__ == "__main__":

	code = '601952'
	df_d = data_d(code)
	df_d['rsi_diff'] = diff_(df_d.RSI.tolist())
	print('日线')
	print(df_d[['date','open', 'close','RSI', 'rsi_diff']].tail(50))
	
	df_w = data_w(code)
	df_w['rsi_diff'] = diff_(df_w.RSI.tolist())
	print('周线')
	print(df_w[['date','open', 'close','RSI', 'rsi_diff']].tail(10))