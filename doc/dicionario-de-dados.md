# Dicionário de Dados
- `CustomerID` - ID único que identifica cada cliente.

- `Count` - Valor usado em relatórios e painéis para somar o número de clientes em um conjunto filtrado.

- `Country` - O país de residência principal do cliente.

- `State` - O estado de residência principal do cliente.

- `City` - A cidade de residência principal do cliente.

- `Zip Code` - O código postal da residência principal do cliente.

- `Lat Long` - Latitude e longitude combinadas da residência principal do cliente.

- `Latitude` - A latitude da residência principal do cliente.

- `Longitude` - A longitude da residênca principal do cliente.

- `Gender` - O gênero do cliente: Male, Female

- `Senior Citizen` - Indica se o cliente tem mais de 65 anos: Yes, No

- `Partner` - Indica se o cliente tem um(a) parceiro(a): Yes, No

- `Dependents` - Indica se o cliente vive com dependentes: Yes, No. Dependentes podem ser filhos, pais, avós, etc.

- `Tenure Months` - Indica a quantidade total de meses que o cliente é um cliente até a data.

- `Phone Service` - Indica se o cliente assina um serviço de linha telefônica fixa com a companhia: Yes, No

- `Multiple Lines` - Indica se o cliente assina múltiplas linhas telefônicas com a companhia: Yes, No

- `Internet Service` - Indica se o cliente assina um serviço de Internet com a companhia: No, DSL, Fiber Optic, Cable.

- `Online Security` - Indica se o cliente assina um serviço adicional de segurança online fornecido pela companhia: Yes, No

- `Online Backup` - Indica se o cliente assina um serviço adicional de backup online fornecido pela companhia: Yes, No

- `Device Protection` - Indica se o cliente assina um plano adicional de proteção para dispositivos fornecido pela companhia para o seu equipamento de Internet: Yes, No

- `Tech Support` - Indica se o cliente assina um plano adicional de suporte técnico da companhia com tempo de espera reduzido: Yes, No

- `Streaming TV` - Indica se o cliente usa seu serviço de Internet para o stream de programação de televisão de um fornecedor terceiro: Yes, No. A companhia não cobra taxas adicionais por este serviço.

- `Streaming Movies` - Indica se o cliente usa seu serviço de Internet para o stream de filmes de um fornecedor terceiro: Yes, No. A companhia não cobra taxas adicionais por este serviço.

- `Contract` - Indica o tipo de contrato atual do cliente: Month-to-Month, One Year, Two Year.

- `Paperless Billing` - Indica se o cliente escolheu cobrança virtual: Yes, No

- `Payment Method` - Indica como o cliente paga sua conta: Bank Withdrawal, Credit Card, Mailed Check

- `Monthly Charge` - Indica o valor mensal total cobrado do cliente pelos serviços fornecidos pela companhia.

- `Total Charges` - Indica o valor total cobrado do cliente, calculado até a data.

- `Churn Label` - Yes = o cliente deixou a companhia neste trimestre. No = o cliente permaneceu com a companhia. Diretamente relacionado ao Churn Value.

- `Churn Value` - 1 = o cliente deixou a companhia neste trimestre. 0 = o cliente permaneceu com a companhia. Diretamente relacionado ao Churn Label.

- `Churn Score` - Um valor entre 0-100 calculado usando a ferramenta preditiva IBM SPSS Modeler. O modelo incorpora múltiplos fatores conhecidos por causar churn. Quanto maior o valor, maior a chance do cliente deixar a companhia.

- `CLTV` - Customer Lifetime Value. O CLTV predito é calculado usando fórmulas corporataivas e dados existentes. Quanto maior o valor, mais valioso é o cliente. Clientes valiosos devem ser monitorados para o churn.

- `Churn Reason` - O motivo específico que levou o cliente a deixar a companhia.