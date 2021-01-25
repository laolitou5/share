import baostock as bs
import pandas as pd


def download_data(date):
    # 获取指定日期的指数、股票数据

    stock_rs = bs.query_all_stock(date)
    stock_df = stock_rs.get_data()
    # print(stock_df["code"])
    #
    # print(stock_df)
    return stock_df

def dividend(stock_df):

    codes = stock_df['code'].tolist()
    rs_list = []
    for code in codes:
        rs_dividend_2019 = bs.query_dividend_data(code=code, year="2019", yearType="report")
        while (rs_dividend_2019.error_code == '0') & rs_dividend_2019.next():
            rs_list.append(rs_dividend_2019.get_row_data())
        result = pd.DataFrame(rs_list, columns=rs_dividend_2019.fields)
        # if len(result) > 0:
    result.to_csv('share.csv', encoding='gb18030', index=False)


if __name__ == '__main__':
    # 获取指定日期全部股票的日K线数据
    bs.login()
    df = download_data("2019-09-25")
    dividend(df)

    bs.logout()