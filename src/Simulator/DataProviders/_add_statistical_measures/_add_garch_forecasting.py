from arch import arch_model


def _add_garch_forecasting(df, interval, **params):
    """
    Add GARCH forecasting results to the dataframe.
    """

    ##TODO: ASSIGNMENT #4 - Add GARCH forecasting here

    should_add_garch = params['should_add_garch']

    if not should_add_garch:
        return df

    df = df.copy()
    
    ## TODO: Add GARCH forecasting

    returns = df['Close'].pct_change().dropna()

    # use the GARCH model to forecast the volatility
    garch_model = arch_model(returns, vol='Garch', p=1, q=1)
    garch_result = garch_model.fit(disp='off')
    garch_forecast = garch_result.forecast(horizon=1)

    # add the forecasted volatility to the dataframe
    df['stat_garch_vol'] = garch_forecast.variance.values[-1]
    print("result of garch:", df['stat_garch_vol'], garch_forecast.variance.values[-1,0])

    df['stat_garch_vol'] = df['stat_garch_vol'].shift(1)

    return df