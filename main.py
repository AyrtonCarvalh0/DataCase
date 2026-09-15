from extract   import carregar_origem, carregar_destino
from transform import normalizar_origem, normalizar_destino, reconstruir_estado_origem
from compare   import comparar, gerar_relatorio


def main():
    df_origem  = carregar_origem()
    df_destino = carregar_destino()

    df_origem              = normalizar_origem(df_origem)
    df_estado, ids_deletados = reconstruir_estado_origem(df_origem)
    df_destino             = normalizar_destino(df_destino, df_estado_origem=df_estado)

    df_diverg = comparar(df_estado, df_destino, ids_deletados)
    gerar_relatorio(df_diverg)


if __name__ == '__main__':
    main()