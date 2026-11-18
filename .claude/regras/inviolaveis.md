## Regras invioláveis

- Somente crie, modifique ou exclua algum arquivo quando explicitamente permitido;
- Não refatore código fora do escopo explícito da tarefa pedida;
- Não adicione tratamento de erro para cenários impossíveis
- Pergunte antes de agir se a tarefa tiver mais de 3 arquivos envolvidos;
- Exceção: as atualizações de rotina em `.claude/memoria/` não exigem permissão e os arquivos de memória não contam no limite de 3, conforme o protocolo de memória (`.claude/regras/memoria.md`);
- Exceção: dentro dos fluxos `/feature` e `/fundacao`, a confirmação do usuário na Etapa 0 é a permissão explícita para os caminhos das autorizações da tarefa (`A-1` e as que os portões do fluxo acrescentarem), e o limite de 3 arquivos não se aplica a eles (ver `.claude/skills/feature/SKILL.md`, regra 8, que vale também para o `/fundacao`);
- Exceção: dentro do fluxo `/bugfix`, a confirmação do usuário na Etapa 0 e no Portão 1 é a permissão explícita para os caminhos das autorizações da tarefa (`A-1`, os registros do fluxo; `A-2`, o escopo de correção confirmado; e as que o usuário acrescentar ao ampliar o escopo), e o limite de 3 arquivos não se aplica a eles (ver `.claude/skills/bugfix/SKILL.md`, regra 11);
- Exceção: dentro do fluxo `/spike`, a confirmação do usuário no Portão 1 é a permissão explícita para o código descartável do experimento, só dentro da worktree isolada dele, e o limite de 3 arquivos não se aplica ali (ver `.claude/skills/spike/SKILL.md`, regra 7);
