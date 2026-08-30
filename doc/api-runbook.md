# Como executar e testar a API

Este guia mostra como instalar as dependências, iniciar a API localmente e
testar os endpoints usando o `uv`.

## Pré-requisitos

- Python 3.13 ou superior.
- `uv` instalado e disponível no terminal.

Para confirmar a instalação do `uv`, execute:

```powershell
uv --version
```

## Instalar as dependências

No terminal, acesse a raiz do projeto e sincronize o ambiente:

```powershell
uv sync --no-install-project
```

O comando cria o ambiente virtual `.venv`, caso ele ainda não exista, e instala
as dependências definidas no `pyproject.toml` e no `uv.lock`. A opção
`--no-install-project` é necessária porque o nome de pacote configurado no
projeto ainda não corresponde ao diretório Python `churn_prediction`.

Não é necessário ativar o ambiente virtual para usar os comandos com `uv run`.

## Iniciar a API

Na raiz do projeto, execute:

```powershell
uv run --no-sync uvicorn telco_churn_prediction.api.main:app --app-dir src --reload
```

O parâmetro `--app-dir src` adiciona o diretório `src/` ao caminho de imports. O
parâmetro `--reload` reinicia o servidor automaticamente quando o código muda e
deve ser usado somente durante o desenvolvimento. A opção `--no-sync` evita
que o `uv` tente instalar o pacote do projeto antes de iniciar o servidor.

Quando o servidor estiver pronto, acesse:

- Documentação Swagger: `http://127.0.0.1:8000/docs`.
- Verificação de saúde: `http://127.0.0.1:8000/health`.

Para encerrar o servidor, pressione `Ctrl+C` no terminal.

## Verificar a API

Abra `http://127.0.0.1:8000/health` ou execute:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

A resposta esperada é:

```json
{
  "status": "ok"
}
```

O endpoint confirma que a aplicação está em execução. Ele não confirma se o
arquivo do modelo está disponível.

## Testar uma previsão

Como as features finais ainda não foram definidas, o endpoint recebe um objeto
genérico chamado `features`.

Use a interface Swagger:

1. Abra o endpoint **POST /predict**.
2. Selecione **Try it out**.
3. Informe as features esperadas pelo modelo carregado.
4. Selecione **Execute**.

Exemplo da estrutura do payload:

```json
{
  "features": {
    "nome_da_feature": "valor_da_feature"
  }
}
```

O exemplo representa apenas o formato da requisição. Substitua os campos
internos pelas mesmas features e tipos usados para treinar o pipeline.

Quando o modelo implementa `predict_proba`, a resposta contém a classe prevista
e sua probabilidade. Caso contrário, `probability` será `null`:

```json
{
  "prediction": 1,
  "probability": 0.82
}
```

## Disponibilizar o modelo

Por padrão, a API procura o artefato neste caminho:

```text
models/baseline_logistic_regression_pipeline.joblib
```

O arquivo deve conter o pipeline completo, incluindo o pré-processamento e o
estimador treinado. Enquanto o arquivo não existir, `POST /predict` retornará o
status HTTP `503` com a mensagem `Prediction model is unavailable.`.

## Executar sem recarregamento automático

Para uma execução local sem o modo de desenvolvimento, remova `--reload`:

```powershell
uv run --no-sync uvicorn telco_churn_prediction.api.main:app --app-dir src
```
