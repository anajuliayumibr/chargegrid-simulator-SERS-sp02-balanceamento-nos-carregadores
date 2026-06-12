## ChargeGrid - Simulador de Recarga + Balanceamento de Carga entre carregadores

FIAP + GoodWe = EV Challenge 2026 - Sprint 2

## Integrantes:

Ana Julia Yumi Inoue - RM: 569430

João Pedro Santos Ferreira - RM: 569202

Maria Beatriz Braga de Lima - RM: 570501

Maria Fernanda Dias Ribeiro - RM: 569999

Ulysses Gomes Soares de Souza - RM: 573826

Yasmin Cristina Carvalho Mayer - RM: 573964

----
## Objetivo: 

*  O projeto inicial simula o funcionamento de uma estação de recarga elétrica, permitindo acompanhar: nível da bateria energia transferda tempo de recarga custo total da sessão
  
* Recarga individual: simular sessão de recarga minuto a minuto, com eficiência reduzida após 80%.

* Foi adicionado o Balanceamento de múltiplos veículos no terminal: para dividir a potência disponível igualmente entre os carros conectados, sem ultrapassar o limite da rede. -> Reduz desperdício, evita sobrecarga, protege equuipamentos..
  
* Prova de conceito funcional/demonstração técnica real no projeto (vídeo)
----

## Fluxo do Sistema 
* Usuário informa tipo de conta (comum/premium), potência do carregador, bateria inicial e limite desejado.

* Sistema inicia a recarga e mostra progresso em tempo real.

* Ao final, gera recibo com energia total, custo e tempo.

* No modo balanceamento, permite conectar/desconectar veículos e redistribui potência automaticamente.
---

## Arquitetura do Sistema

* Usuário informa tipo de conta (comum/premium), potência do carregador, bateria inicial e limite desejado.

* Sistema inicia a recarga e mostra progresso em tempo real.

* Ao final, gera recibo com energia total, custo e tempo.

* No modo balanceamento, permite conectar/desconectar veículos e redistribui potência automaticamente.


## Principais Funcionalidades
* Recarga individual → lógica original intacta.

* Balanceamento de carga → nova função da Sprint 02.

* Exibição da rede → barra de uso percentual + tabela de veículos ativos.

* Recibo final → resumo da sessão com subtotal e total.
--

## Sustentabilidade
* Eficiência reduzida após 80% da bateria → evita desperdício e protege a bateria.

* Balanceamento garante que a rede nunca ultrapasse o limite → evita sobrecarga e uso de fontes poluentes.
-- 

## Estrutura do Projeto 
Sprint 02 → evolução: balanceamento de múltiplos veículos no terminal.
* algorithm.py → lógica principal (recarga + balanceamento).

* simulator.py → interface gráfica Tkinter (recarga individual).
-- 
## Justificativas Técnicas

Python: linguagem versátil e acessível para simulações.

Terminal interativo: simplicidade e portabilidade, sem dependência gráfica.

Modularidade: funções separadas (executar_recarga, balancear, exibir_rede) facilitam manutenção e evolução.


