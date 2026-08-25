# Como executar e testar a API

Este guia mostra o caminho mais curto para iniciar a API localmente e testar
uma previsão de churn.

## Pré-requisitos

- Python 3.13 ou superior.
- `pip`, que já vem com as instalações atuais do Python.

## Iniciar a API

No terminal integrado do VS Code, na raiz do projeto, execute os passos a
seguir.

1. Crie o ambiente virtual:

   ```powershell
   python -m venv .venv
   ```

2. Ative o ambiente virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```powershell
   python -m uvicorn api.main:app --app-dir src --reload
   ```

O modelo é carregado quando a API inicia. Quando o terminal mostrar que o
servidor está em execução, abra `http://127.0.0.1:8000/docs` no navegador.


## Testar uma previsão

Use a página aberta em `/docs`, que é a interface do Swagger do FastAPI.

1. Abra o endpoint **POST /predict**.
2. Clique em **Try it out**.
3. Substitua o corpo de exemplo pelo payload abaixo.
4. Clique em **Execute**.

```json
{
  "customer_id": "6176-YJWAS",
  "tenure_months": 72,
  "monthly_charges": 97.95,
  "total_charges": 7114.25,
  "cltv": 4256,
  "gender": "Male",
  "senior_citizen": "No",
  "partner": "Yes",
  "dependents": "No",
  "phone_service": "Yes",
  "multiple_lines": "Yes",
  "internet_service": "Fiber optic",
  "online_security": "Yes",
  "online_backup": "Yes",
  "device_protection": "Yes",
  "tech_support": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "No",
  "contract": "Two year",
  "paperless_billing": "Yes",
  "payment_method": "Credit card (automatic)"
}
```

A resposta contém o identificador do cliente, a classe prevista e a
probabilidade de churn:

```json
{
  "customer_id": "6176-YJWAS",
  "churn_predict": {
    "prediction": 0,
    "probability": 0.0159
  }
}
```

## Verificar a API

Para confirmar somente se a API e o modelo estão disponíveis, abra
`http://127.0.0.1:8000/health`. A resposta esperada contém
`"status": "healthy"` e `"loaded_model": true`.

