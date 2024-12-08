import pytest
import pandas as pd
import numpy as np
from backtester272 import Universe


# Test de l'univers avec une liste vide
def test_universe_empty_list():
    universe = Universe()
    empty_list = []
    result = universe.get_crypto_prices(empty_list, "2020-01-01", "2020-12-31")
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_universe_crypto():
    universe = Universe()
    tickers = ["BTCUSDT"]
    prices = universe.get_crypto_prices(tickers, "2020-01-01", "2020-12-31")

    # Vérifie si le résultat est un DataFrame avec du float en valeur, BTCUSDT en colonne et des dates en index
    assert isinstance(prices, pd.DataFrame), "Le résultat doit être un DataFrame"
    assert prices.columns == ["BTCUSDT"], "La colonne doit être 'BTCUSDT'"
    assert prices.dtypes.iloc[0] == "float64", "Les valeurs doivent être des float"
    assert isinstance(prices.index, pd.DatetimeIndex), "L'index doit être un pd.DatetimeIndex"

def test_universe_yfinance():
    universe = Universe()
    tickers = ["AAPL"]
    prices = universe.get_equity_prices(tickers, "2020-01-01", "2020-12-31")

    # Vérifie si le résultat est un DataFrame avec du float en valeur, BTC-USD en colonne et des dates en index
    assert isinstance(prices, pd.DataFrame), "Le résultat doit être un DataFrame"
    assert prices.columns == ["AAPL"], "La colonne doit être 'BTC-USD'"
    assert prices.dtypes.iloc[0] == "float64", "Les valeurs doivent être des float"
    assert isinstance(prices.index, pd.DatetimeIndex), "L'index doit être un pd.DatetimeIndex"