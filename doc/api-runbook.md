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

O comando cria o ambiente virtual `.venv`, caso ele ainda não exista, instala
as dependências e registra o pacote `telco_churn_prediction`.

Não é necessário ativar o ambiente virtual para usar os comandos com `uv run`.

## Iniciar a API

Na raiz do projeto, execute:

```powershell
uv run uvicorn telco_churn_prediction.api.main:app --reload
```

O parâmetro `--reload` reinicia o servidor automaticamente quando o código muda
e deve ser usado somente durante o desenvolvimento.

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

O endpoint retorna `503` e informa `loaded_model: false` quando o artefato do
modelo não está disponível.

## Testar uma previsão

Use a interface Swagger para enviar os atributos definidos pelo contrato:

1. Abra o endpoint **POST /predict**.
2. Selecione **Try it out**.
3. Informe os atributos do cliente.
4. Selecione **Execute**.

Para testar pelo PowerShell com o payload versionado no projeto, execute:

```powershell
$body = Get-Content tests/fixtures/prediction-payload.json -Raw
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/predict `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

O endpoint retorna a classe prevista e sua probabilidade:

```json
{
  "customer_id": "6176-YJWAS",
  "churn_predict": {
    "prediction": 0,
    "probability": 0.75
  }
}
```

## Disponibilizar o modelo

Por padrão, a API usa o artefato neste caminho:

```text
models/baseline_logistic_regression_pipeline.joblib
```

O arquivo deve conter o pipeline completo, incluindo o pré-processamento e o estimador treinado. Enquanto o arquivo não existir, `POST /predict` retornará o status HTTP `503` com a mensagem `Prediction model is unavailable.`.

## Executar sem recarregamento automático

Para uma execução local sem o modo de desenvolvimento, remova `--reload`:

```powershell
uv run uvicorn telco_churn_prediction.api.main:app
```
