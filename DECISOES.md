# Decisões Técnicas — Reconciliação de Pedidos

---

## 1. Decisões Tomadas

### 1.1 Fonte da Verdade
A base origem foi tratada como única fonte da verdade.
Onde havia conflito entre origem e destino, a origem prevalece
sempre. Onde a origem não tinha informação (ex: valor NaN),
optou-se por não inferir nem usar o valor do destino.

### 1.2 Normalização de Dados
Antes de qualquer comparação, os dois lados foram normalizados:

- **Status:** `strip().upper()` em ambos os lados.
  O destino continha variações como `'pago'`, `' CANCELADO'`
  e `'ENTREGUE '` que gerariam falsos positivos sem tratamento.
- **Timestamps:** convertidos para UTC em ambos os lados.
  A origem usava formato ISO 8601 com timezone (`-03:00`).
  O destino usava formato sem timezone. Sem normalização,
  comparações de data seriam inválidas.

### 1.3 Duplicatas Verdadeiras na Origem
Linhas completamente idênticas foram descartadas antes de
qualquer processamento. O enunciado avisa que a fila pode
entregar o mesmo evento mais de uma vez. Critério:
todas as colunas iguais → drop de uma cópia.

### 1.4 Reconstrução do Estado Atual
Para determinar o estado atual de cada pedido a partir do log:
1. Ordenação por `id_pedido` e `atualizado_em`
2. Seleção do evento mais recente (`keep='last'`)

O campo `atualizado_em` representa o momento do evento
no sistema de origem — não a ordem de chegada na fila.
Ordenar por ele é a única forma válida de reconstruir
a linha do tempo real.

### 1.5 Pedidos com Operação D como Último Evento
Pedidos cujo evento mais recente é uma exclusão (`D`)
não existem mais na origem e não devem aparecer no destino.
Se aparecem, são classificados como `PEDIDO_DELETADO_PRESENTE`.

### 1.6 Duplicatas no Destino
O destino continha 4 `id_pedido` repetidos.
- Duplicatas idênticas: removidas por `drop_duplicates()`
- Duplicatas com campos diferentes: a linha que bate com
  o status da origem foi mantida. A outra foi descartada.
  Fundamento: a origem é a fonte da verdade.

---

## 2. Casos Sem Resposta Única

### 2.1 Conflito de Timestamp (INDETERMINADO)
Três pedidos (10054, 10105, 10149) possuem dois eventos
com o mesmo `atualizado_em` mas campos diferentes.
Não é possível determinar qual chegou depois — o timestamp
não resolve o desempate e a ordem de chegada na fila
não está registrada.

Os pedidos 10054 e 10105 aparecem no relatório com
tipo_divergencia STATUS_DIVERGENTE|VALOR_DIVERGENTE e
observacao INDETERMINADO — sinalizando que além da
divergência com o destino, o próprio estado da origem
é incerto. O pedido 10149 não tinha divergência de campo
mas foi reportado explicitamente como ESTADO_INDETERMINADO.

**Decisão:** esses pedidos foram marcados com
`observacao = INDETERMINADO` no relatório. Não foram
excluídos nem corrigidos arbitrariamente. A resolução
exige investigação manual ou acesso aos logs da fila.

**Impacto:** se esses pedidos aparecerem no relatório
de divergências, o campo `observacao` sinaliza que o
próprio estado reconstruído da origem é incerto.

### 2.2 Operação I Após D (AMBIGUIDADE)
Três pedidos (10011, 10029, 10126) foram excluídos
(`D`) e depois tiveram um novo evento de criação (`I`)
com o mesmo `id_pedido`.

Duas hipóteses igualmente plausíveis:
- O mesmo pedido foi deletado por engano e recriado
- O sistema reutilizou um `id_pedido` após exclusão,
  criando um pedido diferente com o mesmo identificador

**Decisão:** o evento mais recente foi tratado como
verdade — esses pedidos existem e devem estar no destino.
Foram marcados com `observacao = AMBIGUIDADE` para
sinalizar que o histórico pré-deleção é ambíguo.

**Por que não ignorar:** ignorar seria pior.
Se o pedido existe na origem com evento recente,
não reportá-lo no destino seria um falso negativo.

### 2.3 Valor Ausente na Origem
Três pedidos (10064, 10098, 10119) existem nos dois
lados mas a origem não tem `valor_total` (NaN).
O destino registrou zero para esses pedidos.

Não é possível afirmar que zero é errado — pode ser
um pedido de valor real zero, ou pode ser o valor
padrão que o sistema colocou na ausência de dado.

**Decisão:** classificados como `VALOR_AUSENTE_NA_ORIGEM`
e excluídos do cálculo de impacto financeiro.
Reportar R$ 0,00 como divergência seria um falso positivo.

---

## 3. Premissas Assumidas

- O campo `atualizado_em` reflete o momento real do evento
  no sistema de origem, não a ordem de chegada no log.
- `id_pedido` é um identificador de negócio único por pedido.
  Casos de reuso após deleção são tratados como anomalia,
  não como comportamento esperado.
- O destino deveria conter exatamente um registro por pedido
  ativo na origem, com o estado mais recente.
- Diferenças de capitalização e espaços no status são erros
  de qualidade de dados, não valores semanticamente diferentes.

---

## 4. Limitações

- **Volume:** o script carrega os dois arquivos inteiros
  em memória. Com volume 1000x maior (474.000 linhas),
  seria necessário processamento em chunks ou migração
  para um banco de dados real.
- **Conflitos de timestamp:** os 3 casos INDETERMINADOS
  não têm resolução automática possível com os dados
  disponíveis. Exigem intervenção manual ou fonte adicional.
- **Reuso de ID:** o script não consegue distinguir
  se um I após D é o mesmo pedido recriado ou um pedido
  diferente com ID reutilizado. Ambos os cenários
  produzem o mesmo padrão no log.
- **Valor ausente:** os 3 pedidos com NaN na origem
  não entram no cálculo financeiro. O impacto real
  pode ser maior do que R$ 909,69 reportados.
- **Sem testes automatizados:** o script foi validado
  manualmente pelos outputs intermediários. Em produção,
  seria necessária uma suite de testes unitários para
  cada regra de negócio implementada.

---

## 5. Uso de Inteligência Artificial

Utilizei o **Claude (Anthropic)** como Tech Lead e mentor
durante o desenvolvimento deste case.

**Como foi usado:**
- Debate de arquitetura antes de escrever qualquer código
- Identificação de casos ambíguos nos dados
  (conflito de timestamp, I após D, reuso de ID)
- Geração de código Python
- Revisão de decisões técnicas e apontamento de edge cases
- Geração dos documentos RESUMO.md e DECISOES.md

**O que foi meu:**
- Defini que duplicata verdadeira exige todos os campos
  idênticos — não apenas o id_pedido. Isso veio da minha
  percepção de que dois eventos com o mesmo id mas campos
  diferentes são um conflito, não uma repetição.
- Questionei o significado do campo `D` — se era um status
  de negócio ou uma operação de exclusão. Essa distinção
  foi fundamental para classificar corretamente os pedidos
  deletados presentes no destino.
- Levantei a hipótese de reuso de id_pedido após deleção,
  antes de qualquer análise dos dados. Os dados confirmaram
  essa hipótese com os pedidos 10011, 10029 e 10126.
- Decidi que pedidos com I após D devem ser tratados como
  verdadeiros, marcando ambiguidade em vez de descartar.
- Defini a priorização de resolução por impacto no negócio:
  conflitos que afetam faturamento e pedidos cancelados
  têm prioridade sobre inconsistências de status.
- Decidi não inventar valores quando a origem não tem dado —
  os 3 pedidos com NaN foram classificados separadamente
  em vez de usar o valor do destino como referência.
- Escolhi a arquitetura ETL com separação por responsabilidade,
  e decidi usar funções em vez de classes para esse contexto,
  reconhecendo que o padrão Java não se aplica aqui.
- Defini todos os tipos de divergência e seus nomes antes
  de escrever o compare.py.
- Validei cada output intermediário e identifiquei os
  problemas que apareceram — nan na soma financeira,
  STATUS_DIVERGENTE sumindo após edição, filtro
  capturando VALOR_AUSENTE indevidamente.

O código gerado foi revisado, testado e validado.
Nenhuma linha foi aceita sem compreensão do que faz.