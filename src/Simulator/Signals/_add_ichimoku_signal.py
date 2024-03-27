import pandas_ta as ta
import pandas as pd
import numpy as np

def add_ichimoku_signal(df_in, **params):

    tenkan = 5
    kijun = 20
    chikou = 20
    senkou = 40

    tenkan_key = f"ITS_{tenkan}"
    kijun_key = f"IKS_{kijun}"
    chikou_key = f"ICS_{kijun}"
    senkou_a_key = f"ISA_{tenkan}"
    senkou_b_key = f"ISB_{kijun}"

    slippage_rate = params['slippage_rate']

    df = df_in.copy()

        
    high = ta.sma(df.High)
    low = ta.sma(df.Low)
    tenkan_high = high.rolling(window= tenkan).max()
    tenkan_low = low.rolling(window= tenkan).min()
    df[tenkan_key] = (tenkan_high + tenkan_low)/2
    kijun_high = high.rolling(window=kijun).max()
    kijun_low = low.rolling(window=kijun).min()
    df[kijun_key] = (kijun_high + kijun_low)/2
    df[senkou_a_key] = ((df[tenkan_key]+df[kijun_key])/2).shift(chikou-1)
    senkou_high = high.rolling(window= senkou).max()
    senkou_low = low.rolling(window= senkou).min()
    df[senkou_b_key] = ((senkou_high + senkou_low)/2).shift(chikou-1)

    conditions = [
        (df.Close > df[senkou_a_key]) 
        & (df.Close > df[senkou_b_key]) 
        & (df[tenkan_key].shift(1) <= df[kijun_key].shift(1))
        & (df[tenkan_key] > df[kijun_key])
        & (df.Close > df[tenkan_key])
        & (df[senkou_a_key] > df[senkou_b_key])
        ,
        (df.Close < df[senkou_a_key]) 
        & (df.Close < df[senkou_b_key]) 
        & (df[tenkan_key].shift(1) >= df[kijun_key].shift(1))
        & (df[tenkan_key] < df[kijun_key])
        & (df.Close < df[tenkan_key])
        & (df[senkou_a_key] < df[senkou_b_key])
    ]
    directions = [1, -1]
    df.loc[:, "signal"]= np.select(conditions, directions, default = 0)
    df["trade_opening_price"] = df.Open * (1 + df.signal * slippage_rate)
    df.drop(columns = [tenkan_key, kijun_key, senkou_a_key, senkou_b_key], inplace = True)


    return df
    
    