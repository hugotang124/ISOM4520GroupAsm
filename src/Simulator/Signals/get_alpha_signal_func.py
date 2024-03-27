from ._add_random_signal import add_random_signal
from ._add_MA5_crosses_MA50_signal import add_MA5_crosses_MA50_signal
from ._add_buy_and_hold_signal import add_buy_and_hold_signal
from ._add_bollinger_rsi_adx_signal import add_bollinger_rsi_adx_strategy
from ._add_SuperTrend_signal import add_SuperTrend_signal
from ._add_macd_signal import add_macd_signal
from ._add_rsi_strategy import add_rsi_strategy
from ._add_moving_avg_crossover_signal import add_moving_average_crossover_signal
from ._add_ichimoku_signal import add_ichimoku_signal

def get_alpha_signal_func(**params):

    strategy_name = params["strategy_name"]

    strategy_signal_func_dict = {
        "random": add_random_signal,
        "MA5_cross_MA50": add_MA5_crosses_MA50_signal,
        'buy_and_hold': add_buy_and_hold_signal, 
        "bollinger_rsi_adx": add_bollinger_rsi_adx_strategy,
        "macd": add_macd_signal,
        "rsi": add_rsi_strategy,
        "adx": add_bollinger_rsi_adx_strategy,
        "supertrend": add_SuperTrend_signal,
        "ichimoku": add_ichimoku_signal
    }

    signal_func = strategy_signal_func_dict.get(strategy_name)
    if signal_func is None:
        raise NotImplementedError(
            f"Signal '{strategy_name}' is not implemented yet."
        )
    
    return signal_func