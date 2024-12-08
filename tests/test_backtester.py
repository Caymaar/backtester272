import pytest
import pandas as pd
import numpy as np
from backtester272 import Backtester, MomentumStrategy, EqualWeightStrategy

# Fonction pour générer des prix avec une marche aléatoire
def generate_random_walk(start_price, size, volatility):
    returns = np.random.normal(loc=0, scale=volatility, size=size)
    price = start_price * (1 + returns).cumprod()
    return price

def generate_prices_dataframe(start_date, end_date, tickers, start_prices, volatility, freq="D"):
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    prices = pd.DataFrame(index=dates)
    for ticker in tickers:
        prices[ticker] = generate_random_walk(start_prices[ticker], len(dates), volatility[ticker])
    return prices

# Test avec un DataFrame vide
def test_empty_dataframe():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        Backtester(empty_df)

# Test des limites des paramètres de backtest
@pytest.mark.parametrize("aum, window, freq", [
    (0, 365, 30),  # AUM = 0
    (100, 0, 30),  # window = 0
    (100, 365, 0)  # freq = 0
])
def test_backtest_parameters_limits(aum, window, freq):
    prices = generate_prices_dataframe("2019-01-01", "2020-12-31", ["BTC", "ETH", "LTC"], {"BTC": 10000, "ETH": 500, "LTC": 100}, {"BTC": 0.02, "ETH": 0.03, "LTC": 0.04})
    backtester = Backtester(prices)
    with pytest.raises(ValueError):
        backtester.run("2020-01-01", "2020-12-31", freq=freq, window=window, aum=aum, strategy=MomentumStrategy())

# Test pour EqualWeightStrategy
def test_equal_weight_strategy():
    prices = generate_prices_dataframe("2019-01-01", "2020-12-31", ["BTC", "ETH", "LTC"], {"BTC": 10000, "ETH": 500, "LTC": 100}, {"BTC": 0.02, "ETH": 0.03, "LTC": 0.04})
    backtester = Backtester(prices)
    result = backtester.run("2020-01-01", "2020-12-31", strategy=EqualWeightStrategy())

    # Vérifier que les valeurs uniques dans result.weights.sum(axis=1) sont soit 0, soit 1
    unique_sums = result.weights.sum(axis=1).unique()
    assert np.all(np.isin(unique_sums, [0, 1])), f"Valeurs uniques inattendues: {unique_sums}"

    # Vérifier que result.performance est un pd.Series avec des dates en index
    assert isinstance(result.performance, pd.Series), "result.performance doit être un pd.Series"
    assert isinstance(result.performance.index, pd.DatetimeIndex), "L'index de result.performance doit être un pd.DatetimeIndex"

# Test pour MomentumStrategy
def test_momentum_strategy():
    prices = generate_prices_dataframe("2019-01-01", "2020-12-31", ["BTC", "ETH", "LTC"], {"BTC": 10000, "ETH": 500, "LTC": 100}, {"BTC": 0.02, "ETH": 0.03, "LTC": 0.04})
    backtester = Backtester(prices)
    result = backtester.run("2020-01-01", "2020-12-31", strategy=MomentumStrategy())

    # Vérifier que les valeurs uniques dans result.weights.sum(axis=1) sont soit 0, soit 1
    unique_sums = result.weights.sum(axis=1).unique()
    assert np.all(np.isin(unique_sums, [0, 1])), f"Valeurs uniques inattendues: {unique_sums}"

    # Vérifier que result.performance est un pd.Series avec des dates en index
    assert isinstance(result.performance, pd.Series), "result.performance doit être un pd.Series"
    assert isinstance(result.performance.index, pd.DatetimeIndex), "L'index de result.performance doit être un pd.DatetimeIndex"

# Fait une def pour voir si les dates des prix sont quotidiennes
def test_daily_prices():
    hourly_prices = generate_prices_dataframe("2019-01-01", "2020-12-31", ["BTC", "ETH", "LTC"], {"BTC": 10000, "ETH": 500, "LTC": 100}, {"BTC": 0.02, "ETH": 0.03, "LTC": 0.04}, freq="h")
    with pytest.raises(ValueError):
        Backtester(hourly_prices)