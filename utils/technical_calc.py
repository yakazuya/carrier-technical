import os
import numpy as np
from utils.judge import *

def RSI(config, df, date) -> dict:
    RSI_result = {}
    for key in config['ticker'].keys():
        if 'RSI' in config['ticker'][key]:
            n = config['ticker'][key]['RSI'][0]
            key = national_judgment(key)
            key_df = df['Adj Close'][key]
            delta = key_df.diff()

            # 一定期間の変動幅を計算する

            # 上昇幅と下落幅を分けて計算する
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)

            # 上昇幅と下落幅の移動平均を計算する
            avg_gain = gain.rolling(window=n).mean()
            avg_loss = loss.rolling(window=n).mean()

            # RSIを計算する
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            yesterday_rsi = rsi.loc[date]
            key = national_judgment(key)
            RSI_result[key] = yesterday_rsi
    # print(RSI_result)
    # {'AAPL': 65.6580450117568, 'AMD': 60.78203822141435}
    return RSI_result

def BOLL(config, df, date) -> dict:
    BOLL_result = {}
    for key in config['ticker'].keys():
        if 'BOLL' in config['ticker'][key]:
            n = config['ticker'][key]['BOLL'][0]
            num_std = config['ticker'][key]['BOLL'][1]
            key = national_judgment(key)
            key_df = df['Adj Close'][key]

            # 移動平均を計算する
            rolling_mean = key_df.rolling(window = n).mean()
            # 標準偏差を計算する
            rolling_std = key_df.rolling(window = n).std()
            # ボリンジャーバンドの上限を計算する
            upper_band = rolling_mean + (rolling_std * num_std)
            # ボリンジャーバンドの下限を計算する
            lower_band = rolling_mean - (rolling_std * num_std)
            # ボリンジャーバンドの中心線を計算する
            middle_band = rolling_mean

            key = national_judgment(key)
            BOLL_result[key] = {}
            BOLL_result[key]['upper_band'] = upper_band.loc[date]
            BOLL_result[key]['lower_band'] = lower_band.loc[date]
            BOLL_result[key]['middle_band'] = middle_band.loc[date]
    # print(BOLL_result)
    # 結果をDataFrameとして返す
    return BOLL_result