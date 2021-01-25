# -*- coding:utf-8 -*-
import tushare as ts
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.api import tsa
#规则，macd值是正的还是负的无所谓，macd_diff必须是正的，macd_diff_diff最好是正的，周线macd的各个值最后一行没什么参考价值，除非是一周结束

def data_d(code):
	df = ts.get_k_data(code, start='2018-08-08', end='2020-03-20', ktype='D')
	#print(df)
	#df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
	#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
	#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

	#df.dropna(inplace=True)
	return df
	

def data_w(code):

	try:
		df = ts.get_k_data(code, start='2018-01-08', ktype='w')
		df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
		#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
		#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

		df.dropna(inplace=True)
	except AttributeError:
		print(0)
	return df
	
def data_dd(code):

	df = ts.get_k_data(code, start='2018-01-08', ktype='D')
	df["MACD_macd"],df["MACD_macdsignal"],df["MACD_macdhist"] = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
	#df["MACDEXT_macd"],df["MACDEXT_macdsignal"],df["MACDEXT_macdhist"] = talib.MACDEXT(df.close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
	#df["MACDFIX_macd"],df["MACDFIX_macdsignal"],df["MACDFIX_macdhist"] = talib.MACDFIX(df.close, signalperiod=9)

	df.dropna(inplace=True)
	return df
	
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
		
def main1(df, ss):
	#考虑 月线macd是正的，周线macd是正的，日线macd是正的
	#df = ts.get_industry_classified()
	#df_industry_list = list(set(df.c_name.tolist()))
	#print(df_industry_list)
	#exit(-1)
	codes = df[df.c_name == ss].code.tolist()
	print(codes)
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
			df_d_ = macd_diff_1_2(df_d)
		except (AttributeError, KeyError) as k:
			print('error', code)
		#print('日线macd')
		#print(df_d_[['date', 'close', 'MACD_macd','macd_diff', 'macd_diff_diff']].tail(50))
		try:
			print(df_w_.shape)
			print(alpha_pos(df_m_, 'MACD_macd', 2))
			print(alpha_neg(df_m_, 'macd_diff', 2))
			print(alpha_pos(df_w_, 'macd_diff',2))
			print(alpha_pos(df_d_, 'macd_diff', 2))
			
			if alpha_pos(df_m_, 'MACD_macd', 2)  and alpha_pos(df_w_, 'macd_diff',2) and alpha_pos(df_d_, 'macd_diff', 2):
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
			
			if alpha_pos(df_m_, 2) and alpha_1(df_w_, 2) and alpha_neg(df_d_, 2) and alpha_pos(df_w_, 2):
				print('True：', code)
				c.append(code)
		except NameError:
			print(0)
	print('候选：', c)
	

	
	

if __name__ == "__main__":

	#codes = ts.get_stock_basics().index.values.tolist()
	#codes = ['600145']
	
	#df = ts.get_industry_classified()
	#df_industry_list = list(set(df.c_name.tolist()))
	#print(df_industry_list)
	
	#main1(df, '医疗器械')
	df = data_d('600145')
	arima = ARIMA(df, order=(1, 1, 1))
	result = arima.fit(disp=False)
	#pred = result.predict('2020-03-23' typ='levels')
	#print(pred)

	
	
	
	

