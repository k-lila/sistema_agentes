## Protocolo de memória

A memória do projeto fica em `.claude/memoria/`: `roadmap.json` (visão do todo), `task.json` (tarefa em execução), `decisoes.md` (D-XXX) e `impedimentos.md` (I-XXX). Fica dentro de `.claude/`, que é caminho protegido: cada escrita na memória pede confirmação ao usuário, e numa execução sem interação ela é negada (custo aceito).

- **Estado local, histórico versionado:** `task.json` e `roadmap.json` descrevem a cópia de trabalho e não entram no Git (`.gitignore`): não mudam ao trocar de branch e nunca entram em commit. `decisoes.md`, `impedimentos.md` e `docs/execucoes/` são histórico e são versionados. Num clone novo, o hook `SessionStart` recria os dois JSON a partir dos modelos; um fluxo em andamento se reconstrói pelo registro `docs/execucoes/<slug>.md`.
- **Como escrever:** toda escrita na memória segue a skill `nova-memoria`; leia-a antes da primeira escrita da sessão. Escreva com `Edit`/`Write`, nunca via Bash.
- **Quando registrar:**
  - relatório de alteração (`metodo.md`) aprovado sem tarefa ativa → abre uma tarefa; com tarefa ativa → vira nova autorização dela (se for outro assunto, pergunte);
  - pedido com várias entregas ou que se estenda por várias sessões → proponha um roadmap;
  - decisões e impedimentos surgidos no trabalho → D-XXX e I-XXX, com ou sem tarefa;
  - fluxos `/feature` e `/fundacao` → abrem a tarefa na Etapa 0, com a autorização `A-1` cobrindo os caminhos do fluxo, e a fecham no Encerramento: Etapa 8 do `/feature`, Etapa 7 do `/fundacao` (ver o `SKILL.md` de cada um em `.claude/skills/`);
  - fluxo `/bugfix` → abre a tarefa na Etapa 0, com a autorização `A-1` cobrindo só os registros do fluxo, acrescenta a `A-2` no Portão 1, com o escopo de correção confirmado, e a fecha no Encerramento, Etapa 5 (ver `.claude/skills/bugfix/SKILL.md`);
  - fluxo `/spike` → abre a tarefa no Portão 1, com a autorização `A-1` cobrindo só a worktree do experimento, grava o resultado como D-XXX e fecha a tarefa no Encerramento (ver `.claude/skills/spike/SKILL.md`);
  - perguntas, revisões e análises sem alteração não geram registro.
- **Início de sessão:** o hook `SessionStart` injeta um resumo. Antes de retomar, leia `roadmap.json`, `task.json` e os "Abertos" de `impedimentos.md`; retome por `proximo_passo`.
- **Quem escreve:** só o orquestrador. Subagentes devolvem a informação; o hook nega a escrita deles.
- **Rotina (sem permissão nem relatório):** abrir tarefa já aprovada, atualizar o estado da tarefa, registrar autorizações, D-XXX e I-XXX.
- **Exige confirmação, com resumo antes:** abrir roadmap ou mudar sua estrutura; fechar ou cancelar tarefa; fechar ou suspender roadmap; excluir `arquivos_apoio`; reiniciar arquivos; alterar os modelos (`.claude/skills/nova-memoria/assets/*.vazio.json`).
- **Autorizações:** com tarefa ativa, editar fora de `task.json > autorizacoes` faz o hook pedir confirmação. Sem tarefa ativa, vale o fluxo normal de permissões.
- **Validação:** o hook `PostToolUse` valida após cada escrita; erro estrutural se corrige na hora. Manual: `python3 -I .claude/hooks/validar_memoria.py --tudo`.
- **Limitação:** fora da memória, escrita via Bash não passa pela checagem de autorizações.
