#

import pandas as pd
import re
from real_time_stock import Stock
import time
import numpy as np
from multiprocessing import Pool

def kkk(x):

    real_ = Stock([x])
    df_real = real_.fitPrice()[["name", "open_today", "close_yesterday", "price_ontime", "count_buy1", \
                                "count_buy2", "count_buy3", "count_sell1", "count_sell2", "count_sell3"]]#, 'price_buy1','price_buy2', 'price_buy3', 'price_sell1', 'price_sell2', 'price_sell3'
    df_real["count_buy"] = df_real["count_buy1"].astype(int) + df_real["count_buy2"].astype(int) + df_real[
        "count_buy3"].astype(int)
    df_real["count_sell"] = df_real["count_sell1"].astype(int) + df_real["count_sell2"].astype(int) + df_real[
        "count_sell3"].astype(int)
    df_real["committee"] = df_real.apply(
        lambda x: round((x["count_buy"] - x["count_sell"]) / (x["count_sell"] + x["count_buy"]), 2) if (x[
                                                                                                            "count_sell"] +
                                                                                                        x[
                                                                                                            "count_buy"]) > 0 else 0,
        axis=1)
    # df_real['buy1_price'] = df_real.apply(lambda x: float(x['count_buy1'])*float(x['price_buy1']), axis=1)
    # df_real['buy2_price'] = df_real.apply(lambda x: float(x['count_buy2']) * float(x['price_buy2']), axis=1)
    # df_real['buy3_price'] = df_real.apply(lambda x: float(x['count_buy3']) * float(x['price_buy3']), axis=1)
    #
    # df_real['sell1_price'] = df_real.apply(lambda x: float(x['count_sell1']) * float(x['price_sell1']), axis=1)
    # df_real['sell2_price'] = df_real.apply(lambda x: float(x['count_sell2']) * float(x['price_sell2']), axis=1)
    # df_real['sell3_price'] = df_real.apply(lambda x: float(x['count_sell3']) * float(x['price_sell3']), axis=1)

    df_real.drop(["count_buy1", "count_buy2", "count_buy3", "count_sell1", "count_sell2", "count_sell3", "count_buy",
                  "count_sell"], inplace=True, axis=1)


    return df_real


def cur_data(kk):

    p = Pool(6)
    s = []
    for ele in kk:
        s.append(p.apply_async(kkk, args=(ele,)))
    p.close()
    p.join()
    ss = []
    for res in s:
        ss.append(res.get())

    df = pd.concat(ss)
    return df


if __name__ == '__main__':
    s = ['sh000001', 'sz300753', 'sz300865', 'sh603078', 'sz300770', 'sz300576', 'sh600206', 'sz002797', 'sz002245','sz002364','sz002557', 'sh600885', 'sh600305', 'sh600206']
    while (1):
        try:
            s1 = time.time()
            print(
                '##################################################################################################################')
            df = cur_data(s)
            df['name'] = df[['name']].apply(lambda x: re.sub('var hq_str_', '', x['name']), axis=1)
            print(df)
            time.sleep(15)
            s2 = time.time()

            print('time:', s2-s1)

        except Exception as e:
            print(e)