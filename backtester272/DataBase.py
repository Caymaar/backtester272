import pandas as pd
import os
from binance.client import Client
import yfinance as yf
from typing import List, Tuple, Optional


class DataBase:
    """
    Classe pour gérer une base de données financière avec des fonctionnalités d'intégration
    de données depuis Binance et Yahoo Finance.

    Cette classe offre des fonctionnalités de mise à jour, de suppression, et de récupération
    de données financières historiques.
    """

    def __init__(self, api_key: str = None, api_secret: str = None, verbose: bool = False) -> None:
        """
        Initialise la base de données et tente une connexion à Binance.

        Si la connexion échoue, la base de données fonctionne en mode hors-ligne.

        Args:
            api_key (str, optional): Clé API pour Binance.
            api_secret (str, optional): Secret API pour Binance.
            verbose (bool): Active les messages de débogage si True.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.verbose = verbose
        self.is_online = False

        # Tentative de connexion à Binance
        try:
            self.client = Client(self.api_key, self.api_secret)
            self.is_online = True
            if self.verbose:
                print("Connexion à Binance établie.")
        except Exception as e:
            if self.verbose:
                print(f"Impossible de se connecter à Binance: {e}")
                print("La base de données fonctionnera en mode hors-ligne.")

        if self.verbose:
            print("Initialisation de la base de données...")

        # Chargement ou création de la base de données locale
        self.load_database()

    def load_database(self) -> None:
        """
        Charge ou initialise une base de données locale à partir d'un fichier CSV.

        Si le fichier n'existe pas, un fichier vide est créé.
        """
        directory = 'data'
        database_file = 'database.csv'

        self.file_path = os.path.join(directory, database_file)

        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Créer un fichier vide si la base de données n'existe pas
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['Date'])
            df.to_csv(self.file_path, index=False)

        # Charger les données dans un DataFrame
        self.database = pd.read_csv(self.file_path, index_col='Date', parse_dates=True)

    def get_historical_close(self, symbols: List[str], start_date: str, end_date: str, backend: str) -> Optional[pd.DataFrame]:
        """
        Récupère les données de clôture historiques pour les symboles donnés.

        Args:
            symbols (List[str]): Liste des symboles à récupérer.
            start_date (str): Date de début (format YYYY-MM-DD).
            end_date (str): Date de fin (format YYYY-MM-DD).
            backend (str): Source des données ('binance' ou 'yfinance').

        Returns:
            pd.DataFrame or None: Données de clôture ou None en cas d'échec.
        """
        if backend == 'binance':
            return self.get_binance_historical_close(symbols, start_date, end_date)
        elif backend == 'yfinance':
            return self.get_yfinance_historical_close(symbols, start_date, end_date)
        else:
            raise ValueError("Backend non supporté. Utilisez 'binance' ou 'yfinance'.")

    def get_binance_historical_close(self, symbols: List[str], start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Récupère les données de clôture historiques depuis Binance.

        Args:
            symbols (List[str]): Liste des symboles à récupérer.
            start_date (str): Date de début (format YYYY-MM-DD).
            end_date (str): Date de fin (format YYYY-MM-DD).

        Returns:
            pd.DataFrame or None: Données de clôture ou None en cas d'échec.
        """
        try:
            data = {}

            # Boucle sur chaque symbole pour récupérer les données
            for symbol in symbols:
                klines = self.client.get_historical_klines(
                    symbol,
                    Client.KLINE_INTERVAL_1DAY,
                    start_date,
                    end_date
                )

                # Extraire les dates et prix de clôture
                close_data = [(pd.to_datetime(kline[0], unit='ms'), float(kline[4])) for kline in klines]
                df = pd.DataFrame(close_data, columns=['date', 'close']).set_index('date')
                data[symbol] = df['close']

            # Combiner les DataFrames pour tous les symboles
            result_df = pd.concat(data.values(), axis=1, keys=data.keys())
            result_df.index.name = 'Date'

            return result_df
        except Exception as e:
            if self.verbose:
                print(f"Erreur lors de la récupération des données Binance : {e}")
            return None

    def get_yfinance_historical_close(self, symbols: List[str], start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Récupère les données de clôture historiques depuis Yahoo Finance.

        Args:
            symbols (List[str]): Liste des symboles à récupérer.
            start_date (str): Date de début (format YYYY-MM-DD).
            end_date (str): Date de fin (format YYYY-MM-DD).

        Returns:
            pd.DataFrame or None: Données de clôture ou None en cas d'échec.
        """
        data = yf.download(symbols, start=start_date, end=end_date, progress=self.verbose)
        return data['Close']

    def save_database(self) -> None:
        """
        Sauvegarde la base de données actuelle dans un fichier CSV.
        """
        self.database = self.database.sort_index()
        self.database.to_csv(self.file_path, index=True)
        if self.verbose:
            print("Base de données sauvegardée.")

    def update_database(self, symbols: List[str], start_date: str, end_date: str, backend: str) -> None:
        """
        Met à jour la base de données avec de nouvelles données de clôture.

        Args:
            symbols (List[str]): Liste des symboles à mettre à jour.
            start_date (str): Date de début pour les nouvelles données.
            end_date (str): Date de fin pour les nouvelles données.
            backend (str): Source des données ('binance' ou 'yfinance').
        """
        if not self.is_online:
            if self.verbose:
                print("Mode hors-ligne activé. Mise à jour impossible.")
            return

        for symbol in symbols:
            if self.verbose:
                print(f"Mise à jour des données pour {symbol}...")

            # Récupérer les nouvelles données
            new_data = self.get_historical_close([symbol], start_date, end_date, backend)
            if new_data is not None:
                self.database = self.database.combine_first(new_data)
                if self.verbose:
                    print(f"Données mises à jour pour {symbol}.")
            else:
                if self.verbose:
                    print(f"Les données pour {symbol} ne sont pas disponibles.")

        # Sauvegarder les changements
        self.save_database()

    @staticmethod
    def from_ohlcv_to_close(ohlcv_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforme un DataFrame OHLCV en un DataFrame avec les prix de clôture.

        Args:
            ohlcv_df (pd.DataFrame): DataFrame contenant les colonnes 'DATE', 'ID', et 'CLOSE'.

        Returns:
            pd.DataFrame: DataFrame pivoté avec les prix de clôture.
        """
        ohlcv_df.columns = [col.upper() for col in ohlcv_df.columns]
        ohlcv_df = ohlcv_df[['DATE', 'ID', 'CLOSE']].copy()

        ohlcv_df['DATE'] = pd.to_datetime(ohlcv_df['DATE'])

        # Éliminer les doublons pour chaque combinaison de 'DATE' et 'ID'
        ohlcv_df = ohlcv_df.sort_values('DATE').drop_duplicates(subset=['DATE', 'ID'], keep='last')

        return ohlcv_df.pivot(index='DATE', columns='ID', values='CLOSE')