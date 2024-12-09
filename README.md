# Backtester272

**Version**: 1.0.2
**Auteurs**: Jules Mourgues-Haroche, Alexandre Remiat, Walid Boudini, Cassandre Amizet  

---

## Description

Backtester272 est un projet de backtesting permettant de tester des stratégies d'investissement sur des données historiques provenant de sources comme Binance et Yahoo Finance. Ce package offre une flexibilité dans la personnalisation des stratégies et permet d'exploiter des classes pour gérer les données, construire des univers de trading, et analyser les résultats.

![Structure du projet](image/draw.jpg)

---

## Fonctionnalités principales

1. **Backtesting complet** avec gestion des univers dynamiques.
2. **Stratégies prédéfinies** (pondération égale, minimisation de variance, maximisation du Sharpe, momentum, etc.).
3. **Intégration des données** de Binance et Yahoo Finance pour les cryptomonnaies et actions.
4. **Visualisations interactives** avec Matplotlib et Plotly.
5. **Analyse des métriques de performance** (CAGR, volatilité, drawdown, ratio de Sharpe, etc.).

---

## Structure du projet

```plaintext
├── .github/workflows/
│   └── test.yml               # Configuration GitHub Actions pour lancer les tests
├── backtester272/             # Package principal
│   ├── Backtester.py          # Classe principale pour exécuter le backtest
│   ├── DataBase.py            # Gestion des données historiques
│   ├── Result.py              # Analyse et visualisation des résultats
│   ├── Strategy.py            # Définitions des stratégies abstraites
│   ├── StrategyBank.py        # Stratégies implémentées
│   ├── Universe.py            # Construction des univers d'actifs
│   └── __init__.py            # Initialisation du package
├── data/
│   └── database.csv           # Base de données locale d'exemple
├── examples/
│   ├── simple_examples.ipynb  # Exemple simple d'utilisation du backtester
│   └── data/database.csv      # Fichier CSV d'exemple
├── image/
│   └── draw.jpg               # Schéma de la structure du projet
├── pyproject.toml             # Configuration de gestion des dépendances
├── tests/
│   ├── test_backtester.py     # Tests unitaires pour Backtester
│   ├── test_universe.py       # Tests unitaires pour Universe
│   └── __init__.py            # Initialisation des tests
└── README.md                  # Documentation (ce fichier)
```

Voici une version complète et détaillée en Markdown, incluant toutes les informations nécessaires pour le fichier README.md :

# Backtester272

![Structure du projet](image/draw.jpg)

**Version**: 0.3.0  
**Auteurs**: Jules Mourgues-Haroche, Alexandre Remiat, Walid Boudini, Cassandre Amizet  

---

## Description

Backtester272 est un projet de backtesting permettant de tester des stratégies d'investissement sur des données historiques provenant de sources comme Binance et Yahoo Finance. Ce package offre une flexibilité dans la personnalisation des stratégies et permet d'exploiter des classes pour gérer les données, construire des univers de trading, et analyser les résultats.

---

## Fonctionnalités principales

1. **Backtesting complet** avec gestion des univers dynamiques.
2. **Stratégies prédéfinies** (pondération égale, minimisation de variance, maximisation du Sharpe, momentum, etc.).
3. **Intégration des données** de Binance et Yahoo Finance pour les cryptomonnaies et actions.
4. **Visualisations interactives** avec Matplotlib et Plotly.
5. **Analyse des métriques de performance** (CAGR, volatilité, drawdown, ratio de Sharpe, etc.).

---

## Structure du projet

```plaintext
├── .github/workflows/
│   └── test.yml               # Configuration GitHub Actions pour lancer les tests
├── backtester272/             # Package principal
│   ├── Backtester.py          # Classe principale pour exécuter le backtest
│   ├── DataBase.py            # Gestion des données historiques
│   ├── Result.py              # Analyse et visualisation des résultats
│   ├── Strategy.py            # Définitions des stratégies abstraites
│   ├── StrategyBank.py        # Stratégies implémentées
│   ├── Universe.py            # Construction des univers d'actifs
│   └── __init__.py            # Initialisation du package
├── data/
│   └── database.csv           # Base de données locale d'exemple
├── examples/
│   ├── simple_examples.ipynb  # Exemple simple d'utilisation du backtester
│   └── data/database.csv      # Fichier CSV d'exemple
├── image/
│   └── draw.jpg               # Schéma de la structure du projet
├── pyproject.toml             # Configuration de gestion des dépendances
├── tests/
│   ├── test_backtester.py     # Tests unitaires pour Backtester
│   ├── test_universe.py       # Tests unitaires pour Universe
│   └── __init__.py            # Initialisation des tests
└── README.md                  # Documentation (ce fichier)
```

--- 

## Installation

Prérequis

	•	Python >= 3.10
	•	Poetry pour gérer les dépendances

Installation du projet

	1.	Clonez le dépôt :

```bash
git clone <URL_DU_DEPOT>
cd backtester272
```

	2.	Installez les dépendances :

```bash
pip install poetry
poetry install
```

	3.	Activez l’environnement virtuel :

```bash
poetry shell
```

---

## Utilisation

Exemple minimal d’utilisation

```python
import pandas as pd
from backtester272 import Backtester, EqualWeightStrategy

# Chargement des données
data = pd.read_csv('data/database.csv', index_col='Date', parse_dates=True)

# Initialisation du backtester
backtester = Backtester(data)

# Exécution avec une stratégie à pondération égale
result = backtester.run(start_date='2020-01-01', end_date='2020-12-31', strategy=EqualWeightStrategy())

# Affichage des métriques
result.show_metrics()

# Visualisation
result.visualize()
```

---

## Classes principales

1. Backtester

	•	Effectue le backtest en utilisant des données de prix et une stratégie définie.
	•	Principaux paramètres :
	•	data : pd.DataFrame des données de prix.
	•	start_date, end_date : Période du backtest.
	•	strategy : Objet d’une classe fille de Strategy.
	•	aum : Actifs sous gestion (par défaut : 100).
	•	transaction_cost : Coût des transactions en pourcentage.

2. Strategy

	•	Classe abstraite pour implémenter des stratégies d’investissement.
	•	Stratégies disponibles :
	•	EqualWeightStrategy : Poids égaux entre les actifs.
	•	RandomStrategy : Poids aléatoires normalisés.
	•	MomentumStrategy : Basée sur les rendements passés.
	•	MinVarianceStrategy : Minimisation de la variance.
	•	MaxSharpeStrategy : Maximisation du ratio de Sharpe.

3. Result

	•	Analyse les résultats d’un backtest.
	•	Méthodes principales :
	•	show_metrics() : Affiche les métriques de performance.
	•	visualize() : Visualise la performance du portefeuille.
	•	plot_dashboard() : Compare plusieurs stratégies.

4. Universe

	•	Gère les univers d’actifs en récupérant des données via CoinGecko, Binance, ou Yahoo Finance.

---

## Tests unitaires

Les tests sont définis dans le dossier tests/ et incluent des cas pour les classes principales.
Pour exécuter les tests :

```bash
poetry run pytest
```

---

## Licence

Ce projet est sous licence MIT.
