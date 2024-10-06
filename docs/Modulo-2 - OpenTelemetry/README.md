# OpenTelemetry

Em 2019, houve a fusão entre dois projetos, [OpenCensus](https://opencensus.io/) e [OpenTracing](https://opentracing.io/), que resultou no [OpenTelemetry](https://opentelemetry.io/). Os dois projetos queriam resolver um problema em comum: a falta de padrões para instrumentação de aplicações.

A combinação dos pontos fortes de cada projeto permite que os usuários resolvam os desafios da observabilidade utilizando um padrão único de bibliotecas, APIs, coleta, processamento e envio de dados de telemetria agnóstico de vendors de observabilidade.

## O que é OpenTelemetry?

O OpenTelemetry é uma framework e um conjunto de ferramentas que são utilizados para criar e gerenciar dados de telemetria. Umas das características mais importante do OpenTelemetry é a capacidade de ser agnóstico em relação a fornecedor e ferramentas de observabilidade.

> O OpenTelemetry não é um backend de observabilidade como Zabbix, Prometheus, Grafana, Jaeger, etc. O foco do OpenTelemetry se concentra na geração, coletar, processar e envio de telemetria.

## Principais Componentes do OpenTelemetry

Os principais componentes do OpenTelemetry são:

### Especificação OpenTelemetry

A especificação do OpenTelemetry define os requisitos e expectativas para todas as implementações do OpenTelemetry, abrangendo todos os componentes. A especificação cobre os aspectos na geração, coleta, processamento, envio, APIs, SDKs, convenção semântica etc.

### API e SDK OpenTelemetry

O OpenTelemetry fornece APIs e SDKs para instrumentar aplicações. As APIs são interfaces que definem como os desenvolvedores podem interagir com o OpenTelemetry. Os SDKs são implementações das APIs que fornecem funcionalidades para instrumentar aplicações.

### Convenção Semântica

Convenção semântica especifica nomes comuns e formatos de dados para telemetria. A convenção semântica é importante para garantir que os dados de telemetria sejam consistentes e compreensíveis.

### OpenTelemetry Collector

O OpenTelemetry Collector é um middleware independente de fornecedor que coleta/recebe, processa e exporta dados de telemetria em diversos formatos. O OpenTelemetry Collector possui componentes que o torna altamente configurável e extensível.

## Instrumentação

Instrumentação é o processo de adicionar código em aplicações para gerar dados de telemetria. A instrumentação pode ser feita manualmente ou automaticamente.

### Instrumentação Manual

### Instrumentação Automática

## Saiba mais

- [OpenTelemetry - What is OpenTelemetry?](https://opentelemetry.io/pt/docs/what-is-opentelemetry/)
- [OpenTelemetry - Specification](https://opentelemetry.io/docs/specification/)
- [OpenTelemetry - Components](https://opentelemetry.io/pt/docs/concepts/components/)
- [OpenTelemetry - Semantic Conventions](https://opentelemetry.io/pt/docs/concepts/semantic-conventions/)
- [OpenTelemetry - Collector](https://opentelemetry.io/pt/docs/collector/)
- [OpenTelemetry - Collector Contrib GitHub](https://github.com/open-telemetry/opentelemetry-collector-contrib)
