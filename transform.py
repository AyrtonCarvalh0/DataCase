import pandas as pd


def _normalizar_comum(df):
    df = df.copy()
    df['status'] = df['status'].str.strip().str.upper()
    df['atualizado_em'] = pd.to_datetime(df['atualizado_em'], utc=True)
    return df


def normalizar_origem(df):
    df = _normalizar_comum(df)
    df = df.drop_duplicates()
    return df


def normalizar_destino(df):
    df = _normalizar_comum(df)
    return df