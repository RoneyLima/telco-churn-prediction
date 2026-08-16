- **`Project Name`:** Predição e Prevenção de Churn Telco (Telco Churn Prediction)
        
- **`Business Problem`:** Perda acelerada de clientes da base ativa, gerando queda direta na receita recorrente da operadora. A diretoria necessita identificar clientes em risco com antecedência para permitir ações proativas e direcionadas da equipe de retenção.
        
- **`Machine Learning Task`:** Classificação binária supervisionada (Prever risco de cancelamento: $1 = \text{Churn}$, $0 = \text{Não-Churn}$).
        
- **`Success Metrics`:**

    - _Negócio:_ Redução da taxa de churn mensal da operadora e aumento da taxa de conversão nas campanhas de retenção direcionadas.
                
    - _Técnicas (ML):_ Recall/Sensibilidade elevado na classe positiva (minimizar falsos negativos para não perder clientes em risco), aliado a ROC-AUC/PR-AUC robusto e F1-Score equilibrado para manter a precisão das ofertas.
        
- **`Data Sources`:** Base histórica cadastral, contratual e de faturamento de clientes (IBM Telco Customer Churn dataset / CRM da operadora).
    
- **`Features`:** N/A _(conforme solicitado)_
        
- **`Target`:** `Churn Value` ($1$ para cancelamento, $0$ para retenção) ou `Churn Label` (`Yes` / `No`).
       
- **`Constraints`:**
   
    - Modelo principal obrigatoriamente implementado como Perceptron Multicamadas (MLP) utilizando PyTorch.
        
    - Comparação obrigatória de performance contra modelos baseline implementados via Scikit-Learn.
        
    - Rastreamento de métricas, parâmetros e versionamento de artefatos centralizado via MLflow.
                
    - Entrega final do modelo empacotado e servido operacionalmente via API REST.
        
- **`Risks`:**
          
    - _Vazamento de dados (Data Leakage):_ Risco de inclusão de variáveis calculadas a posteriori ou decorrentes do cancelamento (`Churn Reason`, `Churn Category`, `Churn Score`).
        
    - _Desbalanceamento de classes:_ Risco de viés do modelo para a classe majoritária (não-churn), prejudicando a identificação dos clientes em risco real.
        
    - _Degradação temporal (Concept Drift):_ Mudança no comportamento de consumo ou novas ações da concorrência tornando o modelo obsoleto sem rotina de retreinamento.
        
    - _Custo operacional de erros:_ Falsos negativos geram perda irreversível de clientes; falsos positivos desperdiçam orçamento em ofertas desnecessárias.