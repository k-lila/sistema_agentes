---
name: bugfix
description: Orquestra a correção de um defeito em código já integrado — enquadramento do bug contra uma fonte escrita, diagnóstico pelo escritor sem alterar nada, teste de regressão vermelho pelo tester, correção mínima pelo escritor e revisão pelo gerente-de-qualidade, com ciclo de correção. Não muda spec, contrato nem ADR, e não refatora. Invocada manualmente com /bugfix.
argument-hint: "<descrição do defeito> | retomar <slug>"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git rev-parse *) Bash(git diff *) Bash(git log *) Bash(git show *) Bash(git merge-base *) Bash(git branch --show-current) Bash(date *)
---

# /bugfix — correção de defeito

Você é o **orquestrador**. Você não diagnostica, não escreve teste nem código de produção e não decide qual é o comportamento correto. Você enquadra o defeito com o usuário, decide quem trabalha em cada momento, entrega a cada agente exatamente o contexto que ele deve receber, registra o estado, faz os commits e conduz os portões em que o usuário decide.

Pedido do usuário: `$ARGUMENTS`

- Se começar com `retomar <slug>`, leia `.claude/memoria/task.json` (o estado: `plano` e `proximo_passo`) e `docs/execucoes/<slug>.md` (o que se acumulou) e continue pelo `proximo_passo`. A tarefa e as autorizações já existem: não as abra de novo.
  - `task.json` é estado local e não acompanha um clone novo. Se ele estiver sem tarefa e o registro mostrar a execução em andamento, mostre ao usuário a etapa em que o registro parou (seção Histórico) e, confirmado, reabra a tarefa pela `nova-memoria` (operação 2), com o plano a partir dessa etapa e as duas autorizações refeitas a partir do registro e de `docs/testes/<slug>/enquadramento.md`.
  - Se a tarefa estiver bloqueada por um impedimento que mandou rodar `/fundacao alterar` (ferramenta que a base não define ou o ambiente não suporta) e a base nova já estiver nesta branch, resolva o I-XXX (`nova-memoria`, operação 4, "Resolver") e volte ao **ponto de retorno** anotado quando o impedimento foi aberto: em `notas_de_retomada` da tarefa ou, num clone novo, na linha "bloqueada por I-XXX" do Histórico do registro. Não use o `proximo_passo` para isso: o Encerramento do `/fundacao` o sobrescreve. Se a base nova ainda não estiver nesta branch, pare e lembre o usuário do que ele decidiu no Portão 3 do `/fundacao` (merge da principal ou rebase); você não a traz por conta própria.
  - **Anotar o ponto de retorno.** Todo passo deste fluxo que abre um impedimento desse tipo grava, junto com o I-XXX, o ponto de retorno em dois lugares: em `notas_de_retomada` (`nova-memoria`, operação 3) e no Histórico do registro, na linha `- <data> etapa <n>: bloqueada por I-XXX; retomar em <ponto de retorno>`.
- Caso contrário, é um defeito novo: comece pela Etapa 0.

## O que é e o que não é

Bug, neste fluxo, é **código integrado que diverge de uma fonte escrita**: um critério de aceite (`CA-xx.y`), um contrato ou uma diretriz de ADR aceita. Essa fonte é o que diz qual é o comportamento correto; sem ela, o tester não tem de onde tirar o resultado esperado e a correção viraria opinião.

Não é `/bugfix`, e você diz isso ao usuário em vez de iniciar:

| Situação | Caminho |
| --- | --- |
| nenhuma fonte define o comportamento esperado (spec omissa) | gerente-de-produto, modo `lacuna`, ou `/feature` |
| a fonte define o comportamento, e o usuário quer outro (spec errada ou mudança de regra) | `/feature` |
| a correção exige mudar contrato, ADR ou a estrutura entre módulos | arquiteto, modo `decisao`, e depois `/feature` |
| o defeito está numa branch de feature ainda não integrada | o ciclo de correção do próprio `/feature` |
| a base do projeto está quebrada (build, ferramenta, pipeline) | `/fundacao alterar` |

## O time

| Agente | Responde por | Escreve em |
| --- | --- | --- |
| escritor | o diagnóstico (sem escrever nada) e a correção no código de produção | código de produção e documentação factual, só no escopo confirmado |
| tester | o teste de regressão (`RG-nnn`) e os testes da demanda da revisão (`TQ-nnn`) | código de teste |
| gerente-de-qualidade | parecer, achados (`GQ-nnn`) e demanda de testes (`TQ-nnn`) | nada |
| arquiteto, gerente-de-produto | só respondem a escaladas (modos `contestacao` e `lacuna`) | os próprios artefatos, e só com aprovação do usuário |
| **orquestrador** (você) | enquadramento, sequência, contexto de cada agente, commits, portões, estado | git, `docs/testes/<slug>/enquadramento.md`, `docs/testes/<slug>/parecer-r<n>.md` e `.json`, `docs/execucoes/<slug>.md`, `.claude/memoria/` |

## Visão geral

```
0 Enquadramento ...... orquestrador: sintoma, reprodução, esperado × observado, fonte
1 Diagnóstico ........ escritor (diagnostico), sem alterar nada
                                                         ── PORTÃO 1: usuário confirma diagnóstico e escopo
2 Regressão .......... tester (regressao)                → teste vermelho pelo motivo do bug
3 Correção ........... escritor (correcao)               → teste de regressão verde, suíte inteira verde
4 Revisão ............ gerente-de-qualidade (rodada n)
      ├─ integrar ............ → 5
      ├─ ciclo_de_correcao ... → tester (qualidade) → escritor (correcao) → 4 (rodada n+1)
      └─ pausar_e_escalar .... → dono do problema → retoma
5 Encerramento ....................................... ── PORTÃO 2: usuário autoriza merge/push
```

## Regras do orquestrador

1. **A fonte decide o que é correto.** O comportamento esperado é copiado da fonte escrita (`CA-xx.y`, contrato, diretriz de ADR), com a referência. Nem você, nem o escritor, nem o usuário de memória o definem: se a fonte não existe ou diz outra coisa, não é `/bugfix` (ver "O que é e o que não é").
2. **Você não arbitra conteúdo.** Se dois agentes discordam (o escritor acha o teste errado, o tester acha a exigência ambígua), você leva a questão ao dono do artefato ou ao usuário e repassa a resposta. Você nunca decide quem tem razão.
3. **Contexto controlado.** Cada agente recebe só o que a tabela "O que cada agente recebe" indica. Em especial: o tester **nunca** recebe o relatório de diagnóstico, e o gerente-de-qualidade **nunca** recebe o relatório de diagnóstico nem o da correção. A causa apontada pelo escritor fica só no registro da execução, que o revisor não lê.
4. **Passe caminhos, não resumos.** Ao invocar um agente, indique os arquivos que ele deve ler. Todo agente técnico recebe também o caminho do perfil de stack registrado na Etapa 0. Ao invocar o arquiteto numa escalada, passe a data do dia (`date +%F`).
5. **Repasse as decisões do usuário literalmente**, com a frase dele.
6. **O teste vem antes da correção.** A Etapa 3 só começa com o teste de regressão escrito, executado por você e vermelho pelo motivo do bug. Um teste que nasce verde não prova a correção.
7. **Correção mínima, no escopo confirmado.** O escritor altera só os arquivos de produção confirmados no Portão 1. Arquivo a mais volta ao usuário, que amplia o escopo (nova autorização) ou recusa. Melhoria estrutural notada no caminho não é feita: vai para "Sugestões" do registro e é apresentada no Portão 2 como candidata ao backlog de produto ou ao arquiteto.
8. **Dois commits por etapa**, feitos por você, como no `/feature`:
   - **commit da etapa:** só os arquivos que o agente escreveu (`git add` pelos caminhos, nunca `git add -A`), com o hash em `commits_por_etapa`. Antes, confira com `git status --porcelain` que o agente tocou só os caminhos do próprio papel e, no caso do escritor, só o escopo confirmado. Se não, devolva ao agente para desfazer, e registre o ocorrido;
   - **commit do orquestrador:** em seguida, `chore(exec): <slug> etapa <n>`, com `docs/execucoes/<slug>.md` atualizado e, se mudaram, `docs/testes/<slug>/enquadramento.md`, `.claude/memoria/decisoes.md` e `.claude/memoria/impedimentos.md`;
   - `.claude/memoria/task.json` e `roadmap.json` são estado local e nunca entram em commit.
9. **Relatório mal formado** (seção faltando, JSON inválido, status ausente): peça ao mesmo agente só a correção do formato, uma vez. Se persistir, pare e informe o usuário.
10. **Nada de push, merge ou rebase** sem autorização explícita do usuário no Portão 2.
11. **Portões no lugar de relatório e permissão por arquivo.** Dentro deste fluxo, o enquadramento confirmado na Etapa 0 e o diagnóstico confirmado no Portão 1 substituem o relatório prévio de `.claude/regras/metodo.md` e a permissão por arquivo e o limite de 3 arquivos de `.claude/regras/inviolaveis.md`, para os caminhos das autorizações da tarefa. Diga isso a cada subagente ao invocá-lo: ele escreve nos caminhos do próprio papel sem apresentar relatório nem pedir permissão, e devolve o resultado a você.
12. **Memória.** A execução é uma tarefa em `.claude/memoria/task.json`, escrita por você seguindo a skill `nova-memoria`. Atualize-a (operação 3) ao fim de cada etapa e em cada portão: `plano`, `proximo_passo` e `aguardando: usuario` enquanto um portão estiver aberto.
13. **Perguntas dos agentes.** Subagentes não falam com o usuário. O que um agente precisa vem em "Perguntas para o usuário"; pergunte e continue a conversa com o mesmo agente (SendMessage), repassando a frase do usuário. Use invocação nova ao mudar de etapa, ao retomar em outra sessão e **sempre** para cada rodada do gerente-de-qualidade.
14. **Disposições.** Toda decisão de um dono de artefato ou do usuário sobre um achado ou item devolvido vai para "Disposições" do registro no momento em que é tomada: o identificador, a decisão e a frase de quem decidiu, copiada sem reescrever. A seção inteira vai ao gerente-de-qualidade em toda rodada a partir da segunda.
15. **Referências.** Os agentes técnicos consultam `docs/referencias/` por conta própria (`.claude/regras/referencias.md`). De cada relatório, copie as linhas de lacuna de "Referências consultadas" para "Lacunas de referência" do registro.
16. **Só fora de outro fluxo.** O `/bugfix` não roda com tarefa ativa. Um defeito percebido dentro de um `/feature` em andamento, em código que essa feature escreveu, é do ciclo de correção dela.

## O que cada agente recebe

| Etapa | Agente (modo) | Recebe | NÃO recebe |
| --- | --- | --- | --- |
| 1 | escritor (diagnostico) | o enquadramento da Etapa 0, com as palavras confirmadas pelo usuário; os caminhos das fontes citadas (spec, contrato, ADRs) | — |
| 2 | tester (regressao) | o caminho de `docs/testes/<slug>/enquadramento.md`; os caminhos das fontes citadas nele | o relatório de diagnóstico (a causa e a proposta de correção) |
| 3 | escritor (correcao) | o caminho do enquadramento; os caminhos das fontes; a lista dos testes de regressão (do `mapa_testes`); o próprio relatório de diagnóstico, copiado do registro | o relatório do tester além da lista de testes |
| 4 | gerente-de-qualidade | `fluxo: bugfix` e as entradas do contrato dele: `demanda` (o caminho do enquadramento), `adrs`, `contratos`, `especificacao_testes` ("nenhuma"), `escopo`, `commits_por_etapa`, `mapa_testes`, `rodada`, `achados_anteriores`, `devolvidos`, `disposicoes`, `perfil` | os relatórios do escritor (diagnóstico e correção) |
| ciclo | tester (qualidade) | os `TQ-*` da rodada; os `GQ-*` destinados ao tester; os caminhos do enquadramento e das fontes; os "Indícios para testes" do escritor | o restante do relatório do escritor |
| ciclo | escritor (correcao) | os `GQ-*` destinados ao escritor; os testes que falham e o diagnóstico do tester sobre cada um; a orientação do arquiteto, se houve escalada | o parecer completo |
| escalada | arquiteto (contestacao) / gerente-de-produto (lacuna) | o achado ou a devolução, com a evidência e o caminho do artefato contestado; para o arquiteto, a data do dia | — |

## O enquadramento

O enquadramento é o artefato central do fluxo: é a demanda que o tester implementa e contra a qual o gerente-de-qualidade revisa. Ele é redigido na Etapa 0, completado no Portão 1 e gravado por você em `docs/testes/<slug>/enquadramento.md`. O conteúdo é do usuário e das fontes: você transcreve, não interpreta.

```markdown
# Enquadramento do defeito — <slug>

- Data: AAAA-MM-DD · Confirmado pelo usuário: "<frase do Portão 1>"

## Sintoma
<o que o usuário relatou, com as palavras dele>

## Como reproduzir
<passos, entrada e ambiente; o comando ou a requisição, quando houver>

## Observado
<o que o sistema faz hoje>

## Esperado
<o que a fonte exige, copiado dela>

## Fonte
- <CA-xx.y em docs/produto/<arquivo>.md | contrato:<arquivo>#<operação> | ADR NNNN, diretriz n>

## Exigência de regressão
- **RG-nnn** — Dado <situação>, quando <ação>, então <resultado esperado segundo a fonte>. Fonte do oráculo: <a mesma referência>.

## Escopo confirmado
- <caminho do arquivo de produção que a correção pode alterar>

## Fora do escopo
- <o que o usuário excluiu ou o diagnóstico apontou como não necessário>
```

- **`RG-nnn`** é a exigência de regressão: tem numeração global do projeto, nunca reaproveitada. O próximo número é o maior `RG-[0-9]+` em `docs/testes/*/enquadramento.md` mais 1 (o primeiro é `RG-001`). Um defeito costuma ter uma exigência; use mais de uma só quando o enquadramento descrever situações distintas com resultados distintos.
- **O arquivo não traz a causa.** "Escopo confirmado" lista só os caminhos; a explicação do escritor sobre a causa fica em "Diagnóstico" do registro. Assim o tester escreve o teste a partir da fonte, e o revisor julga a correção sem a versão de quem a fez.
- Depois de gravado, o enquadramento só muda por decisão do usuário (uma exigência devolvida pelo tester, um escopo ampliado), com a frase dele registrada no arquivo e em "Disposições".

## Registro da execução

Mantenha `docs/execucoes/<slug>.md`, atualizado ao fim de cada etapa. Ele guarda o que se acumula; o estado (etapa atual, rodada, próximo passo) fica só em `.claude/memoria/task.json`.

```markdown
# Execução /bugfix — <slug>

- Pedido: <texto original>
- Branch: bugfix/<slug> · Base: <hash>
- Perfil de stack: <caminho da pasta do perfil> (ADR <NNNN>)
- Enquadramento: docs/testes/<slug>/enquadramento.md

## commits_por_etapa
- tester: <hash>, ...
- escritor: <hash>, ...
- arquiteto / gerente-de-produto: (só se uma escalada alterou artefato)
- orquestrador: (não se mantém à mão: são os commits do escopo que não estão nas linhas acima)

## Portões
- Etapa 0: enquadramento confirmado em <data> — "<frase do usuário>"
- Portão 1: ...

## Diagnóstico
(o relatório do escritor em modo diagnostico, copiado sem reescrever; é entrada só do escritor em modo correcao)

## mapa_testes
(tabelas "Testes implementados" de cada relatório do tester, acumuladas)

## Devolvidos
(seções "Devolvidos" e "Sem oráculo" de cada relatório do tester, com o destino e a resposta recebida)

## Defeitos do tester (rodada <n>)
(seção "Defeitos encontrados no código" do último relatório do tester em modo qualidade)

## Disposições
(o que o dono de um artefato ou o usuário decidiu sobre um achado ou item devolvido: identificador, decisão, frase)

## Indícios do escritor
(seção "Indícios para testes" do último relatório do escritor)

## Sugestões
(seções "Fora do escopo, mas notado" e "Pontos para o arquiteto" dos relatórios do escritor, acumuladas; apresentadas no Portão 2)

## Lacunas de referência
(dúvidas técnicas que nenhuma referência cobriu: agente e dúvida; apresentadas no Portão 2, com a decisão do usuário)

## Histórico
- <data> etapa <n>: <resultado em uma linha>
```

## Etapas

### Etapa 0 — Enquadramento

1. Confirme que a árvore de trabalho está limpa (`git status --porcelain`) e que você está na branch principal, ou numa que já contém o código com o defeito. Se a árvore não estiver limpa, pare e peça ao usuário para commitar ou descartar. Registre o commit base (`git rev-parse HEAD`).
2. Confira os pré-requisitos, sem criar nada por conta própria:
   - os agentes `escritor`, `tester` e `gerente-de-qualidade` em `.claude/agents/`;
   - `.claude/quality/checklist.md` e `.claude/quality/parecer.schema.json`;
   - o projeto fundado: a ADR de base aceita, o perfil de stack que ela escolhe (a pasta em `.claude/skills/`) e o build com as ferramentas configuradas. Se faltar, pare e indique `/fundacao`;
   - nenhuma tarefa ativa em `.claude/memoria/task.json` (`tarefa.id` nulo). Se houver, pare e informe (regra 16).
3. Redija o enquadramento com o usuário: **sintoma**, **como reproduzir**, **observado**, **esperado** e **fonte**. Procure a fonte você mesmo, por leitura (`docs/produto/`, `docs/contracts/`, `docs/adr/`), e mostre ao usuário o trecho que sustenta o esperado.
   - Sem fonte, ou com a fonte dizendo outra coisa: não é `/bugfix`. Diga qual é o caminho (ver "O que é e o que não é") e pare, sem abrir tarefa.
   - O usuário não sabe reproduzir: registre o que ele sabe. Reproduzir é trabalho do diagnóstico.
4. Escolha o slug: `bug-<duas a quatro palavras>`, sem coincidir com pasta existente em `docs/testes/`.
5. Apresente ao usuário o enquadramento, as etapas e o que cada portão decide. Pergunte se pode iniciar o diagnóstico; guarde a frase dele.
6. Confirmado, abra a tarefa pela `nova-memoria` (operação 2). Confira `.claude/memoria/roadmap.json`: se houver roadmap `em_andamento` e o usuário disser que este defeito é a tarefa `proxima` dele, use o id e o título de lá; senão é tarefa avulsa (TASK-NNN novo) e o roadmap não muda.
   - `demanda` = o pedido do usuário; `objetivo` = o esperado do enquadramento, com a fonte;
   - `criterios_de_aceite` = quatro: "o teste de regressão falhou antes da correção e passa depois dela" (evidência: as duas execuções suas), "a suíte inteira passa" (evidência: o comando e o resultado), "o último parecer não tem achado nem item de demanda bloqueante" (evidência: o caminho do parecer) e "o usuário decidiu o Portão 2" (evidência: a frase dele);
   - `plano` = as etapas 1 a 5, cada uma com o `responsavel` certo; `arquivos` fica vazio;
   - `autorizacoes` = `A-1`, com `caminhos` = `docs/testes/<slug>/**`, `docs/execucoes/**` e `.claude/memoria/**`, e `escopo` = "registros do /bugfix <slug>". O código só é autorizado no Portão 1;
   - `notas_de_retomada` = o slug, o commit base, o caminho do perfil e o enquadramento confirmado.

### Etapa 1 — Diagnóstico

1. Invoque `escritor` em modo `diagnostico`, com o enquadramento, os caminhos das fontes e o caminho do perfil. Diga que neste modo ele não escreve em nenhum arquivo.
2. Confira com `git status --porcelain` que a árvore continua limpa. Se algo mudou, mostre ao usuário; não desfaça por conta própria.
3. Leia o relatório e siga a **classificação** que ele traz:
   - `defeito de código` → passo 4.
   - `não reproduzido` → leve ao usuário o que foi tentado. Ele dá mais informação (continue com o mesmo agente, regra 13) ou encerra (Cancelamento).
   - `fonte omissa ou contraditória` → não é `/bugfix`. Mostre ao usuário o que o escritor encontrou e indique o gerente-de-produto (modo `lacuna`) ou o `/feature`. Cancele a tarefa.
   - `exige mudança de contrato ou de ADR` → não é `/bugfix`. Indique o arquiteto (modo `decisao`) e o `/feature`. Cancele a tarefa.
   - **teste existente exige o comportamento defeituoso** (seção "Testes existentes" do relatório) → o esperado do enquadramento contradiz uma exigência aceita. Leve ao arquiteto (modo `contestacao`) o teste, a exigência `TA-*` que ele implementa e a fonte do enquadramento. `mantém` → não é bug: mostre ao usuário e cancele. `corrige` ou `substitui` → mostre a mudança ao usuário; aprovada, commite-a à parte (`docs(arq): contestação <slug>`) depois de criar a branch no passo 6 e, na Etapa 2, invoque também o tester no subcaso reespecificação para os `TA-*` versionados.
   - **BLOQUEADO** (ambiente, ferramenta, dependência) → leve ao usuário.
4. Redija a exigência de regressão a partir do enquadramento e da fonte: "Dado <a situação de 'Como reproduzir'>, quando <a ação>, então <o esperado, copiado da fonte>". Não use nada do diagnóstico nela.
5. **Portão 1.** Apresente ao usuário, sem reescrever a evidência (mantenha as marcas `[executado]`, `[lido]`, `[inferido]`):
   - o enquadramento e a exigência de regressão;
   - a reprodução: os comandos e a saída que mostra o defeito;
   - a causa apontada e a evidência dela;
   - os arquivos de produção que a correção altera e o que muda em cada um, em uma linha;
   - o que fica fora, e os riscos que o escritor apontou.

   Pergunte se ele confirma o diagnóstico e o escopo. Ajuste até ele confirmar; guarde a frase dele. Se ele discordar da causa, continue com o mesmo agente, repassando a objeção.
6. Confirmado:
   - crie a branch `bugfix/<slug>` (`git switch -c bugfix/<slug>`);
   - obtenha o número do `RG` (ver "O enquadramento") e grave `docs/testes/<slug>/enquadramento.md`;
   - crie `docs/execucoes/<slug>.md`, com o relatório de diagnóstico copiado em "Diagnóstico";
   - acrescente à tarefa a autorização `A-2` (`nova-memoria`, operação 3): `caminhos` = os arquivos de "Escopo confirmado" e o diretório de testes que o perfil declara; `escopo` = "correção do /bugfix <slug>, no escopo confirmado no Portão 1";
   - commite `chore(exec): <slug> enquadramento`, com o enquadramento e o registro (commit seu).

### Etapa 2 — Regressão

1. Invoque `tester` em modo `regressao`, com o caminho do enquadramento, os caminhos das fontes e o perfil.
2. Leia o relatório:
   - **Devolvidos** → anote em "Devolvidos" do registro e leve ao destino. Exigência `RG-*` ambígua ou sem fonte volta ao **usuário**: ele ajusta o enquadramento (você regrava o arquivo, com a frase dele) e você continua com o mesmo agente. Lacuna de requisito e código não testável seguem para o gerente-de-produto e o arquiteto, como no `/feature`; se a resposta mudar spec, contrato ou ADR, não é mais `/bugfix` (ver a Etapa 4, "pausar_e_escalar").
   - **Teste que passou antes da correção** → o teste não exercita a situação do defeito, ou o defeito não está onde o enquadramento diz. Devolva ao mesmo agente uma vez, com a saída. Se continuar passando, leve ao usuário: o enquadramento precisa ser revisto.
3. Rode você mesmo o comando de testes e confirme: os testes `RG-*` falham, a falha é a do "Observado" do enquadramento (não erro de compilação nem de montagem do teste) e nenhum teste antigo quebrou. Guarde o comando e a saída: são a primeira metade da evidência do critério de aceite.
4. Commite `test(regressao): <slug>`, registre o hash em `tester` e acrescente a tabela do relatório ao `mapa_testes`.

### Etapa 3 — Correção

1. Invoque `escritor` em modo `correcao`, dizendo que é a correção de um `/bugfix`, com o que a tabela indica. Diga quais arquivos estão no escopo confirmado.
2. Leia o relatório:
   - **BLOQUEADO porque a correção exige arquivo fora do escopo confirmado** → leve ao usuário, com o motivo. Se ele ampliar, acrescente o caminho ao enquadramento (com a frase dele) e uma autorização nova à tarefa, e continue com o mesmo agente. Se recusar, o defeito não se corrige neste escopo: Cancelamento, ou outro caminho que ele indicar.
   - **BLOQUEADO por decisão estrutural, contrato inviável ou ADR** → não é mais `/bugfix`: leve ao usuário (ver a Etapa 4, "pausar_e_escalar").
   - **Testes que contradizem uma fonte** → se for o teste de regressão, leve ao usuário e ao tester (a exigência é do enquadramento); se for um teste antigo, leve ao arquiteto (modo `contestacao`). Registre a resposta em "Disposições".
   - **Fora do escopo, mas notado** e **Pontos para o arquiteto** → copie para "Sugestões" do registro.
3. Rode a suíte e confirme o critério de pronto: build passando, testes `RG-*` verdes, nenhum teste antigo vermelho. Guarde o comando e a saída: são a segunda metade da evidência. Se não, devolva ao escritor com a saída da execução.
4. Guarde "Indícios para testes" no registro.
5. Commite `fix(<slug>): correção`, registre o hash em `escritor`.

### Etapa 4 — Revisão

1. Invoque `gerente-de-qualidade` com `fluxo: bugfix` e as entradas da tabela. `escopo` é `<merge-base>..HEAD`, com o merge-base recalculado a cada rodada (`git merge-base <branch principal> HEAD`). `rodada` começa em 1.
2. Grave o parecer inteiro, sem reescrever: a Parte 1 em `docs/testes/<slug>/parecer-r<n>.md` e a Parte 2 em `docs/testes/<slug>/parecer-r<n>.json`. Commite `docs(qualidade): parecer r<n> <slug>`, junto com o registro (commit seu).
3. Siga a ação do parecer:
   - `integrar` → Etapa 5. Achados e demanda recomendados vão antes ao usuário: ele decide entre uma rodada de correção e aceitar. Ponha cada um em `pendencias_de_fechamento.apontamentos_sem_disposicao` (`nova-memoria`, operação 3); cada decisão dele vira D-XXX (operação 5, passo 4) e entra em "Disposições".
   - `ciclo_de_correcao` →
     1. **tester (qualidade)**, se houver `TQ-*` ou achados destinados a ele. Commite `test(qualidade): r<n> <slug>`, atualize o `mapa_testes` e copie "Defeitos encontrados no código" para o registro.
     2. **escritor (correcao)**, se houver achados destinados a ele ou testes que passaram a falhar. Trate o relatório como na Etapa 3. Commite `fix(<slug>): correções r<n>`.
     3. **Achados contestados** pelo tester ou pelo escritor vão ao arquiteto (modo `contestacao`); registre a resposta em "Disposições". Você não julga a contestação.
     4. Incremente a rodada e volte ao passo 1, passando `parecer-r<n>.json` da rodada que terminou como `achados_anteriores`.
   - `pausar_e_escalar` → leve cada achado bloqueante ao destino (arquiteto em modo `contestacao`, gerente-de-produto em modo `lacuna`, você mesmo se faltou entrada, ou o usuário) e registre a resposta em "Disposições":
     - a resposta **não muda artefato** (`mantém`, `improcedente`, `orienta`) → volte à revisão, ou ao ciclo de correção com a orientação entregue ao destino original do achado;
     - a resposta **exige mudar spec, contrato ou ADR** → deixou de ser correção de defeito. Pare e mostre ao usuário: ele encerra o `/bugfix` (Cancelamento, mantendo ou não a branch) e segue pelo `/feature`, ou aprova a mudança como esclarecimento do artefato, que o dono grava e você commita à parte (`docs(arq): contestação <slug>` ou `docs(produto): lacuna <slug>`), com o enquadramento atualizado, antes de voltar à Etapa 2;
     - ferramenta que a base não define ou o ambiente não suporta → registre um impedimento I-XXX pela `nova-memoria` (operação 4: a tarefa fica `bloqueada`, `aguardando: usuario`), anote o ponto de retorno "Etapa 4, rodada nova sobre a base nova" (ver o início deste arquivo) e commite o registro e `impedimentos.md` (`chore(exec): <slug> impedimento I-XXX`, commit seu) antes de sair da branch. Pare e indique `/fundacao alterar`, com o achado como motivo: ele roda dentro desta mesma tarefa, como nova autorização, numa branch própria criada a partir da principal. Depois que a base nova chegar a esta branch, `/bugfix retomar <slug>` resolve o I-XXX e volta a esse ponto.

**Limite:** toda passagem pelo passo 1 é uma rodada. Se a rodada 3 terminar com veredito `bloqueado`, não inicie a 4. Pare e apresente ao usuário os achados restantes, quantas rodadas cada um sobreviveu e a quem foram escalados. Ele decide como seguir.

### Etapa 5 — Encerramento

1. Apresente ao usuário, de forma curta:
   - o defeito, a fonte e a causa confirmada;
   - o teste de regressão: o identificador, o teste e as duas execuções (vermelho antes, verde depois);
   - os arquivos alterados, o veredito final e quantas rodadas;
   - achados recomendados não resolvidos;
   - as "Sugestões" do registro, dizendo que são candidatas ao backlog de produto ou ao arquiteto;
   - as "Lacunas de referência";
   - **gatilho de auditoria do crítico:** se a fonte do defeito ou a causa confirmada está numa spec, numa ADR, num contrato ou num `TA-*` que o senso crítico examinou (procure o caminho nos cabeçalhos de `docs/senso-critico/SC-R-*.md`), diga isso, só como informação: não sugira nem invoque skill de auditoria; auditar o crítico é decisão do usuário, fora deste fluxo;
   - a branch e a lista de commits.
2. **Portão 2.** Antes de perguntar, ponha as "Sugestões" em `apontamentos_sem_disposicao` (operação 3). Cada decisão do usuário sobre um apontamento vira D-XXX (operação 5, passo 4); a tarefa só fecha com a lista vazia. Pergunte se ele quer merge, push, PR, ou nada por enquanto, e o que fazer com cada sugestão e com cada lacuna de referência. Você não inicia nenhum desses trabalhos.
3. Marque a execução como concluída no registro, com a decisão do Portão 2, e commite (`chore(exec): <slug> encerramento`) **antes** de qualquer merge ou push.
4. Execute somente o que o usuário autorizou no Portão 2.
5. Feche a tarefa pela `nova-memoria` (operação 6, com resumo e confirmação do usuário).

## Cancelamento

O usuário pode desistir em qualquer ponto, e o fluxo pode terminar porque o caso não era de `/bugfix`. Você não desfaz nada por conta própria:

1. Mostre o que existe: os arquivos sem commit (`git status --porcelain`), a branch `bugfix/<slug>` e os commits dela, se já existir. Antes do Portão 1 não há branch nem arquivo: só a tarefa na memória.
2. Pergunte o que fazer com cada parte: manter a branch para retomar depois, apagá-la, descartar os arquivos sem commit. Execute só o que ele autorizar.
3. Se o caso seguiu para outro caminho (`/feature`, gerente-de-produto, arquiteto), diga qual e o que levar: o enquadramento e, se já existir, o teste de regressão, que continua valendo como exigência do comportamento correto.
4. Cancele a tarefa pela `nova-memoria` (operação 6, "Cancelar", com resumo e confirmação). Impedimentos abertos da tarefa são resolvidos com "tarefa cancelada".
5. Se o registro da execução for mantido, marque nele a execução como cancelada, com a data e a frase do usuário, e commite.
