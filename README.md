# Reconciliação de Pedidos

Pipeline de reconciliação entre o sistema transacional (origem)
e a tabela analítica (destino), desenvolvido como case técnico
para a posição de Engenheiro de Dados.

---

## Pré-requisitos

- Python 3.8+
- pip

---

## Como Rodar

**1. Clone o repositório**
```bash
git clone https://github.com/AyrtonCarvalh0/DataCase.git
cd DataCase
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Adicione os arquivos de dados**

Coloque os arquivos na raiz do projeto:
- `pedidos_origem.csv`
- `pedidos_destino.csv`

> Os arquivos CSV de entrada não estão versionados
> por conterem dados sensíveis.

**5. Execute**
```bash
python main.py
```

---

## Estrutura do Projeto

DataCase/

├── extract.py # Carregamento dos CSVs

├── transform.py # Normalização e reconstrução do estado

├── compare.py # Comparação e classificação de divergências

├── main.py # Orquestrador do pipeline

├── relatorio_divergencias.csv # Relatório gerado automaticamente

├── RESUMO.md # Resumo executivo para o gerente comercial

└── DECISOES.md # Decisões técnicas e casos ambíguos

---

## Resultado

O script gera automaticamente o `relatorio_divergencias.csv`
com todas as divergências encontradas entre os dois sistemas.

Para a análise completa dos resultados e das decisões tomadas,
consulte o `RESUMO.md` e o `DECISOES.md`.

