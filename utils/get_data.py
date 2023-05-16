import os
import pandas as pd
from pandas_datareader import data as pdr
import datetime
import yfinance as yf
import yaml


def yahoo(symble):
    start = datetime.date.today() - datetime.timedelta(days=365)
    end = datetime.date.today()
    yf.pdr_override()
    # 株価の取得
    df= pdr.get_data_yahoo(symble,start,end)
    # 前日終値の取得
    # price = df.tail(1)['Close'].values
    # 出力
    return df

def pandas():
    print('開発中')
    # expire_after = datetime.timedelta(days=3)

    # session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

    # session.headers = DEFAULT_HEADERS

    # start = datetime.datetime(2010, 1, 1)

    # end = datetime.datetime(2013, 1, 27)

    # f = pdr.DataReader("9020.T", 'yahoo', start, end, session=session)

    # f.loc['2010-01-04']
    # print(f)