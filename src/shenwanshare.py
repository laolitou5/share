#
from opendatatools import swindex
from share import getcandlecharts

def data_code(ss):
    df, msg = swindex.get_index_cons(ss)
    return df.stock_code.tolist()

if __name__ == '__main__':
    df, msg = swindex.get_index_list()
    #df.to_csv('zhishu.csv', encoding='gbk')
    codes = data_code('801750')
    getcandlecharts(codes)