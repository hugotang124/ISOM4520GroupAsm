import pandas_ta as ta
import numpy as np
import pandas as pd


def add_SuperTrend_signal(df_in, **params):
    '''
    This function adds a SuperTrend signal to the dataframe.
    A signal is generated when the SuperTrend Indicator and the closing price crosses.
    Buy signal is concluded when SuperTrend was higher than close price previously, while sell signal works vice versa. 
    The trade opening price is the open price of the stock multiplied by 1 plus the signal multiplied by the slippage rate.

    Two new columns should be added to the dataframe:
    - signal: which gives the signal for the trade. 1 for long, -1 for short, 0 for no trade
    - trade_opening_price: which gives the price at which the trade is assumed to be opened

    Using the open price as the trade opening price is a good assumption because
    we are assuming that the trade is opened at the open price of the stock.

    Parameters
    ----------
    df_in : pd.DataFrame
        Input dataframe
    params : dict
        Dictionary of parameters
    
    Returns
    -------
    pd.DataFrame
        DataFrame with added signal and trade_opening_price columns
    '''

    period = 10
    multiplier = 3 
    SUPERTREND_VAL_KEY = f"SUPERT_{period}_{float(multiplier)}"
    SUPERTREND_TREND_KEY = f"SUPERTd_{period}_{float(multiplier)}"
    selected_columns = [SUPERTREND_VAL_KEY, SUPERTREND_TREND_KEY]
    slippage_rate = params["slippage_rate"]


    df = df_in.copy()
    supertrend = ta.supertrend(df.High, df.Low, df.Close, period, multiplier)[selected_columns]
    df[supertrend.columns] = supertrend.values
    df["SUPERT_PREV"] = df[SUPERTREND_VAL_KEY].shift(1)
    df["Close_PREV"] = df.Close.shift(1)
    conditions = [(df["SUPERT_PREV"] > df["Close_PREV"]) & (df[SUPERTREND_VAL_KEY] < df["Close"]), \
                  (df["SUPERT_PREV"] < df["Close_PREV"]) & (df[SUPERTREND_VAL_KEY] > df["Close"])]
    signals = [1, -1]
    df["signal"] = np.select(conditions, signals, default = 0)
    df["trade_opening_price"] = df.Open * (1 + df.signal * slippage_rate)
    
    required_cols = list(filter(lambda x: not x.endswith("PREV") and not x in supertrend.columns, df.columns))
    
    return df[required_cols]