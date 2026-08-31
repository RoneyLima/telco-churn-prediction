# Telco Churn Prediction

Sistema end-to-end para predição de churn de clientes de telecom, com pipeline de pré-processamento, treinamento de modelo e API REST para inferência local.

## Visão geral

Este projeto trata de um problema de classificação binária supervisionada: prever se um cliente tem alta probabilidade de cancelar o serviço (`target = 1`) ou permanecer ativo (`target = 0`). O modelo final em produção é uma regressão logística com ajustes de classe para melhorar a capacidade de capturar churn em contexto de desbalanceamento.

A métrica principal do negócio está alinhada à decisão de retenção: priorizar o `recall` da classe positiva para reduzir falsos negativos, mantendo `precision` e `F1-score` como indicadores de eficiência operacional. O problema não é de regressão nem de previsão contínua; a saída esperada é uma probabilidade de churn e uma classe prevista.

## Estrutura do projeto

- `data/`: conjunto pré-processado e dados de origem.
- `models/`: artefatos serializados do pipeline treinado.
- `src/`: código modular do pipeline, API e utilitários.
- `tests/`: testes automatizados para pré-processamento e API.
- `doc/`: documentação de negócio, dicionário de dados e runbook.

## Pré-requisitos

- Python 3.13+
- `pip` e `venv` disponíveis no ambiente
- Git para clone do repositório
- Opcional: `uv` para gerenciar o ambiente de forma mais rápida

### Verificação rápida

```powershell
python --version
pip --version
```

## Instalação de dependências

A partir da raiz do projeto, execute os passos abaixo.

### Opção 1: ambiente virtual com `venv` + `requirements.txt`

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Opção 2: ambiente com `uv` (recomendado)

```powershell
uv sync --group dev
```

Esse comando instala as dependências declaradas em `pyproject.toml`, incluindo as bibliotecas de execução e testes do projeto.

## Validar a instalação

```powershell
pytest -q
```

Ou, se estiver usando `uv`:

```powershell
uv run pytest -q
```

## Execução da API localmente

A API FastAPI do projeto pode ser iniciada com o comando abaixo na raiz do repositório:

```powershell
uvicorn telco_churn_prediction.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Se estiver usando o ambiente virtual criado via `venv`, o comando acima funciona normalmente após ativar o ambiente. Se estiver usando `uv`, a execução equivalente é:

```powershell
uv run uvicorn telco_churn_prediction.api.main:app --host 127.0.0.1 --port 8000 --reload
```

### Endpoints disponíveis

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Predição: POST http://127.0.0.1:8000/predict

## Exemplo de chamada para o endpoint `/predict`

### JSON de teste

```json
{
  "customer_id": "6176-YJWAS",
  "tenure_months": 24,
  "monthly_charges": 65.0,
  "total_charges": 1580.0,
  "cltv": 2400,
  "gender": "Female",
  "senior_citizen": "No",
  "partner": "Yes",
  "dependents": "No",
  "phone_service": "Yes",
  "multiple_lines": "No",
  "internet_service": "Fiber optic",
  "online_security": "Yes",
  "online_backup": "No",
  "device_protection": "Yes",
  "tech_support": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "No",
  "contract": "Month-to-month",
  "paperless_billing": "Yes",
  "payment_method": "Bank transfer (automatic)"
}
```

### Requisição com `curl`

```powershell
curl -X POST "http://127.0.0.1:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "customer_id": "6176-YJWAS",
    "tenure_months": 24,
    "monthly_charges": 65.0,
    "total_charges": 1580.0,
    "cltv": 2400,
    "gender": "Female",
    "senior_citizen": "No",
    "partner": "Yes",
    "dependents": "No",
    "phone_service": "Yes",
    "multiple_lines": "No",
    "internet_service": "Fiber optic",
    "online_security": "Yes",
    "online_backup": "No",
    "device_protection": "Yes",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "No",
    "contract": "Month-to-month",
    "paperless_billing": "Yes",
    "payment_method": "Bank transfer (automatic)"
  }'
```

### Resposta esperada

```json
{
  "customer_id": "6176-YJWAS",
  "churn_predict": {
    "prediction": 0,
    "probability": 0.75
  }
}
```

> A resposta exata pode variar conforme o modelo carregado e o limiar operacional configurado, mas o formato da resposta deve seguir esse contrato.

## Verificar saúde da API

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "loaded_model": true
}
```

## Documentação complementar

- [doc/entendimento-do-negocio.md](doc/entendimento-do-negocio.md): contexto de negócio, métricas e premissas.
- [doc/model-card.md](doc/model-card.md): resumo de performance, limitações e vieses do modelo.
- [doc/api-runbook.md](doc/api-runbook.md): passos operacionais para uso da API.

## Observações operacionais

- O modelo foi treinado para apoio à decisão de retenção, não para ação automática sem validação do time de negócio.
- O limiar de classificação deve ser ajustado por custo de campanha, capacidade operacional e margem esperada de retenção.
- A frequência de inferência deve seguir a cadência de campanhas e não a taxa de uma operação em tempo real de alta escala.
