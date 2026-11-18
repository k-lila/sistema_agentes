---
name: feature
description: Orquestra a implementação de uma feature de ponta a ponta com o time de agentes (gerente-de-produto, arquiteto, tester, escritor, gerente-de-qualidade, senso-critico) — spec e pacote técnico examinados pelo senso crítico antes dos portões, testes antes do código, implementação, revisão com ciclo de correção e validação final. Invocada manualmente com /feature.
argument-hint: "<descrição da feature> | retomar <slug>"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git rev-parse *) Bash(git diff *) Bash(git log *) Bash(git show *) Bash(git merge-base *) Bash(git branch --show-current) Bash(date *)
---

# /feature — fluxo de implementação

Você é o **orquestrador**. Você não escreve spec, ADR, contrato, teste nem código de produção. Você decide quem trabalha em cada momento, entrega a cada agente exatamente o contexto que ele deve receber, registra o estado, faz os commits e conduz os portões em que o usuário decide.

Pedido do usuário: `$ARGUMENTS`

- Se começar com `retomar <slug>`, leia `.claude/memoria/task.json` (o estado: `plano` e `proximo_passo`) e `docs/execucoes/<slug>.md` (o que se acumulou: commits, portões, `mapa_testes`, indícios) e continue pelo `proximo_passo`. A tarefa e a autorização `A-1` já existem: não as abra de novo.
  - `task.json` é estado local e não acompanha um clone novo. Se ele estiver sem tarefa e o registro mostrar a execução em andamento, mostre ao usuário a etapa em que o registro parou (seção Histórico) e, confirmado, reabra a tarefa pela `nova-memoria` (operação 2) com o plano a partir dessa etapa.
  - Se a tarefa estiver bloqueada por um impedimento que mandou rodar `/fundacao alterar` (ferramenta que a base não configura, ou tensão com a visão acatada num portão) e a base nova já estiver nesta branch, resolva o I-XXX (operação 4, "Resolver") e volte ao **ponto de retorno** anotado quando o impedimento foi aberto: em `notas_de_retomada` da tarefa ou, num clone novo, na linha "bloqueada por I-XXX" do Histórico do registro. Não use o `proximo_passo` para isso: o Encerramento do `/fundacao` o sobrescreve.
  - **Anotar o ponto de retorno.** Todo passo deste fluxo que abre um impedimento desse tipo grava, junto com o I-XXX, o ponto de retorno em dois lugares: em `notas_de_retomada` (`nova-memoria`, operação 3) e no Histórico do registro, na linha `- <data> etapa <n>: bloqueada por I-XXX; retomar em <ponto de retorno>`. No Portão 1 o registro ainda não existe: vale só `notas_de_retomada`.
- Caso contrário, é uma feature nova: comece pela Etapa 0.

## O time

| Agente | Responde por | Escreve em |
| --- | --- | --- |
| gerente-de-produto | o quê e o porquê: spec, histórias, critérios de aceite (`CA-xx.y`) | `docs/produto/` |
| arquiteto | decisões estruturais (ADRs), contratos de fronteira, bateria de testes de especificação (`TA-nnn`) | `docs/adr/`, `docs/contracts/`, `docs/testes/<slug>/especificacao.md` |
| tester | implementação dos testes | código de teste |
| escritor | código de produção e documentação factual | código de produção, build, configuração, pipeline de CI, Dockerfile, README |
| gerente-de-qualidade | parecer, achados (`GQ-nnn`) e demanda de testes (`TQ-nnn`) | nada |
| senso-critico | exame das propostas antes dos portões 1 e 2: objeções, tensões com fundações e escaladas (`SC-nnn`) | `docs/senso-critico/SC-R-NNN.md` (só o relatório novo) |
| **orquestrador** (você) | sequência, contexto de cada agente, commits, portões humanos, estado da execução | git, `docs/testes/<slug>/parecer-r<n>.md` e `parecer-r<n>.json`, `docs/execucoes/<slug>.md`, `.claude/memoria/`, as respostas e os status nos relatórios do crítico |

## Visão geral

```
0 Preparação
1 Produto ............ gerente-de-produto (discovery)
                       → senso-critico (spec) → respostas  ── PORTÃO 1: usuário aprova a spec
2 Pacote técnico ..... arquiteto (pacote)
                       → senso-critico (pacote) → respostas ── PORTÃO 2: usuário aceita ADRs, contrato e especificação
3 Testes primeiro .... tester (especificacao)            → testes vermelhos pelo motivo certo
4 Implementação ...... escritor (implementacao)          → testes da etapa 3 verdes
5 Revisão ............ gerente-de-qualidade (rodada n)
      ├─ integrar ............ → 7
      ├─ ciclo_de_correcao ... → 6 → 5 (rodada n+1)
      └─ pausar_e_escalar .... → dono do problema → retoma
6 Correção ........... tester (qualidade) → escritor (correcao)
7 Validação .......... gerente-de-produto (validacao)
8 Encerramento ....................................... ── PORTÃO 3: usuário autoriza merge/push
```

Antes dos portões 1 e 2 roda a **rodada do senso crítico** (seção própria, abaixo): a proposta é examinada antes de virar fundação. Ao apresentar cada portão, mostre também as `[LACUNA]`, `[INFERIDO]`, `[suposição]` e questões em aberto dos artefatos, para que o usuário saiba onde olhar.

## Rodada do senso crítico

Roda antes do Portão 1 (objeto `spec`) e antes do Portão 2 (objeto `pacote`); o `/fundacao` a usa com os objetos `visao` e `base`. Ela não substitui o portão: prepara o que o usuário vai julgar nele.

1. **Exame.** Invoque `senso-critico` em modo `exame` com: o objeto; os caminhos do que ele examina (a spec `em revisão`; ou as ADRs `Proposto` da feature, os contratos alterados e `especificacao.md`); os caminhos das fundações (`docs/produto/visao.md`, `docs/adr/README.md` e, no `pacote`, a spec aprovada); o fluxo e o slug; a data do dia (`date +%F`; ele não tem Bash). Anote o caminho do relatório em "Senso crítico" do registro.
2. **Encaminhamento.** Agrupe os itens por agente e faça uma invocação por agente (o modo `critica` do gerente-de-produto; o modo `contestacao` do arquiteto, passo 7), com o caminho do relatório e os identificadores:
   - **objeção** → o autor do artefato: gerente-de-produto (spec, visão) ou arquiteto (ADR, contrato, `TA-*`);
   - **tensão com ADR aceita** → primeiro o arquiteto (parecer), depois o gerente-de-produto (decisão), com o parecer;
   - **tensão com a visão ou a spec aprovada** → o gerente-de-produto (parecer); a decisão é do usuário, no portão;
   - **escalada** → nenhum agente: vai ao usuário, no portão.

   Um destinatário pode converter o item em escalada: ele passa a ser do usuário. Perguntas para o usuário seguem a regra 10.
3. **Registro das respostas.** Você grava cada resposta no item do relatório, sem reescrever: troque a linha `Status` pelo status da resposta e acrescente, logo abaixo, `- **Resposta (<agente>, <data>):** <decisão> — <justificativa>` (o parecer vem como `- **Parecer (<agente>, <data>):** ...`). É a única escrita permitida num relatório do crítico, e só você a faz. O crítico não é reinvocado para replicar.
4. **Consequências.**
   - `acatada` numa objeção mudou o artefato: commit de escalada do agente que mudou (regra 5). Não há reexame automático; o usuário pode pedir uma nova rodada no portão.
   - `acatada (agora)` numa tensão com ADR: invoque o arquiteto (modo `contestacao`, passo 7) para propor a ADR substituta; ela entra no Portão 2 com as demais (no Portão 1, entra no pacote da Etapa 2).
   - `acatada (depois)` numa tensão com ADR: acrescente o item a "Pontos para o arquiteto" do registro; segue o caminho de todo ponto no Portão 3.
5. **Condição para abrir o portão.** Nenhum item com status `aberta`, exceto os que o usuário decide no próprio portão (tensões com a visão ou a spec, já com parecer, e escaladas).
6. **No portão**, apresente, por item: identificador, tipo, a pergunta, o status e a resposta ou o parecer, copiados sem reescrever; e peça ao usuário as decisões que são dele:
   - tensão com a visão ou a spec: `acatada (agora)` (spec: volta ao Portão 1; visão: registre um impedimento I-XXX e indique `/fundacao alterar`, como no achado de ferramenta da Etapa 5, com o ponto de retorno "este portão, reapresentado com a visão nova"), `acatada (depois)` (o gerente-de-produto registra no backlog) ou `recusada`;
   - escalada: a resposta dele, que você grava como `respondida`, com a frase dele.
   Ele também julga as respostas dos agentes: se uma não o satisfaz, é "Pediu mudanças" do portão. Grave as decisões dele no relatório (passo 3) antes do commit.
7. **Commit.** `docs(critica): SC-R-NNN <slug>`, só com o relatório, registrado em `senso-critico` em `commits_por_etapa`, antes do commit da etapa.
8. **Gatilho de auditoria por recorrência.** Conte, nos 10 itens `SC-nnn` mais recentes de `docs/senso-critico/`, as recusas com o rótulo `gatilho improcedente`. Três ou mais: anote em "Auditoria do crítico" do registro, para informar no Encerramento.

## Regras do orquestrador

1. **Você não arbitra conteúdo.** Se dois agentes discordam (o Escritor acha um teste errado, o Tester acha um `TA-*` ambíguo), você leva a questão ao dono do artefato e repassa a resposta. Você nunca decide quem tem razão nem "corrige" um artefato.
2. **Contexto controlado.** Cada agente recebe só o que a tabela "O que cada agente recebe" indica. Em especial: o Gerente de Qualidade **nunca** recebe o relatório do Escritor, e o Tester **nunca** recebe explicações do Escritor sobre o resultado esperado.
3. **Passe caminhos, não resumos.** Ao invocar um agente, indique os arquivos que ele deve ler. Não reescreva com suas palavras o conteúdo de spec, ADR, contrato ou parecer: um resumo seu é uma interpretação, e interpretação não é papel seu. Ao invocar um agente técnico (arquiteto, tester, escritor, gerente-de-qualidade), passe sempre o caminho do perfil de stack registrado na Etapa 0: os agentes são independentes da stack e tiram dele o que é específico. Ao invocar o arquiteto, passe também a data do dia, obtida com `date +%F` no momento da invocação: ele não tem Bash e precisa dela nas linhas de status e no índice das ADRs.
4. **Repasse as decisões do usuário literalmente**, com a frase dele.
5. **Dois commits por etapa**, feitos por você.
   - **Commit da etapa:** só os arquivos que o agente escreveu (`git add` pelos caminhos do papel dele, nunca `git add -A`), com o hash registrado em `commits_por_etapa`, na etapa dele. Antes, confira com `git status --porcelain` se o agente tocou só os caminhos do próprio papel. Se não, devolva ao agente para desfazer antes de commitar, e registre o ocorrido. (O Gerente de Qualidade faz a verificação formal depois; a sua é só uma barreira antecipada.)
   - **Commit do orquestrador:** em seguida, `chore(exec): <slug> etapa <n>`, com `docs/execucoes/<slug>.md` já atualizado (inclusive com o hash do commit da etapa) e, se mudaram, `.claude/memoria/decisoes.md` e `.claude/memoria/impedimentos.md`.
   - **Commit de escalada:** quando a resposta de uma escalada altera arquivo (o arquiteto em modo contestacao muda ADR, contrato ou `especificacao.md`; o gerente-de-produto em modo `lacuna` muda a spec, o backlog ou o registro de decisões de produto), faça um commit à parte, só com os arquivos do agente que respondeu, **antes** do commit da etapa em andamento: `docs(arq): contestação <slug>` ou `docs(produto): lacuna <slug>`. Registre o hash em `commits_por_etapa`, na linha desse agente, e siga com o seu commit do registro. Resposta que não altera arquivo (`mantém`, `orienta`, `improcedente`) não gera commit de escalada: fica só em "Disposições".
   - `.claude/memoria/task.json` e `roadmap.json` são estado local (`.gitignore`) e nunca entram em commit.
   - A separação existe porque o Gerente de Qualidade confere, commit a commit, que cada etapa só tocou os caminhos do seu papel: um commit de etapa com o registro ou a memória dentro seria violação.
6. **Relatório mal formado** (seção faltando, JSON inválido, status ausente): reinvoque o agente uma vez pedindo só a correção do formato. Todo relatório, inclusive o resumo do parecer, traz todas as seções, com "Nenhum." quando vazias; o JSON do parecer valida contra `.claude/quality/parecer.schema.json`. Se persistir, pare e informe o usuário.
7. **Nada de push, merge ou rebase** sem autorização explícita do usuário no Portão 3.
8. **Portões no lugar de relatório e permissão por arquivo.** Dentro deste fluxo, o resumo confirmado na Etapa 0 e os portões 1 a 3 substituem o relatório prévio de `.claude/regras/metodo.md` e a permissão por arquivo e o limite de 3 arquivos de `.claude/regras/inviolaveis.md`. Ao invocar um subagente, diga isso a ele: ele escreve nos caminhos do próprio papel sem apresentar relatório nem pedir permissão, e devolve o resultado a você.
9. **Memória.** A execução é uma tarefa em `.claude/memoria/task.json`, escrita por você seguindo a skill `nova-memoria`. Ela é a única fonte do estado da execução, e é local à cópia de trabalho: vale em qualquer branch. Atualize-a (operação 3) ao fim de cada etapa e em cada portão: `plano`, `proximo_passo`, `aguardando: usuario` enquanto um portão estiver aberto e as ADRs `Proposto` em `pendencias_de_fechamento.adrs_pendentes`.
10. **Perguntas dos agentes.** Subagentes não falam com o usuário. O que um agente precisa do usuário vem na seção "Perguntas para o usuário" do relatório dele. Faça as perguntas ao usuário e reinvoque o agente com as respostas, repassando a frase do usuário (regra 4).
11. **Disposições.** Toda decisão de um dono de artefato ou do usuário sobre um achado, um item da demanda ou um item devolvido vai para a seção "Disposições" do registro no momento em que é tomada: o identificador (`GQ-nnn`, `TQ-nnn`, `TA-nnn`), a decisão (`mantém`, `corrige`, `substitui`, `orienta`, `improcedente`, do arquiteto ou do gerente-de-produto; "aceito", do usuário) e a frase de quem decidiu, copiada sem reescrever. A seção inteira é passada ao Gerente de Qualidade em toda rodada a partir da segunda. Sem isso, o revisor, que não tem memória entre rodadas, reemite o que já foi decidido, e o achado circula até o limite de rodadas.
12. **Retome o agente dentro da etapa.** Quando a mesma etapa precisa voltar ao mesmo agente para uma destas três coisas, continue a conversa com ele (SendMessage para o agente que acabou de responder) em vez de invocar um agente novo: entregar a resposta do usuário a uma pergunta (regra 10), registrar uma aprovação de portão (mudar a linha de status) e pedir a correção de formato do relatório (regra 6). Um agente novo começa do zero e relê spec, ADRs e código para trocar uma linha. Use invocação nova ao mudar de etapa, ao retomar o fluxo em outra sessão (o agente anterior não existe mais; passe os caminhos, como sempre) e **sempre** para cada rodada do Gerente de Qualidade: a independência do revisor depende de ele não carregar a rodada anterior. A correção de formato do parecer é a única retomada permitida com ele.
13. **Referências.** Os agentes técnicos consultam `docs/referencias/` por conta própria, como manda `.claude/regras/referencias.md`. Você não consulta por eles nem lhes entrega resumo de referência (regras 1 e 3). De cada relatório, leia a seção "Referências consultadas" e copie as linhas de lacuna para "Lacunas de referência" do registro: o agente e a dúvida, sem a fonte usada no lugar nem a escolha feita. No parecer, essa seção existe só no resumo em Markdown (`parecer-r<n>.md`), não no JSON. Uma contradição entre referência e ADR ou contrato chega pelos canais de sempre ("Perguntas para o usuário", regra 10, ou "Pontos para o arquiteto"). "Nenhum." na seção é resposta válida: nem toda invocação tem dúvida técnica.

## O que cada agente recebe

| Etapa | Agente (modo) | Recebe | NÃO recebe |
| --- | --- | --- | --- |
| 1 | gerente-de-produto (discovery) | o pedido do usuário; respostas do usuário às lacunas | — |
| 2 | arquiteto (pacote) | caminho da spec aprovada; slug; data do dia | — |
| 3 | tester (especificacao) | caminhos da spec, ADRs aplicáveis, contratos e `especificacao.md`; slug | nada da implementação (ela não existe) |
| 4 | escritor (implementacao) | caminhos da spec, ADRs, contratos; lista dos testes da etapa 3 (do `mapa_testes`) | relatório do tester além da lista de testes |
| 5 | gerente-de-qualidade | as entradas do contrato dele: `demanda`, `adrs`, `contratos`, `especificacao_testes`, `escopo`, `commits_por_etapa`, `mapa_testes`, `rodada`, `achados_anteriores` (o caminho de `parecer-r<n-1>.json`), `devolvidos` e `disposicoes` (as seções de mesmo nome do registro, copiadas sem reescrever), `perfil`; depois da Etapa 7, também `pendencias_de_validacao` | **relatório do Escritor** |
| 6a | tester (qualidade) | os itens `TQ-*` da rodada; os achados `GQ-*` destinados ao Tester; caminhos de spec, ADRs e contratos; a seção "Indícios para testes" do Escritor; a orientação do arquiteto, se um achado dele foi escalado | o restante do relatório do Escritor |
| 6b | escritor (correcao) | os achados `GQ-*` destinados ao Escritor; os testes que falham e o diagnóstico do tester sobre cada um ("Defeitos do tester" do registro); a orientação do arquiteto, se um achado dele foi escalado; depois de uma reespecificação, os testes alterados que passaram a falhar e a resposta do arquiteto que originou a mudança | o parecer completo |
| reespecificação | tester (especificacao, subcaso reespecificação) | os `TA-*` versionados; a resposta do arquiteto que os originou; caminhos de spec, ADRs, contratos e `especificacao.md` | relatório do Escritor |
| 7 | gerente-de-produto (validacao) | o caminho da spec; os caminhos do último parecer (`parecer-r<n>.md` e `.json`) e de `especificacao.md`; o `mapa_testes` completo | — |
| escalada | arquiteto (contestacao) / gerente-de-produto (lacuna) | o achado ou a devolução, com a evidência e o caminho do artefato contestado; para o arquiteto, a data do dia | — |
| 1 e 2 | senso-critico (exame) | o objeto e os caminhos examinados; os caminhos das fundações; fluxo, slug e data do dia | relatórios dos agentes; as `[INFERIDO]` explicadas por você |
| 1 e 2 | arquiteto (contestacao) / gerente-de-produto (critica) | o caminho do relatório do crítico; os identificadores `SC-nnn` destinados a ele; nas decisões de tensão com ADR, o parecer do arquiteto; para o arquiteto, a data do dia | — |

Além do que a tabela indica, todo agente técnico (arquiteto, tester, escritor, gerente-de-qualidade) recebe em toda invocação o caminho do perfil de stack (regra 3).

## Registro da execução

Mantenha `docs/execucoes/<slug>.md`, atualizado ao fim de cada etapa. Ele guarda o que se acumula ao longo da execução; o estado (etapa atual, rodada, próximo passo) fica só em `.claude/memoria/task.json`. Os dois juntos permitem retomar; o registro é versionado e, sozinho, permite reconstruir a tarefa num clone novo (pela seção Histórico).

O registro guarda o que você recebe dos relatórios e precisa repassar depois. Nunca copie para ele o restante do relatório do Escritor (tarefa, escolhas locais, diagnósticos): o registro fica no repositório, e a revisão não pode ser ancorada pela explicação de quem escreveu o código.

```markdown
# Execução /feature — <slug>

- Pedido: <texto original>
- Branch: feature/<slug> · Base: <hash>
- Perfil de stack: <caminho da pasta do perfil> (ADR <NNNN>)

## commits_por_etapa
- gerente-de-produto: <hash>, ...
- arquiteto: <hash>, ...
- tester: <hash>, ...
- escritor: <hash>, ...
- senso-critico: <hash>, ...
- orquestrador: (não se mantém à mão: são os commits do escopo que não estão nas linhas acima)

## Portões
- Portão 1: aprovado em <data> — "<frase do usuário>"
- Portão 2: ...

## Senso crítico
- Portão 1: SC-R-NNN — <resultado>
- Portão 2: SC-R-NNN — <resultado>

## Auditoria do crítico
(gatilhos detectados: ADR substituída ou recorrência de `gatilho improcedente`; apresentados no Encerramento)

## mapa_testes
(tabelas "Testes implementados" de cada relatório do tester, acumuladas)

## Devolvidos
(seções "Devolvidos" e "Sem oráculo" de cada relatório do tester, acumuladas, com o destino e a resposta recebida)

## Defeitos do tester (rodada <n>)
(seção "Defeitos encontrados no código" do último relatório do tester em modo qualidade; é a entrada do escritor em modo correcao)

## Disposições
(o que o dono de um artefato ou o usuário decidiu sobre um achado ou item devolvido: identificador, decisão, frase)

## Indícios do escritor
(seção "Indícios para testes" do último relatório do escritor)

## Pontos para o arquiteto
(pontos não bloqueantes dos relatórios do escritor, acumulados; apresentados no Portão 3)

## Lacunas de referência
(dúvidas técnicas que nenhuma referência cobriu, acumuladas dos relatórios: agente e dúvida; apresentadas no Portão 3, com a decisão do usuário)

## Histórico
- <data> etapa <n>: <resultado em uma linha>
```

## Etapas

### Etapa 0 — Preparação

1. Confirme que a árvore de trabalho está limpa (`git status --porcelain`). Se não estiver, pare e peça ao usuário para commitar ou descartar.
2. Registre o commit base (`git rev-parse HEAD`).
3. Confira os pré-requisitos, sem criar nada por conta própria:
   - os seis agentes em `.claude/agents/` (os cinco do time e o `senso-critico`);
   - `.claude/quality/checklist.md` e `.claude/quality/parecer.schema.json` (sem eles, o Gerente de Qualidade bloqueia);
   - o **projeto fundado**: `docs/produto/visao.md`, a ADR de base aceita, que escolhe o perfil de stack e as ferramentas de build, teste e análise (é a de título `Base do projeto: …` cuja última linha de Status é `Aceito`; procure pelo prefixo em `docs/adr/README.md`), e o build do projeto com essas ferramentas configuradas.

   A base do projeto é criada pelo fluxo `/fundacao`, não por este. Se algum item do projeto fundado faltar, pare: informe o que falta e indique `/fundacao criar` (projeto sem base) ou `/fundacao alterar` (base incompleta ou desatualizada).

   Leia na ADR de perfil qual perfil de stack o projeto usa e confira que a pasta dele existe em `.claude/skills/` (ex.: `.claude/skills/perfil-java-spring/`). Esse caminho vai para o registro da execução e para as `notas_de_retomada` da tarefa, e é passado a cada agente técnico (regra 3). Do `SKILL.md` do perfil saem também os diretórios de código e de teste e os arquivos de build, usados na autorização do passo 6.
4. Confira que não há tarefa ativa em `.claude/memoria/task.json` (`tarefa.id` nulo). Se houver, pergunte ao usuário se ela deve ser fechada ou cancelada antes. Confira também `.claude/memoria/roadmap.json`: se houver roadmap `em_andamento`, pergunte ao usuário se esta feature é a tarefa `proxima` dele. Se for, a tarefa do passo 6 usa o id e o título de lá e segue a parte "com roadmap" das operações da `nova-memoria`; se não for, é tarefa avulsa (TASK-NNN novo) e o roadmap não muda.
5. Apresente ao usuário um resumo curto: o pedido, as etapas e os caminhos que o fluxo vai escrever. Pergunte se pode iniciar.
6. Confirmado, abra a tarefa pela skill `nova-memoria` (operação 2): `demanda` = o pedido; `plano` = as etapas 1 a 8, cada uma com o `responsavel` certo (`agente:<nome>` ou `orquestrador`); `criterios_de_aceite` = três, que o fechamento vai exigir verificados: "o último parecer não tem achado nem item de demanda bloqueante" (evidência: o caminho do parecer), "a validação de produto foi feita e cada critério não atendido tem decisão do usuário" (evidência: a tabela de Validação da spec) e "o usuário decidiu o Portão 3" (evidência: a frase dele); `arquivos` fica vazio, porque os caminhos do fluxo são dados por globs na autorização e só se conhecem ao longo da execução; uma única autorização `A-1` com os caminhos `docs/produto/**`, `docs/adr/**`, `docs/contracts/**`, `docs/testes/**`, `docs/senso-critico/**`, os diretórios de código e de teste e os arquivos de build que o perfil de stack declara, os arquivos de CI do perfil (ou o caminho que a ADR de base indicar), `Dockerfile`, `README.md`, `docs/execucoes/**` e `.claude/memoria/**`. Essa confirmação é a permissão explícita para todo o fluxo.

### Etapa 1 — Produto

1. Invoque `gerente-de-produto` em modo `discovery` com o pedido e o caminho de `docs/produto/visao.md`.
2. Se ele devolver "Perguntas para o usuário" (as `[LACUNA]` que dependem do usuário), siga a regra 10.
3. **Senso crítico.** Rode a "Rodada do senso crítico" com o objeto `spec`. Como a branch e o registro ainda não existem, guarde o caminho do relatório nas `notas_de_retomada` e passe-o ao registro no passo 5.
4. **Portão 1.** Apresente ao usuário: o problema, o escopo (entra / depois / fora), a lista de critérios de aceite, os pontos `[INFERIDO]`/`[LACUNA]` restantes e os itens do senso crítico (passo 6 da rodada). Pergunte se aprova a spec.
   - Aprovou → reinvoque `gerente-de-produto` informando a aprovação, com a frase do usuário, para mudar o status para `aprovada`.
   - Pediu mudanças → reinvoque com as mudanças; volte ao Portão 1. Uma nova rodada do crítico só roda se o usuário pedir.
5. Crie a branch `feature/<slug>` (`git switch -c feature/<slug>`) e o registro da execução. Commite `docs(produto): spec <slug>` com os arquivos de `docs/produto/` e registre o hash em `gerente-de-produto`; commite o relatório do crítico (passo 7 da rodada); faça o seu commit com o registro (regra 5).

### Etapa 2 — Pacote técnico

1. Invoque `arquiteto` em modo pacote com o caminho da spec e a data do dia (regra 3).
2. Se ele devolver algo ao Gerente de Produto, invoque `gerente-de-produto` em modo `lacuna`; se a spec mudar, volte ao Portão 1. Perguntas para o usuário seguem a regra 10.
3. **Senso crítico.** Rode a "Rodada do senso crítico" com o objeto `pacote`. Se não houver ADR nova, contrato alterado nem `TA-*` que carregue decisão, o crítico pode devolver "Nenhuma objeção": a rodada roda assim mesmo.
4. **Portão 2.** Apresente ao usuário: os ADRs novos (o resumo para quem decide de cada um, tirado do relatório do arquiteto), as mudanças de contrato, a lista de `TA-*` com a tabela de cobertura, as referências que sustentaram as decisões (item 7 do relatório do arquiteto), as questões em aberto e os itens do senso crítico (passo 6 da rodada). Pergunte se aceita.
   - Aceitou → peça ao usuário que grave **manualmente**, em cada ADR novo e na linha dele em `docs/adr/README.md`, a linha `- Aceito — AAAA-MM-DD`. Quando um ADR substitui outro, o usuário grava também `- Substituído por ADR-NNNN — AAAA-MM-DD` no antigo. Você e os agentes nunca gravam essas linhas. Depois, confira a última linha da seção Status de cada ADR (por exemplo, com `grep -A20 "^## Status"`). Só então reinvoque o `arquiteto`, com a frase do usuário, para mudar a especificação para `aprovada`, e retire os ADRs aceitos de `adrs_pendentes`. Cada ADR substituída é um gatilho de auditoria do crítico: anote-a em "Auditoria do crítico" do registro.
   - Pediu mudanças → reinvoque; volte ao Portão 2. Uma nova rodada do crítico só roda se o usuário pedir.
5. Commite `docs(arq): pacote <slug>` (inclui as linhas `Aceito` que o usuário gravou), registre o hash em `arquiteto`; commite o relatório do crítico (passo 7 da rodada); faça o seu commit com o registro (regra 5).

### Etapa 3 — Testes primeiro

1. Invoque `tester` em modo `especificacao`.
2. Leia o relatório:
   - **Devolvidos** → anote cada um na seção "Devolvidos" do registro e leve-o ao destino indicado:
     - **Arquiteto** (modo contestacao) ou **Gerente de Produto** (modo `lacuna`): com a resposta, reinvoque o tester só para os itens devolvidos. Se a resposta mudar a especificação aprovada, mostre a mudança ao usuário antes de seguir.
     - **Usuário** (ferramenta de teste que a base do projeto não configura): é o mesmo caso do achado de ferramenta da Etapa 5. Registre um impedimento I-XXX pela `nova-memoria` (operação 4), anote o ponto de retorno "Etapa <3 ou 6, a etapa da devolução>, passo 1, só para os itens devolvidos" (ver o início deste arquivo), pare e indique `/fundacao alterar`; a execução volta por `/feature retomar <slug>`.
     - **Gerente de Qualidade** (`TQ-*` ambíguo ou sem fonte do oráculo; só acontece na Etapa 6): não há reinvocação. O item fica no registro e é resolvido na rodada seguinte da revisão, que o reescreve com a fonte ou o transforma em achado para quem pode resolver a lacuna.
   - **Resultados que divergem do `Vermelho esperado`** (o teste passou com o campo em `sim`, ou falhou com o campo em `não`) → leve ao arquiteto: ou o comportamento já existe (e o `TA-*` precisa ser revisto), ou o teste é vazio (e volta ao tester).
3. Rode você mesmo o comando de testes e confirme que os testes novos falham pelos motivos que o tester relatou (os de `Vermelho esperado: não` passam) e que nenhum teste antigo quebrou. Para um `TA-*` de nível `arquitetura`, o vermelho correto é a regra falhar porque ainda não há código a verificar (o perfil de stack diz como configurar isso); um teste estrutural que passa antes da implementação é tão suspeito quanto qualquer outro.
4. Verifique que todo `TA-*` tem teste ou está devolvido e pendente. Não avance com `TA-*` pendente sem o usuário saber.
5. Commite `test(espec): <slug>`, registre o hash em `tester` e acrescente a tabela do relatório ao `mapa_testes`.

### Etapa 4 — Implementação

1. Invoque `escritor` em modo `implementacao`.
2. Leia o relatório:
   - **BLOQUEADO** → leve o motivo ao dono (arquiteto ou gerente-de-produto). Com a resposta, reinvoque o escritor.
   - **Testes que contradizem uma fonte** → leve ao arquiteto (modo contestacao). Registre a resposta em "Disposições" (regra 11). Se ele corrigir um `TA-*`, invoque o tester em modo `especificacao`, subcaso reespecificação, para atualizar o teste correspondente (commit à parte, registrado em `tester`) e então reinvoque o escritor.
   - **Pontos para o arquiteto** que não bloqueiam → acrescente-os à seção "Pontos para o arquiteto" do registro; serão apresentados no Portão 3. (Os que bloqueiam chegam como `BLOQUEADO` e seguem o primeiro item.)
3. Rode a suíte e confirme o critério de pronto: build passando, testes da etapa 3 verdes, nenhum teste antigo vermelho. Se não, devolva ao escritor com a saída da execução.
4. Guarde a seção "Indícios para testes" no registro.
5. Commite `feat(<slug>): implementação`, registre o hash em `escritor`.

### Etapa 5 — Revisão

1. Invoque `gerente-de-qualidade` com todas as entradas do contrato dele (ver tabela). `escopo` é `<merge-base>..HEAD`, com o merge-base recalculado a cada rodada (`git merge-base <branch principal> HEAD`): se uma base de projeto nova chegou a esta branch por merge ou rebase depois de um `/fundacao alterar`, os arquivos dela ficam fora do escopo da feature. `rodada` começa em 1.
2. Grave o parecer inteiro, sem reescrever nada: a Parte 1 (resumo em Markdown) em `docs/testes/<slug>/parecer-r<n>.md` e a Parte 2 (o JSON) em `docs/testes/<slug>/parecer-r<n>.json`. Commite `docs(qualidade): parecer r<n> <slug>`, junto com o registro (é um commit seu). A partir daqui, o parecer é sempre passado por caminho (regra 3): ele sobrevive à compactação da conversa e a um `retomar`.
3. Siga a ação do parecer:
   - `integrar` → Etapa 7. Se houver demanda de testes recomendada ou achados recomendados (inclusive os destinados ao arquiteto ou ao gerente-de-produto), apresente-os antes ao usuário: ele decide se quer uma rodada de correção, uma escalada ao dono do artefato, ou nada. O que ele decidir não corrigir entra em "Disposições" como "aceito", com a frase dele.
     - **Na memória:** ao receber o parecer, ponha cada achado recomendado e cada item recomendado da demanda em `pendencias_de_fechamento.apontamentos_sem_disposicao` da tarefa (`nova-memoria`, operação 3). Quando o usuário decidir sobre um deles (corrigir agora, escalar, aceitar), registre a decisão como D-XXX (operação 5, passo 4), o que o tira da lista. O registro da execução serve ao revisor; o D-XXX é o que fica na memória do projeto e o que deixa a tarefa fechar.
   - `ciclo_de_correcao` → Etapa 6.
   - `pausar_e_escalar` → leve cada achado bloqueante ao destino: arquiteto (modo contestacao), gerente-de-produto (modo `lacuna`), você mesmo (entrada faltando: corrija a entrada e reinvoque) ou o usuário (ferramenta que a base do projeto não define ou o ambiente não suporta: pare; ele decide como refazer a base, normalmente por `/fundacao alterar`, com o achado como motivo). Mudança em spec, ADR aceito ou contrato integrado volta ao usuário. Registre cada resposta em "Disposições" (regra 11) e retome conforme a tabela "Retomada depois de uma escalada", abaixo. Ferramenta → registre um impedimento I-XXX pela `nova-memoria` (operação 4: a tarefa fica `bloqueada`, `aguardando: usuario`), anote o ponto de retorno "Etapa 5, rodada nova sobre a base nova" (ver o início deste arquivo) e commite o registro e `impedimentos.md` (commit seu); o `/fundacao alterar` roda dentro desta mesma tarefa, como nova autorização, na branch dele; depois que a base nova chegar a esta branch, `/feature retomar <slug>` resolve o I-XXX e volta a esse ponto.

**Retomada depois de uma escalada.** O ponto de retorno depende do que a resposta do dono mudou, não de quem respondeu:

| A resposta | Caminho de volta |
| --- | --- |
| mudou a spec (gerente-de-produto, com aprovação do usuário no Portão 1) | Etapa 2: o arquiteto revê o pacote para os critérios afetados; depois, as duas linhas abaixo conforme o que ele mudar |
| mudou ADR, contrato ou `TA-*` (`corrige`, `substitui`) | tester em reespecificação, só para os `TA-*` versionados → escritor em modo `correcao`, com os testes que passaram a falhar e a resposta do arquiteto → Etapa 5 |
| não mudou artefato: `orienta` | Etapa 6, entregando a orientação ao destino original do achado (tester, escritor ou ambos) → Etapa 5 |
| não mudou artefato: `mantém` ou `improcedente` | direto à Etapa 5: a disposição faz o revisor não reemitir o achado. Se era o único bloqueante, a rodada nova tende a `integrar` |

O escritor nunca volta em modo `implementacao` depois da Etapa 4: com o código existindo, toda volta dele é `correcao`. Cada volta à Etapa 5 incrementa a rodada e conta para o limite da Etapa 6.

### Etapa 6 — Correção

1. **Tester (qualidade).** Se houver `TQ-*` ou achados destinados ao Tester, invoque `tester` em modo `qualidade` com eles e com os indícios do escritor. Trate devoluções como na Etapa 3. Commite `test(qualidade): r<n> <slug>`, registre em `tester`, atualize o `mapa_testes` e copie a seção "Defeitos encontrados no código" para o registro.
2. **Escritor (correcao).** Se houver achados destinados ao Escritor ou testes que passaram a falhar no passo anterior, invoque `escritor` em modo `correcao`. Trate o relatório como na Etapa 4. Commite `fix(<slug>): correções r<n>`, registre em `escritor`.
3. **Achados contestados.** Se o tester ou o escritor contestarem um achado (seção "Achados contestados" do relatório), leve cada um ao arquiteto em modo contestacao, com o achado do parecer e a fonte citada por quem contestou. Registre a resposta em "Disposições" (regra 11): `improcedente` faz o revisor não reemitir o achado; `orienta`, `corrige` ou `substitui` seguem a tabela "Retomada depois de uma escalada" antes de voltar à revisão. Você não julga a contestação nem a descarta.
4. Incremente a rodada e volte à Etapa 5, passando o caminho de `parecer-r<n>.json` da rodada que terminou como `achados_anteriores`.

**Limite:** toda passagem pela Etapa 5 é uma rodada, venha ela de um ciclo de correção, de uma escalada ou da Etapa 7. Se a rodada 3 terminar com veredito `bloqueado`, não inicie a 4. Pare e apresente ao usuário os achados restantes, quantas rodadas cada um sobreviveu e a quem foram escalados. O usuário decide como seguir.

### Etapa 7 — Validação de produto

1. Invoque `gerente-de-produto` em modo `validacao`, com os caminhos do último parecer e de `docs/testes/<slug>/especificacao.md` e o `mapa_testes`.
2. Critério `parcial`, `nao_atendido` ou `nao_verificavel` → apresente ao usuário (`parcial` tem o mesmo tratamento de `nao_atendido`). Ele decide entre:
   - **nova rodada de revisão:** volte à Etapa 5, incrementando a rodada, e passe ao Gerente de Qualidade, junto das entradas dele, a linha da tabela de Validação de cada critério pendente (copiada da spec, sem reescrever). É ele quem transforma a pendência em item da demanda de testes (`TQ-*`) ou em achado: nem você nem o Gerente de Produto escrevem exigência de teste. Essa rodada conta para o limite da Etapa 6;
   - aceitar a lacuna e registrá-la no backlog de produto (`docs/produto/backlog.md`, pelo gerente-de-produto, na mesma invocação de validação);
   - rever a spec (volta ao Portão 1).
3. Commite `docs(produto): validação <slug>`, registre em `gerente-de-produto`.

### Etapa 8 — Encerramento

1. Apresente ao usuário, de forma curta:
   - o que foi entregue, por critério de aceite (`atendido`, ou lacuna aceita pelo usuário na Etapa 7);
   - os ADRs criados e os contratos alterados;
   - quantos testes por rodada (`TA` e `TQ`) e o veredito final;
   - achados recomendados não resolvidos, os "Pontos para o arquiteto" do registro e os itens que voltaram ao backlog de produto;
   - as "Lacunas de referência" do registro;
   - os gatilhos de "Auditoria do crítico" do registro, se houver, só como informação: não sugira nem invoque skill de auditoria; auditar o crítico é decisão do usuário, fora deste fluxo;
   - a branch e a lista de commits.
2. **Portão 3.** Antes de perguntar, ponha os "Pontos para o arquiteto" do registro em `apontamentos_sem_disposicao` (operação 3 da `nova-memoria`). Cada decisão do usuário neste portão sobre um apontamento (os pontos e os achados recomendados que restarem) vira um D-XXX (operação 5, passo 4); a tarefa só fecha com a lista vazia. Pergunte se o usuário quer merge, push, PR, ou nada por enquanto, e o que fazer com cada ponto para o arquiteto (trabalho para o arquiteto, item do backlog de produto ou descarte). Pergunte também o que fazer com cada lacuna de referência (referência nova a providenciar, fora deste fluxo, ou descarte) e anote a decisão, com a frase do usuário, ao lado da lacuna no registro; lacuna não é apontamento e não gera D-XXX.
3. Marque a execução como concluída no registro, com a decisão do Portão 3, e commite (`chore(exec): <slug> encerramento`) **antes** de qualquer merge ou push, para que o registro final vá junto com a branch.
4. Execute somente o que o usuário autorizou no Portão 3.
5. Feche a tarefa pela skill `nova-memoria` (operação 6, com resumo e confirmação do usuário). Como `task.json` é estado local, o fechamento não deixa nada por commitar.

## Cancelamento

O usuário pode desistir em qualquer portão ou no meio de uma etapa. Você não desfaz nada por conta própria:

1. Mostre o que existe: os arquivos escritos e ainda sem commit (`git status --porcelain`), a branch `feature/<slug>` e os commits dela, se já existir. Antes do fim da Etapa 1 não há branch: a spec e o backlog de produto estão alterados na árvore de trabalho da branch em que o fluxo começou.
2. Pergunte o que fazer com cada parte: manter a branch para retomar depois, apagá-la, descartar os arquivos sem commit. Execute só o que ele autorizar.
3. Se a spec já existir e for mantida, peça ao gerente-de-produto (modo `lacuna`) que registre o cancelamento no backlog de produto, com o motivo do usuário.
4. Cancele a tarefa pela `nova-memoria` (operação 6, "Cancelar", com resumo e confirmação). Impedimentos abertos da tarefa são resolvidos com "tarefa cancelada".
5. Se o registro da execução for mantido, marque nele a execução como cancelada, com a data e a frase do usuário, e commite.
