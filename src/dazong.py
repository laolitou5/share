key = '75f7cbe506f185ba42bf382701b21f5e599482881eda3dd639fd8eb2'

import tushare as ts
pro = ts.pro_api(key)

#获取南华沪铜指数
import datetime
now = datetime.datetime.now().strftime('%Y%m%d')

df_nongchanpin = pro.index_daily(ts_code='NHAI.NH', start_date='20180101', end_date=now)
df_shangpin = pro.index_daily(ts_code='NHCI.NH', start_date='20180101', end_date=now)
df_shangpin = pro.index_daily(ts_code='NHCI.NH', start_date='20180101', end_date=now)
df_
print(df)