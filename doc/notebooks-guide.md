# Guia para executar os notebooks

Este guia descreve como preparar o ambiente, iniciar o Jupyter e executar os
notebooks do projeto na ordem recomendada.

## Pré-requisitos

Antes de começar, confirme os seguintes requisitos:

- Python 3.13 ou superior.
- `uv` instalado e disponível no terminal.
- Arquivo `data/Telco_customer_churn.xlsx` disponível.
- Terminal aberto na raiz do projeto.

Verifique as versões instaladas:

```powershell
python --version
uv --version
```

## Instalar o ambiente

Na raiz do projeto, instale as dependências e o grupo de desenvolvimento:

```powershell
uv sync --group dev
```

O comando cria ou atualiza o ambiente `.venv` e instala Jupyter, pandas,
scikit-learn, openpyxl e as demais dependências do projeto.

## Iniciar o Jupyter Lab

Os notebooks importam módulos localizados em `src` e usam caminhos relativos
ao diretório `notebooks`. Configure essas duas condições antes de iniciar o
Jupyter:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
uv run jupyter lab --ServerApp.root_dir=notebooks
```

Quando o navegador abrir, selecione o kernel do ambiente do projeto. O nome
normalmente aparece como `telco-churn-prediction` ou `.venv`.

Para encerrar o Jupyter, pressione `Ctrl+C` no terminal.

## Conhecer os notebooks

Execute os notebooks conforme o objetivo de cada etapa:

| Ordem | Notebook | Entrada principal | Saída principal |
|---:|---|---|---|
| 1 | [`exploratory_data_analysis.ipynb`](../notebooks/exploratory_data_analysis.ipynb) | `data/Telco_customer_churn.xlsx` | CSV preparado e figuras da análise |
| 2 | [`baseline_model.ipynb`](../notebooks/baseline_model.ipynb) | CSV preparado | Modelo baseline em `models/` |
| 3 | [`model_comparison.ipynb`](../notebooks/model_comparison.ipynb) | CSV preparado | Comparação de modelos e registro de métricas |
| 4 | [`champion_model_training.ipynb`](../notebooks/champion_model_training.ipynb) | CSV preparado | Modelo champion e registro de métricas |

### 1. Executar a análise exploratória

Abra `exploratory_data_analysis.ipynb` e execute **Run All**.

O notebook:

- carrega `data/Telco_customer_churn.xlsx`;
- analisa qualidade, distribuição e relação das variáveis com churn;
- remove e transforma as colunas definidas durante a análise;
- salva `data/telco_customer_churn_preprocessed.csv`;
- salva as visualizações no diretório `figures/`.

Execute essa etapa novamente quando o arquivo de origem mudar.

### 2. Treinar o modelo baseline

Abra `baseline_model.ipynb` e execute **Run All**.

O notebook usa o CSV preparado, treina uma regressão logística e salva:

```text
models/baseline_logistic_regression_pipeline.joblib
```

Esse artefato contém o pré-processamento e o classificador no mesmo pipeline.

### 3. Comparar os modelos

Abra `model_comparison.ipynb` e execute **Run All**.

O notebook compara regressão logística, random forest e rede neural. Ele
registra métricas em:

```text
models/log_training_runs.jsonl
```

O notebook também pode salvar
`models/champion_logistic_regression_pipeline.joblib`. Execute o notebook de
treinamento champion depois da comparação para garantir que o artefato final
corresponda ao fluxo selecionado.

### 4. Treinar o modelo champion

Abra `champion_model_training.ipynb` e execute **Run All**.

Esse notebook usa as funções de `src/preprocessing.py`, `src/training.py` e
`src/utils.py`. Ao final, ele:

- calcula e exibe as métricas do modelo;
- adiciona uma execução a `models/log_training_runs.jsonl`;
- salva `models/champion_logistic_regression_pipeline.joblib`.

## Confirmar os resultados

Depois da execução completa, confirme os principais artefatos:

```powershell
Get-Item `
  .\data\telco_customer_churn_preprocessed.csv, `
  .\models\baseline_logistic_regression_pipeline.joblib, `
  .\models\champion_logistic_regression_pipeline.joblib, `
  .\models\log_training_runs.jsonl
```

## Evitar alterações acidentais

Antes de executar **Run All**, considere estes efeitos:

- A análise exploratória sobrescreve o CSV preparado.
- Os notebooks de treinamento sobrescrevem os arquivos `.joblib`.
- Cada avaliação adiciona uma linha ao arquivo `log_training_runs.jsonl`.
- A execução altera contadores, saídas e metadados do arquivo `.ipynb`.

Revise `git status` depois da execução:

```powershell
git status --short
```

## Solucionar problemas

### Erro `No module named preprocessing`

Encerre o Jupyter, volte para a raiz do projeto e configure `PYTHONPATH` antes
de iniciá-lo novamente:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
uv run jupyter lab --ServerApp.root_dir=notebooks
```

### Erro de arquivo não encontrado em `../data`

Inicie o Jupyter com `notebooks` como diretório raiz. Os notebooks foram
escritos considerando esse diretório de trabalho.

### Erro ao abrir o arquivo Excel

Atualize o ambiente para garantir a instalação de `openpyxl`:

```powershell
uv sync --group dev
```

### Kernel diferente do ambiente do projeto

No Jupyter, abra **Kernel > Change Kernel** e selecione o interpretador da
pasta `.venv`.

