# Guia Prático OpenTelemetry

## Objetivo

Apresentar os conceitos fundamentais de monitoramento, observabilidade e telemetria, além de fornecer um passo a passo prático para implementar e operar os recursos do OpenTelemetry. Este guia oferece habilidades práticas para gerar, coletar, processar e exportar telemetria logs, métricas e traces. Ao final da leitura, você estará apto a integrar as funcionalidades do OpenTelemetry em suas aplicações de forma eficiente.

## Agradecimentos

Este guia não seria possível sem o apoio e contribuição de pessoas especiais:

Um agradecimento especial ao [Juraci Paixão Kröhling](https://www.linkedin.com/in/jpkroehling/), que não só me apresentou ao mundo do OpenTelemetry como também me proporcionou inúmeras oportunidades para aprender e crescer nesta jornada. Sua mentoria foi fundamental!

[Lindemberg Barbosa](https://www.linkedin.com/in/lindemberg-barbosa/) e [Pedro Espíndula](https://www.linkedin.com/in/pedroespindula/) pelo incrível trabalho de revisão e contribuições técnicas ao conteúdo deste guia. Suas percepções foram valiosíssimas!

Obrigado, vocês são incríveis! ❤️❤️❤️❤️

## Sobre o Autor

Olá! Sou **Ezzio Moreira**, membro do projeto OpenTelemetry, atuo como SRE e criei este guia para compartilhar conhecimentos práticos que gostaria de ter tido quando comecei minha jornada em observabilidade.

**Por que este guia?**  
- Combina fundamentos teóricos com implementações reais
- Foca em cenários práticos do dia a dia
- Apresenta decisões de arquitetura baseadas em experiências reais
- Ofrece exercícios hands-on para fixação do aprendizado

**Minha filosofia:**  
> "Observabilidade deve ser acessível, prática e agregar valor real aos times de desenvolvimento"

Conecte-se comigo:  
[🔗 LinkedIn](seu_link) | [🐙 GitHub](seu_link) | [✉️ Email](mailto:seu@email)

## Público-alvo

Desenvolvedores, arquitetos de software, analistas de sistemas e profissionais de infraestrutura que desejam aprender sobre monitoramento, observabilidade, telemetria e OpenTelemetry.

## Pré-requisitos

Conhecimento básico em desenvolvimento de software, infraestrutura e Kubernetes.

### Ferramentas

- [Docker](https://docs.docker.com/get-docker/) 🐳
- [Docker Compose](https://docs.docker.com/compose/install/) 🐳

## Estrutura do Guia OpenTelemetry

Este guia será dividido em módulos teóricos e práticos para garantir uma compreensão abrangente dos conceitos e habilidades necessárias para implementar e manter o OpenTelemetry. Cada módulo combinará teoria com exercícios práticos e serão armazenados no GitHub.

- **Conceitos Básicos**: Iniciar com a introdução aos princípios de monitoramento, observabilidade e telemetria, instrumentação e projeto OpenTelemetry.
- **Instrumentação**: Explorar a instrumentação manual e automática de aplicações usando SDK e API OpenTelemetry.
- **Configuração do OpenTelemetry Collector**: Implementar e configuração do OpenTelemetry Collector, cobrindo a arquitetura e como configurar pipelines para coletar, processar e exportar dados.
- **Escalabilidade e Resiliência**: Abordar como tornar a observabilidade escalável e resiliente, utilizando Kafka e OpenTelemetry loadbalance para lidar com grandes volumes de dados.

## Módulo 1 - Conceitos Básicos

- [Monitoramento e Observabilidade](./docs/module-1/README.md#monitoramento-e-observabilidade)
  - [O que é Monitoramento?](./docs/module-1/README.md#o-que-é-monitoramento)
  - [O que é Observabilidade?](./docs/module-1/README.md#o-que-é-observabilidade)
  - [Saiba mais](./docs/module-1/README.md#saiba-mais)
- [Telemetria](./docs/module-1/README.md#telemetria)
  - [Métricas](./docs/module-1/README.md#métricas)
    - [Tipos de Métricas](./docs/module-1/README.md#tipos-de-métricas)
  - [Cardinalidade](./docs/module-1/README.md#cardinalidade)
  - [Traces](./docs/module-1/README.md#traces)
    - [Propagação de Contexto](./docs/module-1/README.md#propagação-de-contexto)
    - [Amostragem](./docs/module-1/README.md#amostragem)
  - [Logs](./docs/module-1/README.md#logs)
  - [Saiba mais](./docs/module-1/README.md#saiba-mais)

## Módulo 2 - OpenTelemetry

- [OpenTelemetry](./docs/module-2/README.md#opentelemetry)
  - [O que é OpenTelemetry?](./docs/module-2/README.md#o-que-é-opentelemetry)
  - [Principais Componentes do OpenTelemetry](./docs/module-2/README.md#principais-componentes-do-opentelemetry)
    - [Especificação OpenTelemetry](./docs/module-2/README.md#especificação-opentelemetry)
    - [API e SDK OpenTelemetry](./docs/module-2/README.md#api-e-sdk-opentelemetry)
    - [Convenção Semântica](./docs/module-2/README.md#convenção-semântica)
    - [OpenTelemetry Collector](./docs/module-2/README.md#opentelemetry-collector)
  - [Instrumentação](./docs/module-2/README.md#instrumentação)
    - [Instrumentação Sem Código](./docs/module-2/README.md#instrumentação-sem-código)
    - [Instrumentação Manual](./docs/module-2/README)
  - [Saiba mais](./docs/module-2/README.md#saiba-mais)
  
## Módulo 3 - Instrumentação Sem Código

- [Módulo 3](./docs/module-3/README.md)
  - [Instrumentação Com e Sem Código](./docs/module-3/README.md#instrumentação-com-e-sem-código)
  - [Requisitos](./docs/module-3/README.md#requisitos)
  - [Sistema Bookstore](./docs/module-3/README.md#sistema-bookstore)
    - [Microserviços](./docs/module-3/README.md#microserviços)
    - [Diagrama de Arquitetura](./docs/module-3/README.md#diagrama-de-arquitetura)
    - [Diagrama de Sequência](./docs/module-3/README.md#diagrama-de-sequência)
    - [Diagrama Geral do Sistema e Stack de Observabilidade](./docs/module-3/README.md#diagrama-geral-do-sistema-e-stack-de-observabilidade)
  - [Instrumentação Sem Código](./docs/module-3/instrumentação-sem-código.md)
    - [Implementando Instrumentação Sem Código](./docs/module-3/instrumentação-sem-código.md#implementando-instrumentação-sem-código)
    - [O que Esperar?](./docs/module-3/instrumentação-sem-código.md#o-que-esperar)
    - [Exercício](./docs/module-3/instrumentação-sem-código.md#exercício)
    - [Resultado Esperado](./docs/module-3/instrumentação-sem-código.md#resultado-esperado)
    - [Conclusão](./docs/module-3/instrumentação-sem-código.md#conclusão)
    - [Saiba Mais](./docs/module-3/instrumentação-sem-código.md#saiba-mais)

## Módulo 4 - Instrumentação Manual

- [Criação de Trace](./docs/module-4/criando-trace.md)
  - [Adicionando Spans](./docs/module-4/criando-trace.md#adicionando-spans)
  - [Adicionando Atributos ao Span](./docs/module-4/criando-trace.md#adicionando-atributos-ao-span)
  - [Adicionando Eventos ao Span](./docs/module-4/criando-trace.md#adicionando-eventos-ao-span)
  - [Adicionando Status ao Span](./docs/module-4/criando-trace.md#adicionando-status-ao-span)
  - [Criando Span Aninhado](./docs/module-4/criando-trace.md#criando-span-aninhado)
  - [Instrumentando Queries SQL](./docs/module-4/criando-trace.md#instrumentando-queries-sql)
  - [Exercício](./docs/module-4/criando-trace.md#exercícios)
  - [Conclusão](./docs/module-4/criando-trace.md#conclusão)
- [Propagação de Contexto](./docs/module-4/propagacao-contexto.md)
  - [Contexto](./docs/module-4/propagacao-contexto.md#contexto)
  - [Propagadores](./docs/module-4/propagacao-contexto.md#propagadores)
  - [Criando Causalidade entre Spans](./docs/module-4/propagacao-contexto.md#criando-causalidade-entre-spans)
  - [Propagando Contexto com o OpenTelemetry](./docs/module-4/propagacao-contexto.md#propagando-contexto-com-o-opentelemetry)
  - [Conclusão](./docs/module-4/propagacao-contexto.md#conclusão)
- [Solução do Exercício](./docs/module-4/solucao-exercicio/README.md)
  - [Criando Trace](./docs/module-4/solucao-exercicio/criando-trace/)
  - [Propagação de Contexto](./docs/module-4/solucao-exercicio/propagacao-contexto/)

## Módulo 5 - Criando Métricas

- [Criando Métricas](./docs/module-5/criando-metrica.md)
  - [Criando Métricas Counter](./docs/module-5/criando-metrica.md#criando-métricas-counter)
  - [Criando Métricas Histogram](./docs/module-5/criando-metrica.md#criando-métricas-histogram)
  - [Criando Métricas Gauge](./docs/module-5/criando-metrica.md#criando-métricas-gauge)
- [Exercício](./docs/module-5/criando-metrica.md#exercício)
- [Conclusão](./docs/module-5/criando-metrica.md#conclusão)
- [Solução do Exercício](./docs/module-5/solucao-exercicio/README.md)

## Módulo 6 - Instrumentando Logs

- [Instrumentando Logs](./docs/module-6/instrumentando-logs.md)
  - [Configurando Logs OpenTelemetry no Cadastro de Livros](./docs/module-6/instrumentando-logs.md#configurando-logs-opentelemetry-no-cadastro-de-livros)
  - [Configurando Logs OpenTelemetry no Ordem de Compra](./docs/module-6/instrumentando-logs.md#configurando-logs-opentelemetry-no-ordem-de-compra)
- [Exercício](./docs/module-6/instrumentando-logs.md#exercício)
- [Conclusão](./docs/module-6/instrumentando-logs.md#conclusão)
- [Solução do Exercício](./docs/module-6/solucao-exercicio/REAMDE.md)

## Módulo 7 - OpenTelemetry Collector
- Em desenvolvimento...

## 🛠️ Como Contribuir

Contribuições são muito bem-vindas! Este material é um projeto colaborativo, e toda ajuda é valiosa para torná-lo mais completo e acessível para a comunidade.

- [Vaja como contribuir.](CONTRIBUTING.md)
