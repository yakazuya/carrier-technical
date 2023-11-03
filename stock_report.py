import os
import pandas as pd
from pandas_datareader import data as pdr
import datetime
import yfinance as yf
import yaml

from utils.technical_calc import *
from utils.get_data import *
from utils.notify import *
from utils.judge import *

def get_config() -> dict:
    symble = []
    file_abs_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_abs_path)
    config_path = f'{file_dir}/config.yaml'
    with open(config_path, 'r') as yml:
        config = yaml.load(yml, Loader=yaml.FullLoader)

    ticker = config['ticker']
    for key in ticker.keys():
        if type(key) != str:
            key = str(key) + '.T'
            # print(key)
        symble.append(key)
    """
    {'score_threshold': 0, 'ticker': {'AAPL': {'RSI': [14, 70, 30], 'BOLL': [14, 3]}, 'AMD': {'RSI': [14, 70, 30], 'BOLL': [14, 3]}}}
    <class 'dict'>
    {'AAPL': {'RSI': [14, 70, 30], 'BOLL': [14, 3]}, 'AMD': {'RSI': [14, 70, 30], 'BOLL': [14, 3]}}
    AAPL:{'RSI': [14, 70, 30], 'BOLL': [14, 3]}
    AMD:{'RSI': [14, 70, 30], 'BOLL': [14, 3]}
    ['AAPL', 'AMD']
    """
    return config, symble

def judge(config, df, result) -> dict:
    notify_dict = {}
    for key in config['ticker'].keys():
        # RSIを設定していた場合に閾値を超えているか
        if 'RSI' in config['ticker'][key]:
            rsi = result['RSI'][key]
            # 上限を超えている場合
            if rsi > config['ticker'][key]['RSI'][1]:
                notify_dict[key] = {}
                upper = config['ticker'][key]['RSI'][1]
                notify_dict[key]['RSI'] = f'RSIが{upper}を超えています'
            # 下限を超えている場合
            elif rsi < config['ticker'][key]['RSI'][2]:
                notify_dict[key] = {}
                lower = config['ticker'][key]['RSI'][2]
                notify_dict[key]['RSI'] = f'RSIが{lower}を下回っています'
        
        # BOLLを設定した場合に終値がBOLL超えているか
        if 'BOLL' in config['ticker'][key]:
            key = national_judgment(key)
            price = df['Adj Close'][key][-1]
            key = national_judgment(key)
            σ = config['ticker'][key]['BOLL'][1]
            # BOLLの上を超えている場合
            if price > result['BOLL'][key]['upper_band']:
                if key not in notify_dict:
                    notify_dict[key] = {}
                notify_dict[key]['BOLL'] = f'BOLLが{σ}σを上回っています'
            # BOLLの下を超えている場合
            if price < result['BOLL'][key]['lower_band']:
                if key not in notify_dict:
                    notify_dict[key] = {}
                notify_dict[key]['BOLL'] = f'BOLLが{σ}σを下回っています'
            # elif price < result['BOLL'][key]['lower_band']:
            #     if not(key in notify_list):    

    return notify_dict


def main():
    result = {}
    slack_id = os.environ['SLACK_ID'] or os.getenv("SLACK_ID")
    config, symble = get_config()
    yfinance = True
    if yfinance == True:
        df = yahoo(symble)
    else:
        df = pandas()
    # date

    # date = df[-1:0]
    date = str(df.index.date[-1])
    result['RSI'] = RSI(config, df, date)
    result['BOLL'] = BOLL(config, df, date)
    # print(result)
    notify_dict = judge(config, df, result)

    notify(notify_dict, slack_id)


if __name__ == '__main__':
    main()
