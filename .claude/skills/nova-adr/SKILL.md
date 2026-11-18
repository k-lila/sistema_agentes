---
name: nova-adr
description: Cria e gerencia Architecture Decision Records (ADRs) no formato de Michael Nygard, com seção de alternativas consideradas. Use quando o usuário quiser documentar ou registrar uma decisão de arquitetura ou técnica, ou criar, editar ou mudar o status (aceitar, rejeitar, descontinuar, substituir) de ADRs em docs/adr/. Quando o usuário tomar uma decisão significativa de design ou arquitetura sem pedir uma ADR, apenas sugira registrá-la, sem criá-la.
---

# Gerador de ADR

Produz ADRs no formato de Michael Nygard (Status, Contexto, Decisão, Consequências), acrescido
das seções "Diretrizes", "Verificação" e "Alternativas consideradas", para responder depois "por
que fizemos assim?" e dar a quem implementa e a quem testa regras verificáveis.

O agente `arquiteto` também usa este template e estas regras como fonte única do formato de ADR.

## Princípio de gravação

- **ADR em `Proposto` é rascunho.** Criar uma ADR com `Proposto` ou editar uma ADR que ainda
  está em `Proposto` não exige aprovação prévia do conteúdo: o próprio status já diz que é uma
  proposta. Basta o pedido do usuário e, fora dos fluxos `/feature` e `/fundacao`, o relatório
  das regras de método do projeto (razões e arquivos). Depois de gravar, apresente a ADR para
  revisão.
- **A aprovação da decisão é a linha `Aceito`**, e ela é gravada só pelo usuário (ver
  *Ciclo de vida*). O mesmo vale para `Substituído por ADR-NNNN`.
- `Rejeitado` e `Descontinuado` só são gravados a pedido do usuário, depois de mostrar a linha
  e obter a aprovação dele.

## Ciclo de vida

```
Proposto ──► Aceito ──► Descontinuado              (terminal)
   │            └─────► Substituído por ADR-NNNN   (terminal)
   └──────► Rejeitado                               (terminal)
```

A seção Status é um histórico: uma linha por transição, em ordem cronológica, no formato

```
- <Status> — AAAA-MM-DD[ — complemento]
```

- **Rejeitado** e **Descontinuado**: o complemento é um motivo curto, obrigatório.
- **ADR nova que substitui outra**: a primeira linha leva `— substitui ADR-NNNN`.
- **ADR antiga substituída**: recebe `- Substituído por ADR-NNNN — AAAA-MM-DD`. Essa linha só
  é acrescentada quando a ADR nova passa a `Aceito`; antes disso a substituição é apenas uma
  proposta.
- **Quem grava cada linha**: `Proposto`, `Rejeitado` e `Descontinuado` são gravados pela skill
  (ou pelo agente `arquiteto`). `Aceito` e `Substituído por ADR-NNNN` são gravados **somente
  pelo usuário, à mão**, no arquivo da ADR e na linha dela no índice: a skill mostra a linha
  exata, com a data, e o arquivo onde ela entra, mas nunca a grava, nem com confirmação.
- **Data**: é a data da transição, ou seja, o dia em que a linha é gravada. Obtenha-a com
  `date +%F` imediatamente antes de montar a linha; nunca a infira da conversa nem da memória.
  Quem grava sem acesso ao Bash (o agente `arquiteto`) usa a data que recebeu de quem o
  invocou, obtida com `date +%F` no momento da invocação.
- **Status inicial**: `Proposto`. Se o usuário disser que a decisão já foi tomada, crie a ADR
  com `Proposto` e mostre a linha `Aceito`, na mesma data, para o usuário gravar.

## Regras centrais

1. **Imutabilidade.** Uma ADR em `Proposto` pode ser editada livremente (Fluxo C). A partir de
   `Aceito`, a única alteração permitida é acrescentar uma nova linha de status. Em status
   terminal (`Rejeitado`, `Descontinuado`, `Substituído`), nenhuma alteração. Linhas de status
   já existentes nunca são editadas, e editar o conteúdo não acrescenta linha. Se uma decisão
   aceita mudar, crie uma ADR nova que a substitua.

2. **Uma decisão por ADR.** Se o usuário descrever várias decisões, proponha dividi-las em ADRs
   separadas. Exceção única: a **ADR de base** do projeto (título `Base do projeto: <stack> com
   <perfil>`), proposta pelo agente `arquiteto` no fluxo `/fundacao`, reúne stack, perfil,
   ferramentas, CI e Dockerfile, porque são escolhidos, verificados e lidos juntos. Não divida
   essa ADR nem use o título `Base do projeto:` em outra.

3. **Mantenha-a curta.** Uma ADR costuma ter de meia a uma página. Se estiver crescendo demais,
   o contexto provavelmente está fazendo um trabalho que pertence a documentos de design.

4. **Referências estáveis.** O texto da ADR deve ser compreensível por si mesmo. Se precisar
   citar algo, cite apenas o que não muda com facilidade:
   - **pode citar:** outras ADRs pelo número, padrões e especificações públicas, documentação
     oficial versionada;
   - **não pode citar:** caminhos de código, números de linha, branches, arquivos temporários,
     conversas.

## Fluxo A: criar uma ADR

### 1. Reúna a decisão

Extraia da conversa, ou peça ao usuário: o que foi decidido; o problema ou as forças que
tornaram a decisão necessária (requisitos, restrições, trade-offs); as alternativas
consideradas e por que foram descartadas; as consequências, positivas e negativas, aceitas.
Se a decisão já foi discutida na conversa, puxe os detalhes de lá e confirme com o usuário em
vez de perguntar tudo de novo. Só pergunte sobre o que realmente estiver faltando.

### 2. Determine o número

O número é o maior `NNNN` dos arquivos `NNNN-slug.md` em `docs/adr/` + 1, com 4 dígitos (números
nunca são reaproveitados). Se a pasta não existir, o número é `0001` e `docs/adr/` entra no
relatório como arquivo a criar.

### 3. Nomeie o arquivo

Formato: `NNNN-slug.md`. O slug é derivado do título: minúsculas, sem acentos nem cedilha,
palavras separadas por hífen, curto e descritivo. Ex.: "Usar PostgreSQL para persistência" →
`0001-usar-postgresql-para-persistencia.md`.

### 4. Preencha o template

O template `assets/template-adr.md`, nesta pasta da skill, é a única fonte da estrutura e das
orientações por seção. Além do que está nele:

- a estrutura é fixa: não adicione, renomeie, reordene nem remova seções;
- todos os placeholders `[...]` devem ser substituídos;
- `Positivas:` e `Negativas:` têm ao menos um item cada;
- **Alternativas consideradas** é obrigatória. Se nenhuma alternativa séria foi considerada,
  escreva `- Nenhuma alternativa séria foi considerada — [motivo].`
- **Diretrizes** são numeradas e citadas por outros artefatos como `ADR NNNN/d<n>` (ex.:
  `ADR 0003/d2`). Sem regra verificável, escreva `Nenhuma.`; **Verificação** então fica
  `Não se aplica.`

Depois, grave com `Proposto` e apresente a ADR, conforme o *Princípio de gravação*.

### 5. Atualize o índice

Ao gravar a ADR, acrescente uma linha ao índice `docs/adr/README.md`, em ordem de número:

```
| NNNN | [Título](NNNN-slug.md) | <status atual> | AAAA-MM-DD |
```

Se o índice não existir, crie-o com o título `# ADRs` e o cabeçalho
`| Número | Título | Status | Data |`, e informe-o no relatório como arquivo a criar.

## ADRs existentes (Fluxos B e C)

Nos dois fluxos, comece identificando a ADR e seu status atual (a última linha da seção Status).

### Fluxo B: mudar o status

1. Confira se a transição é válida pelo diagrama do *Ciclo de vida*. Se não for (ex.:
   `Rejeitado` → `Aceito`), recuse e explique; para retomar uma decisão rejeitada, proponha uma
   ADR nova.
2. Para `Rejeitado` ou `Descontinuado`, obtenha o motivo com o usuário. Mostre a linha a
   acrescentar, obtenha aprovação e grave-a; atualize também o status e a data da linha
   correspondente em `docs/adr/README.md`.
3. Para `Aceito`, mostre ao usuário a linha exata (`- Aceito — AAAA-MM-DD`), o arquivo da ADR
   e a linha do índice a atualizar. O usuário grava as duas à mão. Depois, confira a última
   linha da seção Status (ex.: `grep -A20 "^## Status" <arquivo>`).
4. Para substituição, são duas etapas:
   - crie a ADR nova pelo Fluxo A, com `— substitui ADR-NNNN` na primeira linha de status;
   - quando o usuário aceitar a ADR nova, ele grava `Aceito` nela e
     `Substituído por ADR-NNNN` na antiga, e atualiza as duas linhas do índice. Mostre as
     quatro linhas e os arquivos, como no passo 3.

### Fluxo C: editar o conteúdo

1. Só ADRs em `Proposto` podem ser editadas; nos demais casos, recuse pela regra de
   *Imutabilidade*. Se a ADR substitui outra e a substituição deixar de fazer sentido, rejeite-a
   (Fluxo B) e crie outra.
2. Aplique as orientações do Fluxo A, passo 4.
3. Se a edição transformar a ADR em outra decisão, ou acrescentar uma segunda, aplique a regra
   *Uma decisão por ADR* e proponha uma ADR nova.
4. Se o título mudar, renomeie o arquivo para `NNNN-novo-slug.md`, mantendo o número, e informe
   no relatório nome antigo → nome novo. Ajuste título e link em `docs/adr/README.md`.
5. Grave e mostre cada trecho alterado no formato antes/depois (se a mudança for extensa, a ADR
   completa), conforme o *Princípio de gravação*.

## Exemplos

Para referência de uma ADR preenchida e de uma substituição, leia `assets/exemplo-adr.md`.
