# Dicionário de campos da memória

## task.json

| Campo | Conteúdo |
|---|---|
| `atualizado_em` | `AAAA-MM-DDTHH:MM` da última escrita (`date +%FT%H:%M`). |
| `tarefa.id` | `TASK-NNN` global; `null` sem tarefa ativa. |
| `tarefa.titulo` | Frase curta; com roadmap, igual à de lá. |
| `tarefa.demanda` | Pedido do usuário, fiel, em uma ou duas frases. |
| `tarefa.objetivo` | O que existe ou funciona ao final. |
| `tarefa.criterios_de_aceite[]` | `{criterio, verificado, evidencia}`; critério verificável; evidência = como foi verificado. |
| `tarefa.fora_do_escopo[]` | Frases: o que foi explicitamente excluído. |
| `tarefa.status` | `em_andamento` \| `bloqueada`; `null` sem tarefa. Espera pelo usuário vai em `aguardando`. |
| `tarefa.iniciada_em` | `AAAA-MM-DD`. |
| `plano[]` | `{n, etapa, responsavel, status, impedimento}`; `responsavel`: `orquestrador` \| `usuario` \| `agente:<nome>`; `status`: `pendente` \| `em_andamento` \| `feita` \| `bloqueada`; `impedimento`: I-XXX obrigatório se `bloqueada`, senão `null`. |
| `aguardando` | `null` \| `usuario` \| `agente:<nome>`. |
| `proximo_passo` | Uma frase: a próxima ação concreta. |
| `arquivos[]` | `{caminho, acao, autorizacao, feito}`; `acao`: `criar` \| `modificar` \| `excluir`; `autorizacao`: A-N que o cobre. |
| `autorizacoes[]` | `{id, data, escopo, caminhos}`; `caminhos`: globs relativos à raiz (`**` atravessa pastas). Nunca editadas; nova permissão = nova entrada. |
| `decisoes_registradas[]` | IDs D-XXX registrados durante a tarefa. |
| `pendencias_de_fechamento.apontamentos_sem_disposicao[]` | `"[SEVERIDADE] <apontamento> — <origem>"`. |
| `pendencias_de_fechamento.adrs_pendentes[]` | `"docs/adr/NNNN-slug.md — <título>"`. |
| `arquivos_apoio[]` | `{caminho, proposito}`: arquivos temporários criados para a tarefa (rascunhos, scripts de teste, saídas), excluídos no fechamento. |
| `notas_de_retomada[]` | Frases factuais necessárias para retomar sem a conversa. |

## roadmap.json

| Campo | Conteúdo |
|---|---|
| `atualizado_em` | `AAAA-MM-DDTHH:MM`. |
| `roadmap.titulo` | Frase curta; `null` = sem roadmap (tarefa ativa, se houver, é avulsa). |
| `roadmap.objetivo` | O que existe ao final do roadmap. |
| `roadmap.criterio_de_conclusao` | Frase verificável. |
| `roadmap.status` | `planejamento` \| `em_andamento` \| `suspenso` \| `concluido`; `null` sem roadmap. |
| `roadmap.iniciado_em` | `AAAA-MM-DD`. |
| `tarefa_atual` | TASK-NNN carregada em `task.json`; `null` sem tarefa ou quando a tarefa é avulsa. |
| `tarefas[]` | `{id, titulo, objetivo, status, depende_de, concluida_em, resultado}`; `status`: `planejada` \| `proxima` \| `em_andamento` \| `bloqueada` \| `concluida` \| `cancelada`; o motivo de um bloqueio está em `impedimentos.md`. |
| `arquivos_apoio[]` | Como em task.json, mas do roadmap inteiro. |
