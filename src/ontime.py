
import pandas as pd
import re
from real_time_stock import Stock
import time
import numpy as np
from multiprocessing import Pool

def kkk(x):

    real_ = Stock([x])
    df_real = real_.fitPrice()[["name", "open_today", "close_yesterday", "price_ontime", "count_buy1", \
                                "count_buy2", "count_buy3", "count_sell1", "count_sell2", "count_sell3"]]
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

    df = pd.read_csv('../data/bs_hist_merge_new.csv', converters={'code': str})
    k = list(set(df.symbol.tolist()))
    kk = [re.search('[a-zA-Z]+', s).group().lower() + re.search('\d+', s).group() for s in k]

    while(1):
        try:
            s1 = time.time()
            print('##################################################################################################################')

            df1 = cur_data(kk)
            df1.rename(columns={'committee':'committee1'}, inplace=True)
            time.sleep(20)
            df2 = cur_data(kk)
            df2.rename(columns={'price_ontime': 'price_ontime2', 'committee':'committee2'}, inplace=True)

            df = pd.merge(df1, df2[['name', 'price_ontime2', 'committee2']], on='name')
            df['bool'] = df[['name']].apply(lambda x: 1 if 'ST' in x['name'] or '退' in x['name'] else 0, axis=1)
            df['name'] = df[['name']].apply(lambda x: re.sub('var hq_str_', '', x['name']), axis=1)
            df = df[((df['bool'] == 0)&(df.close_yesterday != 0)&(df.open_today != 0))]

            df['r_ontime'] = df[['close_yesterday', 'price_ontime', 'price_ontime2']].apply(
                lambda x: np.sign(float(x['price_ontime2']) - float(x['close_yesterday'])) * round(
                    (float(x['price_ontime2']) - float(x['price_ontime'])) / (float(x['close_yesterday'])) * 100,
                    2) if float(x['close_yesterday']) > 0 else -100, axis=1)
            df['rr_day'] = df[['close_yesterday', 'price_ontime', 'price_ontime2']].apply(lambda x: round(
                (float(x['price_ontime2']) - float(x['close_yesterday'])) / float(x['close_yesterday']) * 100, 2) if float(
                x['close_yesterday']) > 0 else -100, axis=1)

            df = df[["name", "open_today", "price_ontime2","r_ontime", "rr_day", 'committee1', 'committee2']]
            df.sort_values(by=['r_ontime', 'rr_day'], inplace=True, ascending=False)
            print('实时变化率：', df.head(30))
            df.sort_values(by=['rr_day','r_ontime'], inplace=True, ascending=False)
            print('price变化：', df.head(30))
            df['committee_diff'] = df[['committee1', 'committee2']].apply(lambda x: x['committee2'] - x['committee1'], axis=1)
            df.sort_values(by=['committee_diff', 'committee2', 'committee1'],inplace=True, ascending=False)
            # print('委比：', df.head(30))
            s2 = time.time()

            print('time:', s2-s1)
        except Exception as e:
            print(e)



