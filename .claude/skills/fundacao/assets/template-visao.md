# Template da visão do produto

Indica a forma e o conteúdo de `docs/produto/visao.md`, escrita pelo agente `gerente-de-produto`
no modo `visao` (fluxo `/fundacao`). Não é um exemplo a copiar: cada `[...]` diz o que entra
naquele lugar.

## Regras

- **Estrutura fixa.** As quatro seções abaixo, com esses títulos e nessa ordem. Não acrescente,
  renomeie nem remova seções. Todo `[...]` é substituído.
- **Status.** A visão nasce `em revisão` e só passa a `aprovada` com a frase de aprovação do
  usuário, no Portão 1. A mudança de status é um `Edit` só nessa linha.
- **Origem de cada afirmação.** Toda afirmação termina com `[FUNDAMENTADO]` (com a fonte: a fala
  do usuário ou o arquivo lido), `[INFERIDO]` (com uma linha dizendo de onde vem) ou `[LACUNA]`.
  Público, problema, objetivos e o que o produto não é só o usuário pode dizer: o que ele não
  disse é `[LACUNA]` e vai para "Perguntas para o usuário", nunca é preenchido por suposição.
- **Objetivos identificados.** Cada objetivo tem um identificador `OBJ-<n>`, em sequência a
  partir de `OBJ-1`. É por ele que as specs ("Alinhamento com a visão") e o backlog citam o
  objetivo. Um identificador nunca é reaproveitado: objetivo retirado fica riscado
  (`~~OBJ-2 — ...~~`) com o motivo ao lado; objetivo novo recebe o próximo número.
- **Objetivo é resultado, não solução.** Descreve o que muda para o usuário ou para o negócio,
  de forma que se possa dizer depois se uma feature contribuiu para ele. Uma funcionalidade
  ("ter um painel") não é objetivo; ela pertence a uma spec.
- **Nada técnico.** Stack, arquitetura e ferramentas não entram na visão: são da ADR de base.
- **Curta.** Cabe em uma página. Cenários, histórias e critérios de aceite são da spec de cada
  feature.
- **Sem histórico.** A visão descreve o agora. O que mudou, quando e por quê fica em
  `docs/produto/decisoes-de-produto.md`.

## Estrutura

```markdown
# Visão — [nome do produto]

Status: em revisão

## Para quem o produto existe

- [Papel ou perfil de quem usa] — [a situação em que essa pessoa recorre ao produto]. [classificação]

[Uma linha por público. Se houver mais de um, o primeiro é o principal.]

## Problema central

[Uma a três frases: que dor esse público tem hoje, em que situação, e o que ela lhe custa.
Descreva o problema, não o produto nem a solução.] [classificação]

## O que o produto não é

- [Um uso, um público ou um problema que alguém poderia esperar do produto e que ele
  deliberadamente não atende] — [por que fica de fora]. [classificação]

[Ao menos um item. É o que permite recusar ou adiar um pedido com referência à visão.]

## Objetivos atuais

- **OBJ-1** — [O resultado que se quer para o usuário ou para o negócio] — [o sinal observável
  que mostra avanço]. [classificação]

[Em ordem de prioridade. Poucos: o bastante para decidir entre dois pedidos concorrentes.]
```
