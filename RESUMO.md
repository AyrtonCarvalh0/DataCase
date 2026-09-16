# Resumo Executivo — Reconciliação de Pedidos

**Preparado para:** Gerência Comercial  
**Data:** junho de 2026

---

## O Que Foi Encontrado

De um total de **133 pedidos ativos** no sistema de origem,
**25 apresentam algum tipo de problema** no relatório analítico.
Isso representa **18,8% da base ativa**.

---

## Tipos de Problema

| Problema | Quantidade |
|---|---|
| Valor no relatório diferente do sistema de pedidos | 9 pedidos |
| Pedido ativo no sistema que não aparece no relatório | 5 pedidos |
| Pedido excluído do sistema que ainda aparece no relatório | 5 pedidos |
| Status no relatório diferente do sistema de pedidos | 3 pedidos |
| Status e valor incorretos ao mesmo tempo | 3 pedidos |
| Pedidos sem valor registrado no sistema de origem | 3 pedidos |

---

## Impacto Financeiro

O faturamento exibido no relatório está **R$ 909,69 acima** do valor real.

- **Valor real (sistema de origem):** R$ 26.245,33
- **Valor no relatório:** R$ 27.155,02
- **Diferença:** R$ 909,69

Outros 3 pedidos não entraram nesse cálculo porque o sistema
de origem não registrou o valor deles. Esses casos precisam
de investigação separada junto à equipe operacional.

---

## O Que Resolver Primeiro

**Prioridade 1 — Pedidos excluídos ainda visíveis no relatório (5 casos)**

São pedidos que foram cancelados ou removidos do sistema mas
continuam aparecendo nos relatórios. Isso significa que a área
comercial pode estar tomando decisões com base em pedidos que
não existem mais. É o problema mais crítico porque afeta
diretamente a confiabilidade dos dados.

**Prioridade 2 — Valores incorretos (9 casos, diferença de R$ 909,69)**

O faturamento total do relatório está inflado. Qualquer meta
ou projeção baseada nesses números está errada.

**Prioridade 3 — Pedidos ativos invisíveis no relatório (5 casos)**

Cinco pedidos existem e estão ativos no sistema de pedidos,
mas não aparecem em nenhum lugar do relatório comercial.
A área comercial nunca os viu. O valor desses pedidos
não está sendo contabilizado nas métricas de faturamento,
o que significa que o total real de vendas pode ser
ainda maior do que o apurado nesta análise.

---

> Este relatório foi gerado automaticamente a partir da comparação
> entre o sistema transacional e a tabela analítica.
> Casos marcados como ambíguos requerem validação manual.