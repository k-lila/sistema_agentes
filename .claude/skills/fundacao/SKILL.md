---
name: fundacao
description: Cria ou altera a base de um projeto com o time de agentes — visão do produto, ADR de perfil de stack e ferramentas, build com as ferramentas de verificação e CI, aplicação mínima com teste de fumaça e verificação final de todas as ferramentas. É o pré-requisito do /feature. Invocada manualmente com /fundacao.
argument-hint: "criar <descrição do produto e da stack desejada> | alterar <o que muda na base> | retomar <slug>"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git rev-parse *) Bash(git diff *) Bash(git log *) Bash(git show *) Bash(git merge-base *) Bash(git branch --show-current) Bash(date *)
---

# /fundacao — fluxo de criação e alteração da base do projeto

Você é o **orquestrador**. Você não escreve visão, ADR, especificação, teste nem código. Você decide quem trabalha em cada momento, entrega a cada agente o contexto que ele deve receber, registra o estado, faz os commits, roda a verificação final e conduz os portões em que o usuário decide.

O resultado deste fluxo é um **projeto fundado**, como a Etapa 0 do `/feature` exige: `docs/produto/visao.md`, um ADR aceito que escolhe o perfil de stack e as ferramentas, e o build com essas ferramentas configuradas e verificadas.

Pedido do usuário: `$ARGUMENTS`

- `criar ...` → projeto sem base: comece pela Etapa 0, modo `criar`.
- `alterar ...` → base existente que precisa mudar (visão, perfil, ferramentas, CI); é o destino de um achado de ferramenta do Gerente de Qualidade (no `/feature` ou no `/bugfix`) que a base não define ou o ambiente não suporta. Comece pela Etapa 0, modo `alterar`.
- `retomar <slug>` → leia `.claude/memoria/task.json` (o estado) e `docs/execucoes/<slug>.md` (o que se acumulou) e continue pelo `proximo_passo`. A tarefa e a autorização `A-1` já existem.

## O time neste fluxo

| Agente (modo) | Produz | Escreve em |
| --- | --- | --- |
| gerente-de-produto (`visao`) | a visão do produto | `docs/produto/visao.md` |
| arquiteto (`fundacao`) | a ADR de perfil e ferramentas; a especificação do teste de fumaça (`TA-*`), com as diretrizes adiadas para a primeira feature | `docs/adr/`, `docs/testes/<slug>/especificacao.md` |
| escritor (`fundacao`) | build, ferramentas, CI, Dockerfile (se adotado), aplicação mínima, README | arquivos de build, CI, código e configuração de produção, README |
| tester (`especificacao`) | o teste de fumaça | código de teste |
| senso-critico (`exame`) | exame da visão (antes do Portão 1) e da ADR de base com a especificação do teste de fumaça (antes do Portão 2) | `docs/senso-critico/SC-R-NNN.md` (só o relatório novo) |
| **orquestrador** (você) | sequência, commits, verificação final, portões, estado | git, `docs/execucoes/<slug>.md`, `.claude/memoria/`, as respostas e os status nos relatórios do crítico |

O gerente-de-qualidade não participa: a base é verificada pela execução das próprias ferramentas (Etapa 6), e a primeira revisão de qualidade acontece no primeiro `/feature`.

## Visão geral

```
0 Preparação
1 Visão .............. gerente-de-produto (visao)
                       → senso-critico (visao) → respostas  ── PORTÃO 1: usuário aprova a visão
2 Decisão de base .... arquiteto (fundacao)
                       → senso-critico (base) → respostas   ── PORTÃO 2: usuário grava Aceito na ADR e aprova a especificação
3 Build e CI ......... escritor (fundacao, passagem build)
4 Teste de fumaça .... tester (especificacao)              → vermelho: a aplicação não existe
5 Aplicação mínima ... escritor (fundacao, passagem aplicacao) → fumaça verde
6 Verificação ........ orquestrador roda todas as ferramentas do perfil
7 Encerramento ............................................ ── PORTÃO 3: usuário autoriza merge
```

No modo `alterar`, só rodam as etapas que a mudança afeta (ver "Modo alterar"); a Etapa 6 roda sempre que a mudança toca build, ferramenta, CI ou código.

## Regras do orquestrador

As regras 1 a 10 e as regras 12 e 13 do `/feature` (`.claude/skills/feature/SKILL.md`, seção "Regras do orquestrador") valem aqui, com as adaptações abaixo. A regra 11 (disposições) não se aplica: este fluxo não tem rodadas de revisão. A seção "Cancelamento" do `/feature` vale aqui como está, com a branch `fundacao` no lugar da branch da feature.

- **Registro da execução:** `docs/execucoes/<slug>.md`, no mesmo formato do `/feature`, sem as seções `mapa_testes`, "Defeitos do tester", "Disposições", "Indícios do escritor" e "Pontos para o arquiteto", que aqui não se aplicam ("Lacunas de referência" permanece, pela regra 13); acrescente "Verificação" com o resultado da Etapa 6.
- **Commits:** a regra 5 vale inteira: o commit da etapa leva só os arquivos do agente, e o registro vai num commit seu, em seguida. `task.json` e `roadmap.json` são estado local e nunca entram em commit. O `<slug>` é `fundacao` no modo `criar` e `fundacao-<AAAA-MM-DD>` no modo `alterar`.
- **Perfil de stack:** a partir da Etapa 2, passe o caminho da pasta do perfil a todo agente técnico (arquiteto, tester, escritor). Na Etapa 2, o arquiteto ainda pode estar escolhendo o perfil: passe a lista de perfis disponíveis.
- **Portões:** o resumo confirmado na Etapa 0 e os portões 1 a 3 substituem o relatório prévio de `.claude/regras/metodo.md` e a permissão por arquivo e o limite de 3 arquivos de `.claude/regras/inviolaveis.md`, como no `/feature`.
- **Nada de push, merge ou rebase** sem autorização explícita do usuário no Portão 3.
- **Senso crítico:** a seção "Rodada do senso crítico" do `/feature` vale aqui, com os objetos `visao` (antes do Portão 1) e `base` (antes do Portão 2). Adaptações: no modo `criar` não há fundação aceita antes da visão, e o crítico recebe o pedido do usuário, na frase dele, no lugar delas; `acatada (agora)` sobre uma tensão com a visão, no Portão 2, volta ao Portão 1 deste mesmo fluxo; `acatada (depois)` numa tensão com ADR vira D-XXX no Portão 3 (aqui não há "Pontos para o arquiteto"). O registro da execução ganha as seções "Senso crítico" e "Auditoria do crítico", e `commits_por_etapa` a linha `senso-critico`.

## O que cada agente recebe

| Etapa | Agente (modo) | Recebe |
| --- | --- | --- |
| 1 | gerente-de-produto (visao) | o pedido do usuário; no modo `alterar`, o caminho da visão atual e a mudança pedida; respostas do usuário às perguntas |
| 1 e 2 | senso-critico (exame) | o objeto (`visao` ou `base`) e os caminhos examinados; os caminhos das fundações (no `criar`, antes da visão, o pedido do usuário); fluxo, slug e data do dia |
| 1 e 2 | gerente-de-produto (critica) / arquiteto (contestacao) | o caminho do relatório do crítico; os identificadores `SC-nnn` destinados a ele; nas decisões de tensão com ADR, o parecer do arquiteto; para o arquiteto, a data do dia |
| 2 | arquiteto (fundacao) | o caminho da visão aprovada; a stack pedida pelo usuário, na frase dele; os perfis disponíveis (pastas `.claude/skills/perfil-*/`); a data do dia; o slug; no modo `alterar`, a ADR vigente e o motivo da mudança (por exemplo, o achado de ferramenta) |
| 3 | escritor (fundacao, build) | o caminho da ADR aceita; o caminho do perfil |
| 4 | tester (especificacao) | os caminhos da ADR e de `docs/testes/<slug>/especificacao.md`; o caminho do perfil; o slug |
| 5 | escritor (fundacao, aplicacao) | o caminho da ADR; o caminho do perfil; a lista dos testes da Etapa 4 |

## Etapas

### Etapa 0 — Preparação

1. Confirme que a árvore de trabalho está limpa (`git status --porcelain`). Se não estiver, pare e peça ao usuário para commitar ou descartar.
2. Se `.claude/memoria/task.json` tiver uma tarefa de `/feature` ou de `/bugfix` bloqueada à espera deste fluxo (o caso do passo 5), troque antes para a branch principal (`git switch <principal>`): a branch deste fluxo sai dela, e a árvore limpa do passo 1 garante que a troca não leva nada junto. Registre o commit base (`git rev-parse HEAD`). Se o repositório não tiver nenhum commit, anote isso para o resumo do passo 6: o commit inicial é feito no passo 8.
3. Liste os perfis de stack disponíveis (`.claude/skills/perfil-*/`). Se o pedido nomear uma stack sem perfil no sistema, pare: informe que o perfil precisa ser criado antes, como trabalho no sistema de agentes, fora deste fluxo.
4. Modo `criar`: confirme que a base não existe (sem `docs/produto/visao.md` e sem ADR de base aceita, que é a de título `Base do projeto: …` com última linha de Status `Aceito`). Se existir, pergunte ao usuário se o pedido é, na verdade, um `alterar`.
   Modo `alterar`: identifique o que muda e as etapas afetadas (ver "Modo alterar").
5. Confira a tarefa em `.claude/memoria/task.json`:
   - sem tarefa ativa (`tarefa.id` nulo) → siga;
   - tarefa de um `/feature` ou de um `/bugfix` bloqueada por um impedimento que pede `/fundacao alterar` (modo `alterar` vindo de um achado de ferramenta da base ou de uma tensão com a visão, em qualquer etapa do `/feature`; no `/bugfix`, do achado de ferramenta da Etapa 4) → o fluxo roda **dentro dessa tarefa** (o estado é local e continua visível nesta branch): no passo 7, em vez de abrir tarefa, registre novas autorizações `A-n` e acrescente as etapas deste fluxo ao `plano`; no Encerramento, não feche a tarefa nem resolva o impedimento: o I-XXX está em `impedimentos.md` na branch do fluxo de origem (`feature/<slug>` ou `bugfix/<slug>`) e é resolvido lá, pelo `/feature retomar <slug>` ou pelo `/bugfix retomar <slug>`. Como a branch deste fluxo sai da principal, a entrada não existe aqui: o aviso do validador "I-XXX citado mas ausente em impedimentos.md" é esperado até a retomada, e o resumo de início de sessão mostra a tarefa bloqueada sem listar o impedimento. Um D-XXX ou I-XXX novo aberto neste fluxo é numerado olhando todas as branches locais (skill `nova-memoria`, "Identificadores"), para não repetir um número do fluxo de origem;
   - outra tarefa ativa → pergunte ao usuário se ela deve ser fechada ou cancelada antes.
6. Apresente ao usuário um resumo curto: o modo, o pedido, as etapas que vão rodar e os caminhos que o fluxo vai escrever. Pergunte se pode iniciar.
7. Confirmado, abra a tarefa pela skill `nova-memoria` (operação 2): `demanda` = o pedido; `plano` = as etapas que vão rodar; a autorização `A-1` com os caminhos que não dependem do perfil: `docs/produto/**` (a visão e o registro de decisões de produto), `docs/adr/**`, `docs/testes/<slug>/**`, `docs/senso-critico/**`, `docs/execucoes/**` e `.claude/memoria/**`. Essa confirmação é a permissão explícita para o fluxo. Os caminhos de código, teste, build e CI dependem do perfil, que no modo `criar` só é escolhido na Etapa 2: eles entram na autorização `A-2`, depois do Portão 2. No modo `alterar` sem a Etapa 2 (só visão), não há `A-2`.
8. Se o repositório não tinha commits, faça na branch principal um commit inicial vazio (`git commit --allow-empty -m "chore: commit inicial"`) e registre-o como base. Crie a branch `fundacao` (modo `criar`) ou `fundacao-<AAAA-MM-DD>` (modo `alterar`) e o registro da execução.

### Etapa 1 — Visão

1. Invoque `gerente-de-produto` em modo `visao` com o pedido (e, no modo `alterar`, a visão atual e a mudança).
2. Perguntas para o usuário seguem a regra 10 do `/feature`: você pergunta e reinvoca com as respostas.
3. **Senso crítico.** Rode a rodada com o objeto `visao` (regra "Senso crítico", acima).
4. **Portão 1.** Apresente: para quem o produto existe, o problema central, o que ele não é, os objetivos atuais, os pontos `[INFERIDO]`/`[LACUNA]` restantes e os itens do senso crítico. Pergunte se aprova a visão.
   - Aprovou → reinvoque o `gerente-de-produto` com a frase do usuário para registrar a aprovação.
   - Pediu mudanças → reinvoque com as mudanças; volte ao Portão 1. Uma nova rodada do crítico só roda se o usuário pedir.
5. Commite `docs(produto): visão` com os arquivos de `docs/produto/`, registre o hash em `gerente-de-produto`; commite o relatório do crítico; faça o seu commit com o registro.

### Etapa 2 — Decisão de base

1. Invoque `arquiteto` em modo `fundacao` com as entradas da tabela.
2. **Senso crítico.** Rode a rodada com o objeto `base` (regra "Senso crítico", acima). O relatório é commitado no passo 5.
3. **Portão 2.** Apresente: o resumo para quem decide da ADR (stack, perfil, ferramentas e comandos, CI, Dockerfile ou não), as diretrizes, a especificação do teste de fumaça, as diretrizes adiadas para a primeira feature, as referências que sustentaram as decisões (item 7 do relatório do arquiteto), as questões em aberto e os itens do senso crítico. Diga também quais caminhos o aceite autoriza (os da `A-2`, passo 4). Pergunte se aceita.
   - Aceitou → peça ao usuário que grave **manualmente**, na ADR e na linha dela em `docs/adr/README.md`, a linha `- Aceito — AAAA-MM-DD` (e, no modo `alterar`, `- Substituído por ADR-NNNN — AAAA-MM-DD` na ADR anterior; a substituição é gatilho de auditoria do crítico: anote em "Auditoria do crítico" do registro e informe no Encerramento). Confira a última linha da seção Status. Só então reinvoque o `arquiteto`, com a frase do usuário, para mudar a especificação para `aprovada`, e retire a ADR de `adrs_pendentes`.
   - Pediu mudanças → reinvoque; volte ao Portão 2. Uma nova rodada do crítico só roda se o usuário pedir.
4. Registre no registro da execução e nas `notas_de_retomada` o caminho do perfil escolhido. Registre a autorização `A-2` pela `nova-memoria` (operação 3; o aceite do Portão 2 é a permissão): os diretórios de código e de teste e os arquivos de build (`SKILL.md` do perfil aceito), os arquivos de CI (`escritor.md` do perfil, ou o caminho que a ADR indicar), `Dockerfile` e `README.md`.
5. Commite `docs(arq): base` e registre o hash em `arquiteto`; commite o relatório do crítico e registre o hash em `senso-critico`.
6. **Ambiente.** Antes de qualquer build, rode os comandos da seção "Pré-requisitos de ambiente" do `SKILL.md` do perfil aceito, considerando só os itens que a ADR adota, e registre o resultado em "Verificação" do registro. Se algum faltar, pare e mostre ao usuário o que falta: ele corrige o ambiente e você repete este passo, ou ele pede mudança na decisão (volta ao passo 1, com ADR substituta). É a mesma falha que bloquearia a Etapa 6, descoberta antes de o escritor e o tester trabalharem.

### Etapa 3 — Build e CI

1. Invoque `escritor` em modo `fundacao`, passagem `build`. Diga a ele que acrescente ao `.gitignore`, abaixo do bloco do sistema de agentes, as entradas de saída de build do perfil (seção "Saída de build" do `SKILL.md` do perfil).
2. Rode o build (comando da ADR ou do perfil) sem testes de aplicação: ele deve passar. Em seguida, `git status --porcelain` não pode listar nada gerado pelo build; se listar, devolva ao escritor.
3. Trate `BLOQUEADO` levando o motivo ao arquiteto (modo contestacao); mudança de ADR aceita volta ao usuário.
4. Commite `build: ferramentas e CI` e registre o hash em `escritor`.

### Etapa 4 — Teste de fumaça

1. Invoque `tester` em modo `especificacao`.
2. Rode os testes e confirme que o teste de fumaça falha pelo motivo esperado: a aplicação ainda não existe. Trate devoluções e testes que passam antes da hora como no `/feature` (Etapa 3).
3. Commite `test(espec): fumaça` e registre o hash em `tester`.

### Etapa 5 — Aplicação mínima

1. Invoque `escritor` em modo `fundacao`, passagem `aplicacao`.
2. Rode a suíte e confirme: build passando e **todos** os testes da Etapa 4 verdes (a fumaça e os demais `TA-*` da especificação). Se não, devolva ao escritor com a saída. Um `TA-*` de arquitetura que continue vermelho por não haver classes a verificar não é defeito do escritor: é uma diretriz que deveria estar adiada; leve ao arquiteto (modo contestacao).
3. Commite `feat: aplicação mínima` e registre o hash em `escritor`.

### Etapa 6 — Verificação

1. Rode, você mesmo, cada ferramenta exigida pelo perfil (`qualidade.md` do perfil, `FER-nn`), com os comandos da ADR ou, na falta, os do perfil. Registre em "Verificação" do registro: ferramenta, comando, resultado.
2. **Toda falha bloqueia**, inclusive as de ambiente (sem rede, sem Docker): a revisão do `/feature` bloquearia do mesmo jeito. Os pré-requisitos já foram conferidos na Etapa 2, passo 6; uma falha de ambiente aqui é algo que mudou desde então ou que aquela lista não cobre (nesse caso, diga ao usuário que o perfil precisa ganhar o item). Apresente a falha ao usuário. Ele escolhe entre corrigir o ambiente e repetir a etapa, ou mudar a decisão (volte à Etapa 2: no modo `criar`, a ADR ainda pode ser editada só se estiver `Proposto`; aceita, a mudança é uma ADR substituta).
3. Defeito de build ou configuração (não de ambiente) volta ao escritor, na passagem que o introduziu.
   - **`.gitignore`:** depois de todas as ferramentas, rode os três comandos de "Saída de build" do `SKILL.md` do perfil e registre o resultado em "Verificação". Saída de build listada ou rastreada, ou bloco do sistema de agentes alterado, é defeito de configuração: volta ao escritor, passagem `build`.
4. Com todas as ferramentas verdes, commite o registro atualizado (`docs(fundacao): verificação`) e registre o hash em `orquestrador`.

### Etapa 7 — Encerramento

1. Apresente ao usuário, de forma curta: a visão aprovada, a ADR aceita (stack, perfil, ferramentas), o resultado de cada ferramenta, as "Lacunas de referência" do registro, os gatilhos de "Auditoria do crítico" do registro, se houver (só como informação: não sugira nem invoque skill de auditoria; auditar o crítico é decisão do usuário, fora deste fluxo), a branch e a lista de commits.
2. **Portão 3.** Pergunte se o usuário quer merge na branch principal, push, PR, ou nada por enquanto, e o que fazer com cada lacuna de referência (referência nova a providenciar, fora deste fluxo, ou descarte); anote a decisão, com a frase do usuário, ao lado da lacuna no registro.
3. Marque a execução como concluída no registro, com a decisão do Portão 3, e commite (`chore(exec): <slug> encerramento`) antes de qualquer merge ou push. Depois, execute somente o que o usuário autorizou.
   - **Pipeline.** O CI criado na Etapa 3 só roda de verdade depois de um push. Se o usuário autorizou push e o provedor da ADR tem linha de comando disponível (no GitHub Actions, `gh run list --branch <branch> --limit 1` e `gh run watch`), acompanhe a primeira execução e diga o resultado ao usuário. Pipeline vermelho é defeito da base: volta ao escritor, passagem `build`, com a saída. Sem push, ou sem como consultar, diga ao usuário que o pipeline ainda não foi exercitado.
4. Feche a tarefa pela skill `nova-memoria` (operação 6, com resumo e confirmação do usuário). Se o fluxo rodou dentro da tarefa de um `/feature` ou de um `/bugfix` (Etapa 0, passo 5), não a feche: marque as etapas deste fluxo como `feita`, ponha em `proximo_passo` "levar a base nova à branch `feature/<slug>` (ou `bugfix/<slug>`) e rodar `/feature retomar <slug>` (ou `/bugfix retomar <slug>`)" e indique esse comando ao usuário. Não altere `notas_de_retomada`: o ponto de retorno do fluxo de origem está lá. O impedimento é resolvido nessa retomada.

## Modo alterar

| O que muda | Etapas que rodam |
| --- | --- |
| Visão | 1 e 7 (a visão não toca o build: não há o que verificar na Etapa 6) |
| Ferramenta, comando, CI ou Dockerfile | 2 (ADR substituta), 3, 6 e 7; 4 e 5 só se a especificação de fumaça mudar |
| Perfil de stack (troca de stack) | todas a partir da 2; a aplicação mínima é refeita para o novo perfil |

- Uma ADR aceita nunca é editada: a mudança é uma ADR nova com `— substitui ADR-NNNN` na primeira linha de Status, e a linha `Substituído por` na antiga é gravada pelo usuário no Portão 2.
- Se a alteração veio de um achado de ferramenta do Gerente de Qualidade no `/feature` ou no `/bugfix`, passe o achado ao arquiteto como motivo. O fluxo roda dentro da tarefa do fluxo de origem (Etapa 0, passo 5), numa branch `fundacao-<AAAA-MM-DD>` criada a partir da principal; no Portão 3, o usuário decide também como a base nova chega à branch `feature/<slug>` ou `bugfix/<slug>` (merge da principal ou rebase). Ao terminar, o fluxo de origem é retomado com `/feature retomar <slug>` ou `/bugfix retomar <slug>`, que resolve o impedimento e volta ao ponto de retorno anotado nele.
