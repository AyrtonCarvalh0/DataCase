import pandas as pd
import math


def comparar(df_estado, df_destino, ids_deletados):
    divergencias = []

    ids_origem  = set(df_estado['id_pedido'])
    ids_destino = set(df_destino['id_pedido'])

    # TIPO 1 — existe na origem ativa mas não está no destino
    ausentes = ids_origem - ids_destino
    for pid in ausentes:
        linha = df_estado[df_estado['id_pedido'] == pid].iloc[0]
        divergencias.append({
            'id_pedido'       : pid,
            'tipo_divergencia': 'PEDIDO_AUSENTE_NO_DESTINO',
            'campo'           : 'registro',
            'valor_origem'    : 'pedido ativo',
            'valor_destino'   : 'não encontrado',
            'observacao'      : linha['observacao']
        })

    # IDs no destino que não estão na origem ativa
    ids_so_no_destino = ids_destino - ids_origem
    for pid in ids_so_no_destino:
        linha_destino = df_destino[df_destino['id_pedido'] == pid].iloc[0]

        # TIPO 2 — foi deletado na origem mas ainda está no destino
        if pid in ids_deletados:
            divergencias.append({
                'id_pedido'       : pid,
                'tipo_divergencia': 'PEDIDO_DELETADO_PRESENTE',
                'campo'           : 'registro',
                'valor_origem'    : 'deletado',
                'valor_destino'   : linha_destino['status'],
                'observacao'      : ''
            })
        # TIPO 3 — não existe em lugar nenhum na origem
        else:
            divergencias.append({
                'id_pedido'       : pid,
                'tipo_divergencia': 'PEDIDO_FANTASMA',
                'campo'           : 'registro',
                'valor_origem'    : 'não existe',
                'valor_destino'   : linha_destino['status'],
                'observacao'      : ''
            })

    # pedidos comuns — compara campo a campo
    ids_comuns = ids_origem & ids_destino
    for pid in ids_comuns:
        linha_origem  = df_estado[df_estado['id_pedido'] == pid].iloc[0]
        linha_destino = df_destino[df_destino['id_pedido'] == pid].iloc[0]

        tipos = []
        campos_divergentes = {}

        # STATUS
        if linha_origem['status'] != linha_destino['status']:
            tipos.append('STATUS_DIVERGENTE')
            campos_divergentes['status'] = {
                'valor_origem': linha_origem['status'],
                'valor_destino': linha_destino['status']
            }

        if not (isinstance(linha_origem['valor_total'], float) and
                math.isnan(linha_origem['valor_total'])):
            if round(linha_origem['valor_total'], 2) != round(linha_destino['valor_total'], 2):
                tipos.append('VALOR_DIVERGENTE')
                campos_divergentes['valor_total'] = {
                    'valor_origem': linha_origem['valor_total'],
                    'valor_destino': linha_destino['valor_total']
                }
        else:
            tipos.append('VALOR_AUSENTE_NA_ORIGEM')
            campos_divergentes['valor_total'] = {
                'valor_origem': 'ausente',
                'valor_destino': linha_destino['valor_total']
            }

        if tipos:
            divergencias.append({
                'id_pedido'       : pid,
                'tipo_divergencia': '|'.join(tipos),
                'campo'           : '|'.join(campos_divergentes.keys()),
                'valor_origem'    : '|'.join(str(v['valor_origem'])  for v in campos_divergentes.values()),
                'valor_destino'   : '|'.join(str(v['valor_destino']) for v in campos_divergentes.values()),
                'observacao'      : linha_origem['observacao']
            })

    # AMBIGUIDADES
    ids_ja_reportados = {d['id_pedido'] for d in divergencias}
    ambiguos = df_estado[df_estado['observacao'] == 'AMBIGUIDADE']
    for _, linha in ambiguos.iterrows():
        pid = linha['id_pedido']
        if pid not in ids_ja_reportados:
            divergencias.append({
                'id_pedido': pid,
                'tipo_divergencia': 'AMBIGUIDADE_I_APOS_D',
                'campo': 'operacao',
                'valor_origem': 'I após D — reativação ou reuso de ID',
                'valor_destino': 'validação manual necessária',
                'observacao': 'AMBIGUIDADE'
            })
            ids_ja_reportados.add(pid)

    # INDETERMINADOS
    indeterminados = df_estado[df_estado['observacao'] == 'INDETERMINADO']
    for _, linha in indeterminados.iterrows():
        pid = linha['id_pedido']
        if pid not in ids_ja_reportados:
            divergencias.append({
                'id_pedido': pid,
                'tipo_divergencia': 'ESTADO_INDETERMINADO',
                'campo': 'atualizado_em',
                'valor_origem': 'dois eventos com mesmo timestamp e campos diferentes',
                'valor_destino': 'validação manual necessária',
                'observacao': 'INDETERMINADO'
            })
            ids_ja_reportados.add(pid)

    return pd.DataFrame(divergencias)


def gerar_relatorio(df_divergencias):
    df_divergencias.to_csv('relatorio_divergencias.csv', index=False)
    print(f'Relatório gerado: {len(df_divergencias)} divergências encontradas')
    print(df_divergencias['tipo_divergencia'].value_counts().to_string())