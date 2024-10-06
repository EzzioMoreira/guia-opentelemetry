# Treinamento OpenTelemetry

## Objetivo

Capacitar pessoas nos conceitos básicos de monitoramento, observabilidade e telemetria, além de ensinar a implementar e operar os recursos do OpenTelemetry. O curso proporcionará habilidades práticas para gerar, coletar, processar e exportar telemetria (logs, métricas e traces). Ao final, os participantes estarão aptos a integrar as funcionalidades do OpenTelemetry em suas aplicações.

## Público-alvo

Desenvolvedores, arquitetos de software, analistas de sistemas e profissionais de infraestrutura que desejam aprender sobre monitoramento, observabilidade, telemetria e OpenTelemetry.

## Pré-requisitos

Conhecimento básico em desenvolvimento de software, infraestrutura e Kubernetes.

### Ferramentas

- [Docker](https://docs.docker.com/get-docker/) 🐳
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) ☸️
- [Helm](https://helm.sh/docs/intro/install/) ⛵
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) 📦

## Estrutura do treinamento

O treinamento será dividido em módulos teóricos e práticos para garantir uma compreensão abrangente dos conceitos e habilidades necessárias para implementar e manter o OpenTelemetry. Cada módulo combinará teoria com exercícios práticos e serão armazenados no GitHub.

- **Conceitos Básicos**: Iniciar com a introdução aos princípios de monitoramento, observabilidade e telemetria, instrumentação e projeto OpenTelemetry.
- **Instrumentação**: Explorar a instrumentação manual e automática de aplicações usando SDK e API OpenTelemetry.
- **Configuração do OpenTelemetry Collector**: Implementar e configuração do OpenTelemetry Collector, cobrindo a arquitetura e como configurar pipelines para coletar, processar e exportar dados.
- **Escalabilidade e Resiliência**: Abordar como tornar a observabilidade escalável e resiliente, utilizando Kafka e OpenTelemetry loadbalance para lidar com grandes volumes de dados.

## Modulo 1 - Conceitos Básicos

- [Monitoramento e Observabilidade](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#monitoramento-e-observabilidade)
  - [O que é Monitoramento?](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#o-que-é-monitoramento)
  - [O que é Observabilidade?](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#o-que-é-observabilidade)
  - [Saiba mais](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#saiba-mais)
- [Telemetria](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#telemetria)
  - [Métricas](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#métricas)
    - [Tipos de Métricas](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#tipos-de-métricas)
  - [Cardinalidade](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#cardinalidade)
  - [Traces](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#traces)
    - [Propagação de Contexto](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#propagação-de-contexto)
    - [Amostragem](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#amostragem)
  - [Logs](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#logs)
  - [Saiba mais](./docs/Module-1%20-%20Conceitos%20Básicos/README.md#saiba-mais)

## Modulo 2 - OpenTelemetry

- [OpenTelemetry](./docs/Modulo-2%20-%20OpenTelemetry/README.md#opentelemetry)
  - [O que é OpenTelemetry?](./docs/Modulo-2%20-%20OpenTelemetry/README.md#o-que-é-opentelemetry)
  - [Principais Componentes do OpenTelemetry](./docs/Modulo-2%20-%20OpenTelemetry/README.md#principais-componentes-do-opentelemetry)
    - [Especificação OpenTelemetry](./docs/Modulo-2%20-%20OpenTelemetry/README.md#especificação-opentelemetry)
    - [API e SDK OpenTelemetry](./docs/Modulo-2%20-%20OpenTelemetry/README.md#api-e-sdk-opentelemetry)
    - [Convenção Semântica](./docs/Modulo-2%20-%20OpenTelemetry/README.md#convenção-semântica)
    - [OpenTelemetry Collector](./docs/Modulo-2%20-%20OpenTelemetry/README.md#opentelemetry-collector)
  - [Instrumentação](./docs/Modulo-2%20-%20OpenTelemetry/README.md#instrumentação)
    - [Instrumentação Manual](./docs/Modulo-2%20-%20OpenTelemetry/README.md#instrumentação-manual)
    - [Instrumentação Automática](./docs/Modulo-2%20-%20OpenTelemetry/README.md#instrumentação-automática)
  - [Saiba mais](./docs/Modulo-2%20-%20OpenTelemetry/README.md#saiba-mais)