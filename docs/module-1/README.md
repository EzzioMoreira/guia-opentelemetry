# Monitoramento e Observabilidade.

O monitoramento é utilizado há décadas por equipes de TI para obter insights sobre a disponibilidade e performance de sistemas. A observabilidade é uma evolução do monitoramento, que busca entender o comportamento de sistemas complexos.

## O que é Monitoramento?

O monitoramento é a prática que visa coletar dados sobre a disponibilidade e performance de sistemas. Esses dados são utilizados para identificar problemas e tomar decisões baseadas em fatos.

O monitoramento tradicional é totalmente reativo, e se concentra em métrica, alerta e dashboards. Dashboard repleta de gráficos, e talvez não sabemos o que todos os gráficos realmente dizem.

Seguindo esse conceito, um sistema monitorado é capaz de produzir respostas para várias perguntas previamente conhecidas. Dentre elas, temos:

- Como estão os níveis de consumo de recursos computacional (CPU, memória, disco, rede)?
- Qual é a taxa de erro da última hora?
- Qual é o tempo médio de resposta das requisições?
- Existe algum alerta disparado?

Você pode pensar no monitoramento como um semáforo:

- O componente está disponível e saudável? 
  - Verde: tudo está bem.
- O componente está em riso?
  -  amarelo: atenção, algo pode estar errado.
- O componente está em falha?
  - vermelho: algo está errado.

As repostas para esses questionamentos nos permite determinar o estado atual do sistema, e tomar ações corretivas quando necessário. Essas informações são cruciais em análise de incidentes, troubleshooting e planejamento de capacidade.

## O que é Observabilidade?

A observabilidade é a capacidade de compreender o estado interno de um sistema com base em suas saídas. A observabilidade fornece todos os dados que você precisa, no contexto adequado, para identificá-los e preveni-los proativamente.

Conforme essa definição, alguns questionamento que podem surgir em um sistema observável:

- Quais são os impactos de uma mudança em um microserviço específico?
- Qual motivo esse cliente específico está recebendo erros?
- Quais são os serviços mais lentos em um ambiente de produção?

Os engenheiros que praticam a observabilidade conseguem questionar o sistema fazendo perguntas exploratórias, usando as respostas para conduzir a outras investigações. Tais questionamentos podem ser realizados em diferentes estágios do ciclo de vida do sistema, de acordo com o contexto da situação enfrentada.


