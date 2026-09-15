from extract import carregar_origem, carregar_destino
from transform import normalizar_origem, normalizar_destino


def main():
    df_origem  = carregar_origem()
    df_destino = carregar_destino()

    df_origem  = normalizar_origem(df_origem)
    df_destino = normalizar_destino(df_destino)

    print(df_origem['status'].unique())
    print(df_destino['status'].unique())
    print(df_origem['atualizado_em'].dtype)
    print(df_destino['atualizado_em'].dtype)


if __name__ == '__main__':
    main()