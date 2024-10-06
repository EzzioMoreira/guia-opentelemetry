# Monitoramento e Observabilidade

O monitoramento é utilizado há décadas por equipes de TI para obter insights sobre a disponibilidade e performance de sistemas. A observabilidade é uma evolução do monitoramento, que busca entender o comportamento de sistemas complexos.

## O que é Monitoramento?

O monitoramento é a prática que visa coletar dados sobre a disponibilidade e performance de sistemas. Esses dados são utilizados para identificar problemas e tomar decisões baseadas em fatos. O monitoramento tradicional é totalmente reativo, e se concentra em métrica, alerta e dashboards. Dashboard repleta de gráficos, e talvez não sabemos o que todos os gráficos realmente dizem.

Seguindo esse conceito, um sistema monitorado é capaz de produzir respostas para várias perguntas previamente conhecidas. Alguns exemplos de perguntas que podem ser respondidas por um sistema monitorado:

- Como estão os níveis de consumo de recursos computacional (CPU, memória, disco, rede)?
- Qual é a taxa de erro da última hora?
- Qual é o tempo médio de resposta das requisições?
- Existe algum alerta disparado?

Você pode pensar no monitoramento como um semáforo:

- O componente está disponível e saudável? 
  - Verde: tudo está bem.
- O componente está em riso?
  - Amarelo: atenção, algo pode estar errado.
- O componente está em falha?
  - Vermelho: algo está errado.

As repostas para esses questionamentos nos permite determinar o estado atual do sistema, e tomar ações corretivas quando necessário. Essas informações são cruciais em análise de incidentes, troubleshooting e planejamento de capacidade.

## O que é Observabilidade?

A observabilidade nada mais é do que a capacidade de compreender o estado interno de um sistema com base em seu comportamento.
Para um sistema ser considerado minimamente observável é necessário cumprir alguns requisitos, sendo eles: permitir a coleta de logs, métricas, traces distribuídos, eventos e correlacionar esses dados de forma a permitir a identificação de problemas e a tomada de decisões baseadas em fatos.

Conforme essa definição, alguns questionamento que podem surgir em um sistema observável:

- Quais são os impactos de uma mudança em um microsserviços específico?
- Qual motivo esse cliente específico está recebendo erros?
- Quais são os serviços mais lentos em um ambiente de produção?

Os engenheiros que praticam a observabilidade conseguem questionar o sistema fazendo perguntas exploratórias, usando as respostas para conduzir a outras investigações. Tais questionamentos podem ser realizados em diferentes estágios do ciclo de vida do sistema, de acordo com o contexto da situação enfrentada.

## Saiba mais

- [Qual é a diferença entre um sistema centralizado e um distribuído?](https://www.atlassian.com/br/microservices/microservices-architecture/distributed-architecture)
- [eBook Free - Monitoring - Google SRE Book](https://sre.google/workbook/monitoring/)
- [eBook Free - Distributed Systems Observability](https://unlimited.humio.com/rs/756-LMY-106/images/Distributed-Systems-Observability-eBook.pdf)
- [eBook Observability Engineering](https://info.honeycomb.io/observability-engineering-oreilly-book-2022)
- [Introdução à Observabilidade - OpenTelemetry](https://opentelemetry.io/pt/docs/concepts/observability-primer/)

# Telemetria

Telemetria é um tipo de dado gerado por um sistema. Esse dado é utilizado para monitorar e observar o comportamento de um sistema. Provavelmente você está familiarizado com dois tipos de telemetria: métricas e logs.

## Métricas

Métrica é uma representação numérica de uma característica de um sistema em relação ao tempo. As métricas fornecem uma visão geral da integridade e performance do sistema. 

As métricas também são úteis para escalar o ambiente, planejar capacidade e são mais indicadas para criar alertas e dashboards.

![metric](./images/metric.jpeg)

A métrica é composta por um nome da métrica (por exemplo, `http.requests.total`), o registro de data e hora (com precisão em milissegundos), pelo valor da métrica (um valor float64) e tags.

Após a coleta, as métricas apresentam maior flexibilidade para cálculos matemáticos, probabilidade, estatistificas, amostragem, etc.

### Tipos de métricas

A maioria das bibliotecas de métricas suportam os seguintes tipos de métricas:

- **Counter**: Um valor que acumula com o tempo, esse valor só cresce ou pode ser redefinido para zero na reinicialização. São muito utilizadas para contagem de eventos: número de requisições HTTP, número de erros, quantidade de acessos. 

- **Gauge**: Um valor que pode aumentar ou diminuir ao longo do tempo. São muito utilizadas para representar valores instantâneos: uso de CPU, memória, etc.

- **Histogram**: Um contador que fornece a distribuição de valores em um intervalo. São muito utilizadas para medir a distribuição de valores: tempo de resposta de uma requisição entre 0-100ms, 100-200ms, tamanho de arquivos.

## Cardinalidade

Cardinalidade se refere ao número de valores possíveis que uma métrica pode assumir. Métricas com alta cardinalidade podem ser mais difíceis de armazenar e processar.

Muitos sistemas de banco de dados não conseguem lidar com eficiência com o volume de dados gerado por métricas de alta cardinalidade. Por isso, é importante entender a cardinalidade dos dados que você está gerando, coletando e armazenando.

**Alta Cardinalidade**: "Monitorar os números de placa de cada carro no estacionamento." (Muitos valores únicos, um para cada carro).

**Baixa Cardinalidade**: "Contar quantos carros são de cada cor no estacionamento." (Poucos valores únicos, como vermelho, azul, preto).

## Saiba mais

- [Prometheus - Types of metrics](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus - Metric and label naming](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry - Metrics](https://opentelemetry.io/pt/docs/concepts/signals/metrics/)
- [Honeycom - Understanding High Cardinality and Its Role in Observability](https://www.honeycomb.io/getting-started/understanding-high-cardinality-role-observability)