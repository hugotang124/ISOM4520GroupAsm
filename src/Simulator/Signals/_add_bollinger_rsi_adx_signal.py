import pandas_ta as ta  

def add_bollinger_rsi_adx_strategy(df_in, **params):
    df = df_in.copy()
    slippage_rate = params['slippage_rate']
    rsi_period = params.get('rsi_period', 14)
    bollinger_period = params.get('bollinger_period', 20)
    std_dev_factor = params.get('std_dev_factor', 2)
    adx_period = params.get('adx_period', 14)

    # Calculate Bollinger Bands
    df['middle_band'] = df['Close'].rolling(window=bollinger_period).mean()
    df['std_dev'] = df['Close'].rolling(window=bollinger_period).std()
    df['upper_band'] = df['middle_band'] + std_dev_factor * df['std_dev']
    df['lower_band'] = df['middle_band'] - std_dev_factor * df['std_dev']

    # Calculate RSI
    df['rsi'] = ta.rsi(df['Close'], length=rsi_period)

    # Calculate ADX
    df['adx'] = ta.adx(df['High'], df['Low'], df['Close'], length=adx_period)['ADX_14']

    # Generate signals
    df['signal'] = 0
    df.loc[(df['Close'] < df['lower_band']) & (df['rsi'] < 30) & (df['adx'] > 25), 'signal'] = 1
    df.loc[(df['Close'] > df['upper_band']) & (df['rsi'] > 70) & (df['adx'] > 25), 'signal'] = -1

    # Shift the signals to avoid look-ahead bias
    df['signal'] = df['signal'].shift(1)

    # Calculate trade opening price
    df['trade_opening_price'] = df['Open'] * (1 + df['signal'] * slippage_rate)

    return df