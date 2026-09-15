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


def normalizar_destino(df, df_estado_origem=None):
    df = _normalizar_comum(df)
    df = df.drop_duplicates()

    if df_estado_origem is not None and df['id_pedido'].duplicated().any():
        ids_duplicados = df[df['id_pedido'].duplicated(keep=False)]['id_pedido'].unique()
        for pid in ids_duplicados:
            if pid in df_estado_origem['id_pedido'].values:
                linha_origem = df_estado_origem[df_estado_origem['id_pedido'] == pid].iloc[0]
                mask = (df['id_pedido'] == pid) & (df['status'] == linha_origem['status'])
                linhas_erradas = df[(df['id_pedido'] == pid) & ~mask]
                df = df.drop(linhas_erradas.index)
            else:
                df = df[~((df['id_pedido'] == pid) & df.duplicated(subset=['id_pedido'], keep='first'))]

    return df


def reconstruir_estado_origem(df):
    df = df.copy()
    df = df.sort_values(['id_pedido', 'atualizado_em'])

    conflitos = (
        df.groupby(['id_pedido', 'atualizado_em'])
        .filter(lambda x: x.drop_duplicates().shape[0] > 1)
        ['id_pedido']
        .unique()
    )

    df_atual = df.drop_duplicates(subset=['id_pedido'], keep='last')

    pedidos_com_d = df[df['operacao'] == 'D']['id_pedido'].unique()
    pedidos_reativados = (
        df_atual[
            (df_atual['id_pedido'].isin(pedidos_com_d)) &
            (df_atual['operacao'].isin(['I', 'U']))
        ]['id_pedido'].unique()
    )

    df_atual = df_atual.copy()
    df_atual['observacao'] = ''
    df_atual.loc[df_atual['id_pedido'].isin(conflitos), 'observacao'] = 'INDETERMINADO'
    df_atual.loc[df_atual['id_pedido'].isin(pedidos_reativados), 'observacao'] = 'AMBIGUIDADE'

    ids_deletados = set(df_atual[df_atual['operacao'] == 'D']['id_pedido'])
    df_atual = df_atual[df_atual['operacao'] != 'D']

    return df_atual, ids_deletados