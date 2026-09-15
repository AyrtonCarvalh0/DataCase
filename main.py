from extract import carregar_origem, carregar_destino
from transform import normalizar_origem, normalizar_destino, reconstruir_estado_origem


def main():
    df_origem  = carregar_origem()
    df_destino = carregar_destino()

    df_origem  = normalizar_origem(df_origem)
    df_destino = normalizar_destino(df_destino)

    df_estado  = reconstruir_estado_origem(df_origem)

    print(f'Pedidos ativos na origem: {len(df_estado)}')
    print(f'Pedidos com AMBIGUIDADE: {len(df_estado[df_estado["observacao"] == "AMBIGUIDADE"])}')
    print(f'Pedidos INDETERMINADOS: {len(df_estado[df_estado["observacao"] == "INDETERMINADO"])}')


if __name__ == '__main__':
    main()