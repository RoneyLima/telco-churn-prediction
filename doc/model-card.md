# Model Card — Telco Churn Prediction

## 1. Visão Geral & Descrição do Modelo

- Projeto: Telco Churn Prediction
- Versão do modelo: 1.0
- Tipo de problema: classificação binária supervisionada
- Algoritmo final: Regressão Logística (`LogisticRegression`) com `class_weight="balanced"`
- Objetivo: priorizar clientes com maior risco de churn para campanhas de retenção e acompanhamento comercial
- Output: probabilidade de churn e classe prevista (`0` = não churn, `1` = churn)

### Dados de treino e teste

- Base utilizada: `data/telco_customer_churn_preprocessed.csv`
- Volume total: 7.043 registros
- Variáveis explicativas: perfil do cliente, serviços contratados, contrato, pagamento, faturamento e CLTV
- Target: `target`
- Distribuição do alvo: 26,54% churn e 73,46% não churn
- Divisão utilizada: 80/20 para treino e teste, com `random_state=7` no pipeline de preparação dos dados
- Pré-processamento: padronização de variáveis numéricas e encoding categórico via `OneHotEncoder`, com pipeline do scikit-learn

### Contexto operacional

Este modelo deve ser usado como apoio à decisão de retenção, não como automatização de contato ou desconto. O score orienta a fila da operação, mas a ação final deve respeitar elegibilidade do cliente, capacidade da campanha, consentimento e regra comercial da empresa.

## 2. Métricas de Performance

A comparação abaixo foi construída com base nos resultados reportados no notebook de comparação do projeto. Como o problema é de classificação binária com foco em priorização de risco, a métrica principal usada para ordenação foi `Average Precision (AP)`; `ROC-AUC` não foi publicado nesta versão do projeto.

| Métrica | Baseline (Regressão Logística) | Modelo final (Champion) | Observação |
|---|---:|---:|---|
| Acurácia | 0.7591 | 0.7708 | Melhor desempenho no modelo final |
| Precision | 0.5303 | 0.5447 | Mantém foco em reduzir contatos desnecessários |
| Recall | 0.8187 | 0.8316 | Maior ganho do modelo final; prioriza detecção de churn |
| F1-Score | 0.6435 | 0.6582 | Equilíbrio entre precisão e recall |
| Average Precision (AP) | 0.6786 | 0.7189 | Melhor ranking de probabilidade de risco |
| MAE / RMSE | Não aplicável | Não aplicável | Problema é de classificação, não de regressão |

### Interpretação

O modelo final supera o baseline principalmente no recall e na capacidade de ranking de risco. Isso é coerente com o uso de negócio: para retenção, o custo de perder clientes em risco costuma ser maior do que a carga extra de contato em clientes de menor chance de churn.

## 3. Possíveis Vieses (Biases)

### Desbalanceamento de classes

- A proporção de churn é menor do que a de não churn (26,54% vs 73,46%).
- Em cenários de alta assimetria, o modelo pode priorizar a classe majoritária se a regra de decisão não for calibrada corretamente.
- Por isso, o projeto usa `class_weight="balanced"` e enfatiza recall e AP como métricas operacionais relevantes.

### Vieses de variáveis e comportamento

- Atributos como `gender`, `contract`, `payment_method` e `cltv` podem refletir padrões históricos de clientes, mas não necessariamente causalidade.
- Clientes com histórico mais curto, menor estabilidade ou comportamento atípico podem receber score mais alto ou mais baixo por efeito de perfil, não necessariamente por risco causal.
- Se a política de retenção priorizar grupos específicos com maior facilidade de conversão, isso pode criar viés operacional mesmo quando o modelo seja tecnicamente estável.

### Risco de discriminação sistemática

- O modelo não deve ser usado para excluir ou tratar grupos demográficos de forma automática.
- Qualquer ação comercial deve considerar regras de elegibilidade, faixa de contato, permissões e políticas internas para evitar discriminação indireta.

## 4. Limitações & Casos de Falha

### Cenários em que o modelo não performa bem

- Dados fora de distribuição: mudança na composição dos clientes, novas ofertas, novos contratos ou mudanças de tarifa podem reduzir a qualidade do score.
- Cold start: clientes novos ou com pouco histórico temporal podem ter sinais pouco representativos para o modelo.
- Alteração temporal no comportamento: mudanças de mercado, concorrência, políticas de cobrança ou percepção de qualidade podem mudar abruptamente a relação entre variáveis e churn.
- Ambiguidade de label: se a definição operacional de churn mudar no tempo, os rótulos anteriores podem não refletir a nova regra de negócio.
- Ausência de contexto operacional: o score sozinho não considera custo de incentivo, margem, capacidade de atendimento e efetividade da campanha.

### Limitações metodológicas

- O modelo é interpretado como preditivo, não causal.
- Não há garantia de que uma variável alta ou baixa em score seja a causa do churn.
- O conjunto de dados representa um período específico e a generalização para outros mercados ou regiões precisa ser validada.

## 5. Riscos de Uso & Recomendação

- Usar o score como priorização e apoio à decisão, e não como decisão final de contato ou cobrança.
- Ajustar o limiar de classificação conforme custo da campanha e capacidade operacional.
- Monitorar drift de dados, mudança de distribuição e queda de recall ao longo do tempo.
- Revalidar o modelo em ciclos periódicos sempre que houver nova campanha, mudança de contrato ou alteração do comportamento de clientes.

## 6. Resumo Executivo

O modelo final é uma Regressão Logística com balanceamento de classe, escolhida por apresentar melhor recall e melhor capacidade de priorização de clientes em risco de churn. O desempenho é suficiente para apoiar campanhas de retenção em contexto acadêmico/operacional inicial, mas exige monitoramento contínuo, revisão do limiar e validação de mercado antes de uso mais amplo e automatizado.
