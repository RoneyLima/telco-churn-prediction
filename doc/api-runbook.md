# Como executar e testar a API

Este guia mostra como instalar as dependências, iniciar a API localmente e testar os endpoints usando o `uv`.

## Pré-requisitos

- Python 3.13 ou superior.
- `uv` instalado e disponível no terminal.
- Repositório clonado localmente.

Para confirmar a instalação do `uv`, execute:

```powershell
uv --version
```

## Instalar as dependências

No terminal, acesse a raiz do projeto e sincronize o ambiente:

```powershell
uv sync --group dev
```

Esse comando cria o ambiente virtual `.venv`, se necessário, e instala as dependências definidas em `pyproject.toml`.

## Iniciar a API

Na raiz do projeto, execute:

```powershell
uv run uvicorn telco_churn_prediction.api.main:app --host 127.0.0.1 --port 8000 --reload
```

O parâmetro `--reload` reinicia o servidor automaticamente quando o código muda e deve ser usado somente durante o desenvolvimento.

Quando o servidor estiver pronto, acesse:

- Documentação Swagger: http://127.0.0.1:8000/docs
- Verificação de saúde: http://127.0.0.1:8000/health
- Predição: http://127.0.0.1:8000/predict

Para encerrar o servidor, pressione `Ctrl+C` no terminal.

## Verificar a API

Abra http://127.0.0.1:8000/health ou execute:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

A resposta esperada é:

```json
{
  "status": "healthy",
  "loaded_model": true
}
```

Se o modelo não estiver carregado, a API responde com `503` e o status `unhealthy`.

## Testar uma previsão

Use o payload real do contrato da API conforme o modelo treinado:

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

Exemplo de chamada com `curl`:

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

Resposta esperada no formato da API:

```json
{
  "customer_id": "6176-YJWAS",
  "churn_predict": {
    "prediction": 0,
    "probability": 0.75
  }
}
```

A resposta exata pode variar conforme o modelo carregado e o limiar operacional configurado, mas a estrutura da resposta deve seguir esse contrato.

## Disponibilizar o modelo

Por padrão, a API usa o artefato neste caminho:

```text
models/baseline_logistic_regression_pipeline.joblib
```

O arquivo deve conter o pipeline completo, incluindo o pré-processamento e o estimador treinado. Enquanto o arquivo não existir, `POST /predict` retornará o status HTTP `503` com a mensagem `Prediction model is unavailable.`.

## Executar sem recarregamento automático

Para uma execução local sem o modo de desenvolvimento, remova `--reload`:

```powershell
uv run uvicorn telco_churn_prediction.api.main:app --host 127.0.0.1 --port 8000
```
