---
name: nova-memoria
description: Registra e mantém a memória do projeto em .claude/memoria/ (roadmap.json, task.json, decisoes.md, impedimentos.md). Use sempre que for abrir, atualizar, bloquear, desbloquear, cancelar ou fechar uma tarefa ou um roadmap; registrar autorização, decisão (D-XXX) ou impedimento (I-XXX); reiniciar a memória; ou quando um relatório de alteração do metodo.md for aprovado, o que abre ou amplia uma tarefa. Só o orquestrador usa esta skill.
---

# Memória do projeto

Procedimentos para escrever em `.claude/memoria/`. O *quando* registrar e as políticas estão em
`.claude/regras/memoria.md`; aqui está o *como*.

## Princípios

- **Estado, não histórico.** `task.json` e `roadmap.json` descrevem o agora: substitua valores,
  não acumule narrativa. O histórico vive em `decisoes.md`, `impedimentos.md` e nas ADRs.
- **Estado é local.** `task.json` e `roadmap.json` estão no `.gitignore`: nunca entram em
  commit e não mudam ao trocar de branch. `decisoes.md` e `impedimentos.md` são versionados e
  entram no commit de quem os alterou.
- **Ferramentas.** Escreva só com `Edit`/`Write`. O hook valida após cada escrita: erro
  estrutural (exit 2) se corrige na hora; aviso de divergência pode ser transitório no meio de
  uma operação, mas não pode sobrar ao fim dela. Exceção: enquanto um `/fundacao alterar`
  roda dentro da tarefa de um `/feature` ou de um `/bugfix`, o aviso "I-XXX citado mas
  ausente em impedimentos.md" é esperado e permanece, porque a entrada está na branch do
  fluxo de origem; ele some quando o `/feature retomar <slug>` ou o `/bugfix retomar <slug>`
  volta a essa branch.
- **Datas.** `atualizado_em` = `date +%FT%H:%M`; datas de evento = `date +%F`. Rode `date`
  imediatamente antes de escrever; nunca deduza da conversa.
- **Toda escrita** em um JSON atualiza o `atualizado_em` dele; em um `.md`, a linha `Atualizado:`.
- **Modelos.** Os arquivos vazios ficam nesta skill: `assets/task.vazio.json` e
  `assets/roadmap.vazio.json`. Itens novos (tarefa, etapa, critério, arquivo, autorização)
  partem do `_modelo_*` correspondente, com exatamente as mesmas chaves. As chaves `_*` do
  arquivo vivo nunca são editadas: o validador exige que sejam iguais às do modelo.
- **Confirmação.** Operações marcadas **[confirmação]** só são gravadas após resumo e "sim" do
  usuário; as demais são rotina.
- Significado de cada campo: `assets/campos.md`. Arquivos preenchidos de exemplo:
  `assets/exemplo-task.json` e `assets/exemplo-roadmap.json`.

## Identificadores

- **TASK-NNN** (global, nunca reaproveitado): maior número citado em `docs/` ou `.claude/`,
  na cópia de trabalho ou em qualquer branch local, + 1; o primeiro é `TASK-001`. Não basta
  olhar a memória: `task.json` e `roadmap.json` voltam ao modelo no fechamento, e o número de
  uma tarefa sobrevive só onde foi citado (D-XXX, I-XXX, perfis, registros de execução).
  `{ grep -rhoE 'TASK-[0-9]+' docs .claude; git grep -hoE 'TASK-[0-9]+' $(git for-each-ref --format='%(refname:short)' refs/heads) -- docs .claude 2>/dev/null; } | sort -t- -k2 -n | tail -1`
- **D-XXX / I-XXX:** maior ID em `decisoes.md` / `impedimentos.md` + 1, com 3 dígitos,
  considerando **todas as branches locais**, não só a atual: os dois arquivos são versionados,
  e uma entrada aberta noutra branch (o I-XXX de um `/feature` bloqueado, por exemplo) não
  aparece nesta. Troque `I` por `D` e o arquivo para as decisões:
  `git grep -hoE '^### I-[0-9]+' $(git for-each-ref --format='%(refname:short)' refs/heads) -- .claude/memoria/impedimentos.md | sort -t- -k2 -n | tail -1`
  Compare com o maior ID da cópia de trabalho (entrada ainda sem commit) e use o maior dos dois.
- **A-N:** sequencial dentro da tarefa (`A-1`, `A-2`, ...); recomeça a cada tarefa.

## 1. Abrir roadmap [confirmação]

Quando: pedido com várias entregas ou que se estenda por várias sessões.

1. Proponha em resumo: título, objetivo, critério de conclusão verificável e as tarefas
   (id, título, objetivo de uma frase, `depende_de`), em ordem.
2. Confirmado, preencha `roadmap.json`: `roadmap.{titulo, objetivo, criterio_de_conclusao}`,
   `iniciado_em`; tarefas pelo `_modelo_de_tarefa`, todas `planejada`.
3. Se o usuário quiser começar já: `status` `em_andamento`, marque a primeira tarefa sem
   dependências como `proxima` e abra-a pela operação 2 (a confirmação do roadmap vale para
   ela). Se não: `status` `planejamento`, sem `proxima`.

## 2. Abrir tarefa

Quando: relatório do `metodo.md` aprovado sem tarefa ativa (tarefa avulsa), ou tarefa `proxima`
do roadmap confirmada pelo usuário. Pré-condição: `task.json > tarefa.id` é `null`; se não for,
feche ou cancele a ativa antes (operação 6), ou pergunte.

1. `tarefa.id`: o do roadmap, ou um TASK-NNN novo (avulsa). `titulo`: o do roadmap, ou uma
   frase curta.
2. `demanda`: o pedido do usuário, fiel, em uma ou duas frases. `objetivo`: o que existe ou
   funciona ao final; com roadmap, detalha o objetivo da tarefa lá, sem contradizê-lo.
3. `criterios_de_aceite`: frases verificáveis tiradas do relatório ou do pedido
   (`verificado: false`, `evidencia: null`). `fora_do_escopo`: o que o relatório excluiu.
4. `plano`: uma etapa por passo do relatório, todas `pendente`.
5. `autorizacoes`: `A-1` com `escopo` = resumo do relatório aprovado e `caminhos` = os arquivos
   a criar/modificar dele (globs quando o relatório citar pastas). `arquivos`: uma entrada por
   arquivo do relatório, com `autorizacao: "A-1"`.
6. `status` `em_andamento`, `iniciada_em`, `aguardando: null`, `proximo_passo` = a primeira etapa.
7. Com roadmap: a tarefa passa de `proxima` a `em_andamento` e `tarefa_atual` = id. Avulsa:
   `roadmap.json` não muda.

## 3. Atualizar durante a execução

Ao fim de cada etapa e antes de qualquer parada:

- `plano[].status`, `arquivos[].feito`, `proximo_passo`, `aguardando`.
- Critério verificado: `verificado: true` e `evidencia` (comando, teste ou conferência do usuário).
- `notas_de_retomada`: só fatos que alguém precisaria para retomar sem a conversa; remova os
  que deixaram de valer.
- Nova permissão do usuário na tarefa (outro relatório aprovado, arquivo extra): nova `A-N` e
  as entradas em `arquivos`. Nunca altere uma autorização existente.
- Apontamento de revisão ainda sem disposição: `pendencias_de_fechamento.apontamentos_sem_disposicao`.
  ADR proposta e não decidida: `pendencias_de_fechamento.adrs_pendentes`.

## 4. Impedimento

**Abrir** (assim que identificado):
1. `impedimentos.md`: entrada em "Abertos" no formato do arquivo, `Tarefa travada` = TASK-NNN.
2. `task.json`: a etapa afetada vai a `bloqueada` com `impedimento` = I-XXX; `tarefa.status`
   `bloqueada`; `aguardando` = `usuario` se "Depende de" for o usuário.
3. Com roadmap: a tarefa vai a `bloqueada`.

**Resolver:**
1. `impedimentos.md`: preencha `Resolução` e mova a entrada para "Resolvidos" (no formato de
   resolvido). Se a resolução gerou decisão, registre-a (operação 5) e cite o D-XXX.
2. `task.json`: a etapa volta a `pendente` ou `em_andamento`, `impedimento: null`; se não
   restar etapa bloqueada, `tarefa.status` `em_andamento` e ajuste `aguardando`.
3. Com roadmap: a tarefa volta a `em_andamento` se não restar bloqueio.

## 5. Registrar decisão

1. Se a decisão atinge vários módulos, a arquitetura ou é cara de reverter, ela é ADR: sugira a
   skill `nova-adr` em vez de registrar aqui.
2. Senão, entrada no topo de "Registros" de `decisoes.md`, no formato do arquivo.
3. Com tarefa ativa, acrescente o ID em `decisoes_registradas`.
4. Disposição de apontamento: `Decisão` no formato "Apontamento <x>: aceito | corrigido |
   descartado — <motivo>"; remova o apontamento de `apontamentos_sem_disposicao`.
5. Resultado de spike (fluxo `/spike`): não é decisão do projeto, mas entra aqui, e o passo 1
   não se aplica. Título "Spike: <pergunta>" e campos como manda a Etapa 3 de
   `.claude/skills/spike/SKILL.md`.

## 6. Fechar ou cancelar tarefa [confirmação]

**Fechar** exige:
- todos os `criterios_de_aceite` com `verificado: true` e `evidencia`;
- `apontamentos_sem_disposicao` e `adrs_pendentes` vazios (ADR sai quando gravada com status
  Aceito ou Rejeitado);
- nenhum I-XXX em "Abertos" de `impedimentos.md` com `Tarefa travada` = esta tarefa;
- `arquivos[].feito` todos `true`.

1. Apresente o resumo: critérios e evidências, arquivos, decisões, e os `arquivos_apoio` a
   excluir. Peça confirmação (vale para todos os passos abaixo).
2. Com roadmap: tarefa `concluida`, `concluida_em`, `resultado` (uma linha: o que foi
   entregue); `tarefa_atual: null`.
3. Exclua os `arquivos_apoio` da tarefa e reinicie `task.json` (operação 8).
4. Com roadmap: se todas as tarefas estiverem `concluida`/`cancelada`, siga para a operação 7.
   Senão, proponha a próxima elegível (todas as `depende_de` em `concluida`); confirmada,
   marque-a `proxima` e abra-a (operação 2).

**Cancelar:** o mesmo fluxo, sem exigir os critérios; com roadmap, status `cancelada` e
`resultado` = motivo. Impedimentos abertos da tarefa são resolvidos com a Resolução "tarefa
cancelada".

## 7. Fechar ou suspender roadmap [confirmação]

- **Fechar** exige `criterio_de_conclusao` verificado e todas as tarefas `concluida` ou
  `cancelada`. Resumo (tarefas e resultados), confirmação, exclusão dos `arquivos_apoio` do
  roadmap e reinício de `roadmap.json` (operação 8). Sugira uma ADR se o roadmap definiu
  arquitetura.
- **Suspender:** `status` `suspenso`, sem tarefa ativa. Retomar volta a `em_andamento`.

## 8. Reiniciar arquivo [confirmação]

Leia `assets/<nome>.vazio.json` (nesta skill) e grave o conteúdo inteiro sobre
`.claude/memoria/<nome>.json` com `Write`. Os modelos nunca mudam sem confirmação própria; ao
mudá-los, atualize no mesmo passo os arquivos vivos e os exemplos (`assets/exemplo-*.json`),
porque as chaves `_*` precisam continuar iguais.

## 9. Mudar a estrutura do roadmap [confirmação]

Incluir, remover ou reordenar tarefas, mudar `objetivo`, `criterio_de_conclusao` ou
`depende_de`: mostre antes/depois, confirme e grave. Mantenha no máximo uma `proxima`, e só
com as dependências concluídas. Tarefa removida que já tem histórico vira `cancelada`, não some.
