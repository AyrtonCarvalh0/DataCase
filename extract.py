import os.path

import pandas as pd
import sys


def carregar_origem():
    try:
        return pd.read_csv('pedidos_origem.csv')
    except FileNotFoundError:
        print("Erro: arquivo 'pedidos_origem.csv' não encontrado. Coloque o arquivo na raiz do projeto.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Erro: arquivo 'pedidos_origem.csv' está corrompido ou mal formatado.")
        sys.exit(1)


def carregar_destino():
     try:
        return pd.read_csv('pedidos_destino.csv')
     except FileNotFoundError:
        print("Erro: arquivo 'pedidos_destino.csv' não encontrado. Coloque o arquivo na raiz do projeto.")
        sys.exit(1)
     except pd.errors.ParserError:
        print("Erro: arquivo 'pedidos_destino.csv' está corrompido ou mal formatado.")
        sys.exit(1)