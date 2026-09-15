from extract import carregar_origem, carregar_destino

df_origem  = carregar_origem()
df_destino = carregar_destino()

print(df_origem.shape)
print(df_destino.shape)