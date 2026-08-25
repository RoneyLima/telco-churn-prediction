# Entendimento do Negócio — Predição de Churn Telco

| Campo | Definição |
|---|---|
| Projeto | Telco Churn Prediction |
| Versão | 1.0 — rascunho para validação |
| Data | 25 de agosto de 2026 |
| Perspectiva | Gestão de Retenção e Experiência do Cliente da Telco |
| Metodologia | CRISP-DM, com práticas de qualidade e operação de ML |
| Status | Aguardando validação dos responsáveis de negócio, dados e privacidade |

## 1. Resumo executivo

A Telco enfrenta perda de clientes por cancelamento (*churn*), o que reduz receita recorrente, eleva o custo de aquisição para repor a base e pode sinalizar problemas de produto, preço, atendimento ou cobrança. Este projeto criará uma capacidade preditiva para identificar clientes com maior propensão a cancelar e apoiar ações de retenção mais oportunas e proporcionais ao valor do cliente.

O produto analítico não decide nem executa o contato com o cliente de forma autônoma. Ele entrega uma probabilidade de churn e uma classificação de risco para que as áreas de Retenção, CRM e Atendimento definam a melhor ação dentro das políticas comerciais e de privacidade. A decisão final deve sempre considerar elegibilidade da campanha, consentimento, histórico de contatos e custo do incentivo.

O escopo atende ao desafio acadêmico: análise exploratória, baseline de Regressão Logística, comparação com modelo de árvores/ensemble e MLPClassifier, seleção do modelo campeão e disponibilização de inferência em API FastAPI.

## 2. Objetivos de negócio

### 2.1 Problema a resolver

Hoje, o risco de cancelamento não está priorizado de forma consistente por cliente. Como consequência, campanhas de retenção podem chegar tarde, atingir pessoas sem risco relevante ou consumir incentivos em clientes que permaneceriam ativos sem intervenção. Precisamos transformar os dados de relacionamento em uma lista priorizada e explicável de clientes para retenção preventiva.

### 2.2 Objetivos priorizados

| Prioridade | Objetivo | Dono de negócio | Como será usado |
|---|---|---|---|
| Alta | Identificar clientes com maior risco de churn | Gerência de Retenção | Priorizar a fila de campanhas e contatos preventivos |
| Alta | Preservar receita e valor de vida de clientes elegíveis | Diretoria Comercial/CRM | Direcionar ofertas e acompanhamento conforme potencial de retenção |
| Alta | Reduzir desperdício de esforço e incentivos | Operações de Retenção | Concentrar contatos em perfis com maior benefício esperado |
| Média | Compreender fatores associados ao churn | Produto, Atendimento e Cobrança | Orientar melhorias estruturais além das campanhas |
| Média | Disponibilizar predição de forma reutilizável | Tecnologia e Analytics | Integrar consultas individuais à API `/predict` |

### 2.3 Critérios de sucesso de negócio

As metas abaixo são propostas iniciais. Elas devem ser calibradas com dados de campanhas, margem, custo de contato e taxa histórica de cancelamento antes de qualquer uso operacional.

| Critério | Métrica | Linha de base necessária | Meta inicial para validação |
|---|---|---|---|
| Alcance da retenção | % dos cancelamentos futuros presentes no grupo priorizado | Aferir no período de teste | Superar a seleção aleatória e a regra vigente |
| Eficiência de campanha | Conversão incremental de retenção no público tratado | Grupo de controle ou experimento A/B | Evidenciar ganho estatisticamente e economicamente relevante |
| Uso de incentivos | Custo por cliente retido incrementalmente | Custo por canal e por oferta | Menor que a margem/valor incremental preservado |
| Proteção de receita | Receita mensal ou CLTV preservado | Base pré-experimento | Resultado positivo após descontar custo da ação |
| Adoção | % da fila de retenção orientada por score | Processo atual | Definir após o piloto; acompanhamento semanal |

Não há série de custos, margem, campanhas ou resultados de intervenção no repositório. Portanto, este documento não declara economia, ROI ou redução de churn como resultado já obtido.

## 3. Recursos do projeto

### 3.1 Stakeholders

| Parte interessada | Responsabilidade e decisão |
|---|---|
| Patrocinador executivo (Diretoria Comercial) | Aprovar objetivo, orçamento e sucesso do piloto |
| Gerência de Retenção/CRM | Definir segmentos, ofertas, cadência de contato e capacidade operacional |
| Produto, Atendimento e Cobrança | Interpretar achados e tratar causas estruturais de churn |
| Ciência de Dados | Conduzir EDA, modelagem, validação e documentação de limitações |
| Engenharia de Dados/Software | Garantir qualidade dos dados, pipeline, API, testes e reprodutibilidade |
| Privacidade, Jurídico e Compliance | Validar finalidade, base legal, minimização, retenção e uso dos dados |
| Atendimento/Operações | Executar ações aprovadas e registrar resultado dos contatos |

### 3.2 Recursos Humanos

| Pessoa | Papel | Responsabilidades principais | Disponibilidade |
|---|---|---|---|
| Roney | Engenheiro de Software | Modularizar a solução, desenvolver e manter a API, integrar o modelo e garantir testes e reprodutibilidade do código. | A definir |
| João | Cientista de Dados | Conduzir EDA, preparar experimentos, treinar e avaliar modelos e documentar métricas, limitações e vieses. | A definir |
| Vinícius | Engenheiro de Dados | Assegurar ingestão, qualidade, transformação e disponibilidade dos dados e dos pipelines de dados. | A definir |

### 3.3 Dados & Tecnologia

#### Dados disponíveis

| Recurso | Localização | Conteúdo e volume | Uso no projeto | Observações |
|---|---|---|---|---|
| Base de origem | `data/Telco_customer_churn.xlsx` | Base tabular de clientes de telecomunicações. | Fonte para exploração, validação do esquema e geração de exemplos. | A origem, o período de referência e a definição operacional de churn precisam ser validados antes de uso produtivo. |
| Base pré-processada | `data/telco_customer_churn_preprocessed.csv` | 7.043 registros e 21 colunas: 20 atributos e o alvo `target`. | Treinamento e avaliação dos modelos. | Não há valores ausentes no arquivo processado. |
| Variável-alvo | Coluna `target` | 1.869 registros de churn (26,54%) e 5.174 de não churn (73,46%). | Classificação binária supervisionada e avaliação de desbalanceamento. | Usar divisão estratificada e métricas por classe; a estratégia de balanceamento deve ser comparada experimentalmente. |
| Atributos de negócio | Colunas de perfil, serviços, contrato, pagamento, cobrança e CLTV. | Incluem, por exemplo, `tenure_months`, `contract`, `payment_method`, `monthly_charges`, `total_charges` e `cltv`. | Compor as entradas do pipeline e da API de predição. | Avaliar atributos derivados, sobretudo CLTV, contra vazamento de informação temporal. |

#### Tecnologias disponíveis no repositório

| Categoria | Tecnologia | Finalidade |
|---|---|---|
| Linguagem e ambiente | Python 3.13, `pyproject.toml` e `uv.lock` | Ambiente reproduzível e gerenciamento de dependências. |
| Dados | Pandas e OpenPyXL | Leitura e transformação dos arquivos CSV e Excel. |
| Análise | Jupyter, Matplotlib e Seaborn | EDA, análise de qualidade e comunicação visual dos achados. |
| Machine Learning | Scikit-Learn e Joblib | Pipeline de pré-processamento, Regressão Logística, validação, comparação de modelos e persistência do artefato. |
| API | FastAPI, Pydantic e Uvicorn | Validação do payload, endpoints `/health` e `/predict` e execução local do serviço. |
| Versionamento | Git e GitHub | Histórico rastreável, colaboração da equipe e entrega do desafio. |

#### Tecnologias recomendadas para as próximas etapas

| Tecnologia ou prática | Aplicação proposta | Prioridade | Condição de adoção |
|---|---|---|---|
| Pytest | Testes unitários para pré-processamento, carregamento do modelo e status da API. | Alta | Requisito do Tech Challenge; incluir ao menos dois testes automatizados. |
| `class_weight="balanced"` no Scikit-Learn | Comparar um baseline sensível ao desbalanceamento sem criar dados sintéticos. | Alta | Avaliar por validação cruzada estratificada, junto do modelo sem pesos. |
| Imbalanced-learn | Testar *oversampling* ou *undersampling* somente dentro dos folds de treino. | Média | Adotar apenas se melhorar as métricas de churn sem vazamento nem perda de generalização. |
| MLflow | Registrar parâmetros, métricas, artefatos e versão de cada experimento. | Média | Útil para rastreabilidade; opcional no escopo acadêmico atual. |
| GitHub Actions | Executar testes e verificações automaticamente a cada *push* ou *pull request*. | Média | Configurar após a suíte Pytest estar disponível. |
| Docker | Padronizar a execução da API em ambientes distintos. | Média | Recomendado se houver deploy ou demonstração em ambiente externo. |
| Nuvem (AWS, Azure ou GCP) | Hospedar a API e, futuramente, integrar dados e monitoramento. | Baixa | Deploy é opcional no desafio e requer avaliação de custo, segurança e privacidade. |

As tecnologias recomendadas não fazem parte da implementação atual, exceto quando já listadas como disponíveis. Sua adoção deve ser justificada por ganho mensurável, prazo do desafio e requisitos de segurança.



## 4. Situação atual e dados disponíveis

O repositório contém o conjunto pré-processado `data/telco_customer_churn_preprocessed.csv`, com **7.043 clientes**, **20 atributos de entrada** e a variável-alvo `target`. A classe positiva (`target = 1`, churn) corresponde a **1.869 clientes (26,54%)**; a classe negativa representa 5.174 clientes. Não foram identificados valores ausentes nesse arquivo pré-processado.

Os atributos representam, entre outros, perfil de relacionamento e serviços contratados, tempo de casa, contrato, forma de pagamento, cobrança mensal e acumulada, além de CLTV.

### 4.1 Cuidados de interpretação

- CLTV e qualquer atributo calculado devem ser avaliados quanto a vazamento de informação. Nenhuma variável pode conter informação conhecida apenas depois da data do score ou após o cancelamento.
- `customer_id` é usado apenas para rastrear a resposta da API e não deve ser empregado como preditor.

## 5. Formulação da tarefa de ML

| Dimensão | Definição |
|---|---|
| Tipo de problema | Classificação binária supervisionada |
| Unidade de predição | Um cliente ativo elegível para ação de retenção |
| Alvo | `target`: 1 para churn e 0 para não churn; definição temporal a validar com negócio |
| Entrada | Perfil, relacionamento, produtos/serviços, contrato, pagamento e cobrança do cliente |
| Saída | Classe prevista e probabilidade de churn entre 0 e 1 |
| Consumo | Consulta individual via API REST e, em operação futura, lista ranqueada para campanhas |
| Horizonte | A confirmar com o dono do dado; a pontuação deve usar somente dados disponíveis na data de referência |

### 5.1 Métricas e regra de decisão

Para negócio, o foco é encontrar clientes que de fato cancelariam e para os quais a intervenção tem valor. Para o modelo, serão analisados AUC-ROC, precisão, recall e F1-score, como sugerido no desafio. O limiar de classificação não deve ser assumido como 0,50 por padrão: ele será escolhido pela relação entre custo do contato/oferta, valor esperado de retenção e capacidade da operação.

O **recall** da classe churn é prioritário quando perder um cliente elegível custa mais que um contato adicional. A **precisão** evita saturar a operação e conceder benefícios a clientes de baixo risco. F1-score equilibra ambos para a comparação inicial, enquanto AUC-ROC avalia a capacidade de ordenação independentemente do limiar. O modelo campeão deverá superar o baseline e manter desempenho estável em validação cruzada.

### 5.2 Matriz de impacto das predições

| Resultado | Consequência para a Telco | Diretriz |
|---|---|---|
| Verdadeiro positivo | Cliente de risco é priorizado e pode ser retido | Melhor caso; medir retenção incremental e custo |
| Falso positivo | Cliente sem churn recebe contato ou oferta desnecessária | Limitar por elegibilidade, frequência e custo |
| Falso negativo | Cliente em risco não é priorizado e pode cancelar | Reduzir com recall adequado e revisão de segmentos |
| Verdadeiro negativo | Cliente estável não consome capacidade de retenção | Manter observação e evitar exclusão indevida de canais de serviço |

## 6. Estratégia de ação e consumo

1. A área de Retenção define a população elegível: clientes ativos, em canais permitidos e fora de períodos de bloqueio ou excesso de contato.
2. A solução retorna a probabilidade de churn para cada cliente elegível. Em consultas unitárias, a integração utiliza `POST /predict`; `GET /health` verifica a disponibilidade da API.
3. CRM/Retenção ordena a fila por risco e aplica regras comerciais complementares, como elegibilidade de oferta e capacidade do canal.
4. A ação escolhida — comunicação, atendimento proativo, proposta de serviço ou nenhuma ação — é registrada com data, canal, custo e resultado.
5. O resultado posterior (retenção/cancelamento) retorna ao ciclo de medição para avaliar a eficácia da política e, quando aplicável, reentreinar o modelo.

O score é apoio à decisão. Não é autorização automática para desconto, bloqueio, alteração contratual, comunicação sem consentimento ou tratamento discriminatório.

## 7. Requisitos, premissas e restrições

### 7.1 Requisitos de entrega

| Categoria | Requisito |
|---|---|
| Modelagem | EDA, baseline de Regressão Logística, modelo de árvores/ensemble e MLPClassifier; comparação com validação cruzada e modelo campeão salvo |
| Engenharia | Separar notebooks de código produtivo; modularizar em `src/`; fixar seeds; gerenciar dependências |
| API | FastAPI com endpoints `/health` e `/predict`, que devolve propensão de churn |
| Qualidade | Ao menos dois testes automatizados, incluindo pré-processamento e disponibilidade/status da API |
| Documentação | README de execução, Model Card com performance, limitações e vieses, e apresentação STAR de até cinco minutos |

### 7.2 Premissas

- O rótulo de churn é historicamente confiável e corresponde ao evento de negócio acordado.
- Os dados usados em inferência terão o mesmo contrato de campos e categorias do pipeline treinado.
- Retenção terá canais, ofertas e capacidade para atuar sobre a priorização fornecida.
- O uso de dados pessoais terá finalidade legítima, base legal e controles aprovados.

### 7.3 Restrições

- O trabalho usa bibliotecas e stack definidos no desafio: Scikit-Learn, FastAPI e Pytest.
- O prazo e o contexto são acadêmicos; não há autorização implícita para acionar clientes reais.
- Não estão disponíveis no repositório os custos de incentivo, margem, histórico de campanhas ou consentimentos; por isso, o valor financeiro será calculado somente quando essas fontes forem fornecidas.
- O modelo deve ser interpretado como preditivo, não causal: associações com churn não provam que uma característica causou o cancelamento.

## 8. Riscos e controles

| Risco | Prob. | Impacto | Controle ou contingência |
|---|---|---|---|
| Vazamento de informação temporal | Média | Alto | Revisar data de referência, origem e disponibilidade de cada atributo antes do treino |
| Dados não representarem a operação real | Alta | Alto | Validar amostragem, período e distribuição; realizar piloto antes do uso em produção |
| Classe minoritária prejudicar a detecção de churn | Média | Alto | Usar divisão estratificada, métricas por classe e ajuste de limiar |
| Incentivos reduzirem margem sem efeito incremental | Média | Alto | Estabelecer grupo de controle e limite de custo por ação |
| Viés ou tratamento desigual entre grupos | Média | Alto | Avaliar métricas por segmento permitido e submeter ações à governança |
| Drift de dados ou comportamento | Média | Médio | Monitorar distribuição, taxa de churn e desempenho; definir gatilho de revisão/re-treino |
| Uso inadequado de dados pessoais | Baixa | Alto | Aplicar minimização, controle de acesso, registro de finalidade e aprovação de Privacidade |

## 9. Plano CRISP-DM e entregáveis

| Fase CRISP-DM | Pergunta de negócio | Atividade neste projeto | Evidência/entregável |
|---|---|---|---|
| 1. Entendimento do negócio | Qual decisão queremos melhorar e como medir valor? | Definir problema, stakeholders, métricas, riscos e critérios | Este documento validado |
| 2. Entendimento dos dados | Os dados suportam a decisão sem vieses ou lacunas críticas? | EDA de volume, qualidade e distribuição das variáveis | Notebook de EDA e relatório de qualidade |
| 3. Preparação dos dados | Como gerar entradas confiáveis e reproduzíveis? | Limpeza, transformação e pipeline de pré-processamento | Código em `src/` e pipeline versionado |
| 4. Modelagem | Qual modelo prioriza melhor os clientes? | Treinar baseline, árvores/ensemble e MLP; validar e comparar | Tabela de experimentos e artefato `.joblib`/`.pkl` |
| 5. Avaliação | O modelo atende aos critérios técnicos e de negócio? | Verificar métricas, estabilidade, limitações e casos de uso | Avaliação contra baseline e aprovação para demo/piloto |
| 6. Implantação | Como o score chega ao processo de retenção? | Expor e testar API FastAPI; documentar execução | `/health`, `/predict`, testes e guia de uso |

Após a entrega acadêmica, a operação deve incluir monitoramento contínuo de qualidade dos dados, desempenho, cobertura de contatos, resultado das campanhas e sinais de drift.

## 10. Governança, privacidade e uso responsável

- Aplicar minimização de dados: utilizar somente atributos necessários para a finalidade de retenção.
- Restringir acesso ao dado identificável e manter `customer_id` separado da lógica de treinamento.
- Registrar versão do dataset, pipeline, modelo, limiar, campanha e regra de elegibilidade usada em cada ação.
- Publicar um Model Card com desempenho, população avaliada, limitações, vieses conhecidos, versão e condições de uso.

## 11. Questões em aberto para o onboarding

| # | Questão | Responsável sugerido | Decisão necessária |
|---|---|---|---|
| 1 | Qual evento e qual janela temporal definem churn? | Retenção + Governança de Dados | Formalizar rótulo e data de corte |
| 2 | Qual é o custo de contato, oferta e incentivo por canal? | CRM + Finanças | Otimizar limiar e valor esperado |
| 3 | Quais segmentos podem receber cada ação e em quais canais? | CRM + Privacidade | Regras de elegibilidade e consentimento |
| 4 | Qual capacidade semanal de contatos por canal? | Operações | Dimensionar tamanho da fila priorizada |
| 5 | Há histórico de campanhas e grupo de controle? | CRM + Analytics | Medir ganho incremental e causalidade da ação |
| 6 | Quais atributos existem antes da data de decisão? | Engenharia de Dados | Prevenir vazamento e definir contrato de inferência |
| 7 | Qual métrica determina aprovação do piloto? | Patrocinador + Retenção | Fixar metas técnicas, econômicas e período de teste |

## 12. Aprovação

| Papel | Nome | Aprovação | Data |
|---|---|---|---|
| Patrocinador executivo | A definir | Pendente | — |
| Responsável por Retenção/CRM | A definir | Pendente | — |
| Liderança de Ciência de Dados | A definir | Pendente | — |
| Privacidade/Compliance | A definir | Pendente | — |

## Referências de escopo

- [Enunciado do Tech Challenge — Fase 1](11MLET%20-%20Tech%20Challenge%20Fase%201.pdf)
- [Template de Business Understanding](../notebooks/Business%20Understanding%20Template%20-%20ML.ipynb)
- Chapman et al. (2000), *CRISP-DM 1.0: Step-by-step data mining guide*.
