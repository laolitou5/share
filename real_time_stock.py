# -*-coding:utf-8 -*-

import requests
import json
#from sendEmail import errorEmail
#from define import *
import datetime
import pandas as pd

class Stock:
    def __init__(self,code):
        #self.name = name
        self.code_list = code


    def __getPrice(self):
        #slice_num, value_num = 21, 3
        #name, now = u'——无——', u'  ——无——'
        #if self.code in ['s_sh000001', 's_sz399001']:
        #    slice_num = 23
        #    value_num = 1
        out = []
        for ele in self.code_list:
            r = requests.get("http://hq.sinajs.cn/list=%s" % (ele))
            res = r.text.split(',')
            out.append(res)
        #print(json.dumps(res, ensure_ascii=False))
        #if len(res) > 1:
        #    name, nowPrice = res[0][slice_num:], res[value_num]
        #return name.encode('utf-8'), float(nowPrice)
        return out




    def fitPrice(self):
        res = self.__getPrice()
        col = ['name', 'open_today', 'close_yesterday', 'price_ontime', 'price_highest', 'price_lower', 'jbuy1','jsell1', 'count', 'money', 'count_buy1', 'price_buy1', 'count_buy2', 'price_buy2','count_buy3', 'price_buy3','count_buy4', 'price_buy4','count_buy5', 'price_buy5', 'count_sell1', 'price_sell1','count_sell2', 'price_sell2', 'count_sell3', 'price_sell3','count_sell4', 'price_sell4', 'count_sell5', 'price_sell5', 'date', 'time', 'null']
        df = pd.DataFrame(res, columns=col)
        df1 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
        print(df1)

        return df1
        #exit(-1)
        #if(name!=self.name):
        #    msg = '股票名字不符，code: %s, local_name: %s, name: %s 。' % (self.code, self.name, name)
        #    errorEmail(msg)
        #    print(json.dumps(msg, ensure_ascii=False))
        #else:
        #    print('name ok!')
        #nowtime = datetime.datetime.now()
        #if(rule.high_threshold and price > rule.high_threshold):
        #    return {'code': CODE_SEND_EMAIL, 'msg': '高价提醒, %s, price: %.3f, time:%s' % (name, price, nowtime)}
        #elif(rule.low_threshold and price < rule.low_threshold):
        #    return {'code': CODE_SEND_EMAIL, 'msg': '低价提醒,name: %s, price: %.3f, time:%s' % (name, price, nowtime)}
        #else:
        #    return {'code': CODE_NOT_SEND_EMAIL, 'msg': '无提醒'}

def plot():
    import numpy as np
    import matplotlib.pyplot as plt
    plt.axis([0, 100, 0, 1])
    plt.ion()
    xs = [0, 0]
    ys = [1, 1]
    for i in range(100):
        y = np.random.random()
        xs[0] = xs[1]
        ys[0] = ys[1]
        xs[1] = i
        ys[1] = y
        plt.plot(xs, ys)
        plt.pause(0.3)
			   
if __name__ == '__main__':
	s = Stock(['sz002074', 'sz002245'])
	print(s.fitPrice())
    plot()



