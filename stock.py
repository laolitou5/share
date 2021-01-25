# -*-coding:utf-8 -*-

import requests
import json
#from sendEmail import errorEmail
#from define import *
import datetime

class Stock:
    def __init__(self,code):
        #self.name = name
        self.code = code


    def __getPrice(self):
        #slice_num, value_num = 21, 3
        #name, now = u'——无——', u'  ——无——'
        #if self.code in ['s_sh000001', 's_sz399001']:
        #    slice_num = 23
        #    value_num = 1
        r = requests.get("http://hq.sinajs.cn/list=%s" % (self.code))
        res = r.text.split(',')
        #print(json.dumps(res, ensure_ascii=False))
        #if len(res) > 1:
        #    name, nowPrice = res[0][slice_num:], res[value_num]
        #return name.encode('utf-8'), float(nowPrice)
        return res

    def fitPrice(self, rule):
        res = self.__getPrice()
        return res
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
			
if __name__ == '__main__':
	s = Stock('sz002597')
	s.fitPrice(' ')


