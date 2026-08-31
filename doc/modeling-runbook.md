# Runbook dos códigos de modelagem

Este runbook descreve como executar o fluxo de modelagem implementado em
`src`.

## Localização do código

Nesta revisão do projeto, o código de modelagem não está em uma pasta física
`src/modeling`. Ele está dividido nestes módulos:

| Arquivo | Responsabilidade |
|---|---|
| [`src/preprocessing.py`](../src/preprocessing.py) | Carregar e dividir dados, criar features e montar o pipeline de pré-processamento |
| [`src/training.py`](../src/training.py) | Treinar, avaliar e salvar o pipeline |
| [`src/utils.py`](../src/utils.py) | Registrar as métricas dos experimentos em JSON Lines |

Os arquivos podem ser organizados em um pacote `modeling` no futuro. Até essa
migração acontecer, use os imports documentados neste runbook.

## Pré-requisitos

Confirme os seguintes requisitos:

- Python 3.13 ou superior.
- `uv` instalado.
- `data/telco_customer_churn_preprocessed.csv` disponível.
- Terminal aberto na raiz do projeto.

Se o CSV preparado ainda não existir, execute primeiro o notebook de análise
exploratória conforme o
[`Guia para executar os notebooks`](notebooks-guide.md).

## Preparar o ambiente

Instale as dependências:

```powershell
uv sync --group dev
```

Adicione `src` ao caminho de imports da sessão atual do PowerShell:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
```

Confirme que os módulos podem ser importados:

```powershell
uv run python -c "import preprocessing, training, utils; print('Imports OK')"
```

## Executar o treinamento completo

O projeto ainda não possui um comando de terminal específico para o fluxo de
modelagem. Execute as funções de `src` com o script abaixo, a partir da raiz do
projeto:

```powershell
@'
from pathlib import Path

from sklearn.linear_model import LogisticRegression

from preprocessing import (
    assemble_full_pipeline,
    create_preprocessing_pipeline,
    load_and_split_data,
)
from training import evaluate_model, save_artifact, train_model

DATA_PATH = Path("data/telco_customer_churn_preprocessed.csv")
LOG_PATH = Path("models/log_training_runs.jsonl")
MODEL_PATH = Path("models/champion_logistic_regression_pipeline.joblib")

TARGET_COLUMN = "target"
NUMERIC_FEATURES = [
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "cltv",
]
CATEGORICAL_FEATURES = [
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "phone_service",
    "multiple_lines",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
]

x_train, x_test, y_train, y_test = load_and_split_data(
    DATA_PATH,
    TARGET_COLUMN,
    random_state=7,
    stratify=True,
)

preprocessor = create_preprocessing_pipeline(
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)
model = LogisticRegression(random_state=7, class_weight="balanced")
pipeline = assemble_full_pipeline(preprocessor, model)
trained_pipeline = train_model(pipeline, x_train, y_train)

evaluate_model(
    "logistic_regression_champion",
    trained_pipeline,
    x_test,
    y_test,
    str(LOG_PATH),
)
save_artifact(trained_pipeline, str(MODEL_PATH))
'@ | uv run python -
```

## Entender as etapas

O fluxo executa estas etapas, na ordem:

1. Carrega o CSV preparado.
2. Separa features e alvo.
3. Divide os dados em treino e teste com estratificação.
4. Cria features numéricas adicionais.
5. Padroniza as variáveis numéricas.
6. Aplica one-hot encoding às variáveis categóricas.
7. Treina a regressão logística com classes balanceadas.
8. Calcula average precision, precision, recall, accuracy e F1-score.
9. Registra as métricas e salva o pipeline completo.

## Arquivos gerados

O treinamento cria ou altera estes arquivos:

```text
models/champion_logistic_regression_pipeline.joblib
models/log_training_runs.jsonl
```

O arquivo `.joblib` contém as transformações e o classificador treinado. A API
pode carregar esse tipo de artefato sem repetir manualmente o
pré-processamento.

## Validar o artefato

Confirme que o pipeline salvo pode ser carregado:

```powershell
uv run python -c "import joblib; model = joblib.load('models/champion_logistic_regression_pipeline.joblib'); print(type(model).__name__)"
```

A saída esperada é:

```text
Pipeline
```

Mantenha `PYTHONPATH` configurado durante o carregamento. O artefato champion
referencia a função de engenharia de features de `src/preprocessing.py`.

## Executar verificações

Execute a suíte do projeto com:

```powershell
uv run pytest -q
```

Na revisão atual, `tests/test_preprocessing.py` importa
`telco_churn_prediction.data.preprocessing`, mas esse pacote não existe na
árvore de código. Se ocorrer `ModuleNotFoundError`, alinhe o import do teste com
`src/preprocessing.py` antes de considerar a suíte válida. Esse erro não indica
falha na instalação das dependências.

## Solucionar problemas

### Erro `No module named preprocessing`

Configure `PYTHONPATH` na mesma sessão em que executará o treinamento:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
```

### Erro `Target column not found`

Confirme que o CSV contém a coluna `target`:

```powershell
uv run python -c "import pandas as pd; print(pd.read_csv('data/telco_customer_churn_preprocessed.csv').columns.tolist())"
```

### Erro ao carregar o arquivo `.joblib`

Use a mesma versão de Python e das dependências empregada no treinamento:

```powershell
uv sync --group dev
```

Depois, configure `PYTHONPATH` e tente carregar o artefato novamente.

### Métricas duplicadas no log

Cada execução adiciona uma linha a `models/log_training_runs.jsonl`. Remova
manualmente apenas as execuções que você tem certeza de que são duplicadas.

## Checklist operacional

Antes de concluir o treinamento, confirme:

- O CSV preparado possui a coluna `target`.
- A divisão usa `random_state=7` e `stratify=True`.
- O classificador usa `class_weight="balanced"`.
- As métricas foram registradas no arquivo JSON Lines.
- O modelo foi salvo no caminho esperado.
- O artefato salvo pode ser carregado com `joblib`.
- `git status --short` mostra apenas alterações esperadas.

