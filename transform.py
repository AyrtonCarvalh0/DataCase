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

def reconstruir_estado_origem(df):
    df = df.copy()

    # 1. Ordena por pedido e data — do mais antigo para o mais recente
    df = df.sort_values(['id_pedido', 'atualizado_em'])

    # 2. Detecta conflito de timestamp — mesmo pedido, mesmo momento, campos diferentes
    conflitos = (
        df.groupby(['id_pedido', 'atualizado_em'])
        .filter(lambda x: x.drop_duplicates().shape[0] > 1)
        ['id_pedido']
        .unique()
    )

    # 3. Pega o evento mais recente de cada pedido
    df_atual = df.drop_duplicates(subset=['id_pedido'], keep='last')

    # 4. Marca pedidos com I após D como AMBIGUIDADE
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

    # 5. Remove pedidos cujo último evento foi D — não existem mais
    df_atual = df_atual[df_atual['operacao'] != 'D']

    return df_atual