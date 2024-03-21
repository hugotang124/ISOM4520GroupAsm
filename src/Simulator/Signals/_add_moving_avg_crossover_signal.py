import numpy as np

# add a trading strategy signal using the Moving Average Crossover with a 50-day moving average and 200-day moving average
def add_moving_average_crossover_signal(df_in, **params):
    
        df = df_in.copy()
        slippage_rate = params['slippage_rate']
    
        df['50d'] = df['Close'].rolling(window=50).mean()
        df['200d'] = df['Close'].rolling(window=200).mean()
    
        df['signal'] = np.where(df['50d'] > df['200d'], 1, -1)
        df['trade_opening_price'] = df['Open'] * (1+ df['signal'] * slippage_rate)
    
        return df
