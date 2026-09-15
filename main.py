from extract   import carregar_origem, carregar_destino
from transform import normalizar_origem, normalizar_destino, reconstruir_estado_origem
from compare   import comparar, gerar_relatorio


def main():
    df_origem  = carregar_origem()
    df_destino = carregar_destino()

    df_origem  = normalizar_origem(df_origem)

    df_estado, ids_deletados = reconstruir_estado_origem(df_origem)

    df_destino = normalizar_destino(df_destino, df_estado_origem=df_estado)

    df_diverg  = comparar(df_estado, df_destino, ids_deletados)
    gerar_relatorio(df_diverg)

    # validação temporária — remover depois do commit
    print(f'\nPedidos deletados: {len(ids_deletados)}')
    print(f'IDs só no destino: {len(set(df_destino["id_pedido"]) - set(df_estado["id_pedido"]))}')
    print(f'Desses, são deletados: {len(set(df_destino["id_pedido"]) - set(df_estado["id_pedido"]) & ids_deletados)}')


if __name__ == '__main__':
    main()