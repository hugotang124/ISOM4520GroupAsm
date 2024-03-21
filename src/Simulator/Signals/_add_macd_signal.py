import pandas_ta as ta

# use the MACD signal to generate buy/sell signals
# when macd crosses signal line from below, it's a buy signal
# when macd crosses signal line from above, it's a sell signal

def add_macd_signal(df_in, **params):
    '''
    This function adds a MACD signal to the dataframe.
    The signal is a buy when the MACD crosses the signal line from below and a sell when the MACD crosses the signal line from above.
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

    df = df_in.copy()
    slippage_rate = params['slippage_rate']
    macd_result = ta.macd(df['Close'])
    df['macd'] = macd_result.iloc[:,0]
    df['signal_line'] = macd_result.iloc[:,2]
    df['signal'] = 0
    df.loc[((df['macd'].shift(1) < df['signal_line'].shift(1)) & (df['macd'] > df['signal_line'])), 'signal'] = 1
    df.loc[((df['macd'].shift(1) > df['signal_line'].shift(1)) & (df['macd'] < df['signal_line'])), 'signal'] = -1
    # close the last trade
    df.loc[df.index[-1], 'signal'] = 0
    # # We only need to trade when the signal changes
    # df['signal'] = df['signal'].diff()
    # We need to shift the signal by one to avoid look-ahead bias
    df['signal'] = df['signal'].shift(1)
    

    df['trade_opening_price'] = df['Open'] * (1+ df['signal'] * slippage_rate)

    return df