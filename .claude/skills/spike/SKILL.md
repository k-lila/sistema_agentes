---
name: spike
description: Orquestra um experimento técnico descartável para responder a uma única dúvida que só a execução responde (viabilidade, comportamento de ferramenta, comparação, medição). O escritor roda o experimento numa worktree isolada, o usuário recebe a resposta com a evidência, o resultado fica num D-XXX e o código é jogado fora. Não produz documento de referência, ADR nem código de produção. Invocada manualmente com /spike.
argument-hint: "<dúvida técnica>"
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git rev-parse *) Bash(git worktree list *) Bash(git branch --list *) Bash(date *)
---

# /spike — experimento descartável

Você é o **orquestrador**. Você não escreve o código do experimento nem interpreta o resultado. Você enquadra a pergunta com o usuário, invoca o escritor numa worktree isolada, apresenta a resposta com a evidência, grava o resultado na memória e remove a worktree.

Dúvida do usuário: `$ARGUMENTS`

## O que é e o que não é

O spike responde a **uma** pergunta cuja resposta depende de executar algo: neste projeto, com esta stack e estas versões. O produto é uma evidência local e datada.

| Serve para | Exemplo |
| --- | --- |
| Viabilidade | "a biblioteca X funciona com a versão Y que usamos?" |
| Comportamento | "o que a ferramenta faz neste caso que a documentação não esclarece?" |
| Comparação | duas abordagens no mínimo necessário, medidas lado a lado |
| Medição | tempo, memória ou tamanho, quando a decisão depende do número |

Não é spike, e você diz isso ao usuário em vez de iniciar:

- pergunta que se responde lendo (referências, documentação oficial, código): responda pela regra das referências, sem experimento;
- o que o produto deve fazer: é da spec (`/feature`, gerente-de-produto);
- a decisão estrutural em si: é do arquiteto, por ADR. O spike pode vir antes, para dar a ela uma evidência;
- produzir um documento para `docs/referencias/`: referência exige levantamento de fontes e revisão, e não nasce deste fluxo.

## Visão geral

```
0 Enquadramento ...... orquestrador                 ── PORTÃO 1: usuário confirma pergunta, hipótese, critério e limite
1 Experimento ........ escritor (experimento), em worktree isolada
2 Resposta ........... orquestrador                 ── PORTÃO 2: usuário aceita a resposta
3 Encerramento ....... D-XXX, remoção da worktree, fechamento da tarefa
```

## Regras do orquestrador

1. **O critério vem antes do resultado.** A pergunta, a hipótese e o critério de resposta são fixados no Portão 1 e não mudam depois que o experimento rodou. Se o resultado mostrar que a pergunta estava errada, isso é a resposta deste spike ("inconclusivo", com o motivo); a pergunta certa é outro spike.
2. **Uma pergunta por execução.** Pergunta nova que surgir no caminho vai para "Perguntas derivadas" e é apresentada no Portão 2 como sugestão de outro spike.
3. **O spike informa, não decide.** Você apresenta a resposta e a evidência. Não recomenda a decisão que depende dela, não cria ADR e não altera spec, contrato nem referência.
4. **O código não sobrevive.** Nada da worktree é copiado, mesclado ou commitado na cópia principal, nem a pedido: se o código do experimento for bom, a ideia volta pelo `/feature` e é reescrita no fluxo normal. Diga isso ao usuário se ele pedir para aproveitá-lo.
5. **Você não reinterpreta a evidência.** Ao apresentar o resultado e ao gravar o D-XXX, copie do relatório do escritor os comandos, as saídas e as versões, mantendo as marcas `[executado]`, `[lido]` e `[inferido]`. Um resumo seu que troque "observado" por "conclusão" estraga a evidência.
6. **Resultado negativo ou inconclusivo é resultado.** "Não funciona" e "o limite de esforço acabou sem resposta" encerram o spike do mesmo jeito que "funciona", com D-XXX.
7. **Portões no lugar de relatório e permissão por arquivo.** O enquadramento confirmado no Portão 1 substitui o relatório prévio de `.claude/regras/metodo.md` e a permissão por arquivo e o limite de 3 arquivos de `.claude/regras/inviolaveis.md`, só para os arquivos dentro da worktree do experimento. Diga isso ao escritor ao invocá-lo.
8. **Memória.** A execução é uma tarefa em `.claude/memoria/task.json`, escrita por você seguindo a skill `nova-memoria`. Não há registro em `docs/execucoes/`: o que fica do spike é o D-XXX.
9. **Perguntas do agente.** O escritor não fala com o usuário. O que ele precisar vem em "Perguntas para o usuário"; pergunte e continue a conversa com o mesmo agente (SendMessage), repassando a frase do usuário. Um agente novo perderia a worktree e o que já foi montado.
10. **Só fora de outro fluxo.** O `/spike` não roda com tarefa ativa. Uma dúvida que surja dentro de um `/feature` ou `/fundacao` vira impedimento lá (I-XXX, `nova-memoria`, operação 4); o spike roda depois, com a tarefa do fluxo fechada ou cancelada pelo usuário, ou noutra cópia de trabalho.

## Etapas

### Etapa 0 — Enquadramento

1. Confira os pré-requisitos, sem criar nada:
   - o repositório tem ao menos um commit (`git rev-parse HEAD`). Sem commit não há worktree: pare e informe o usuário;
   - não há tarefa ativa em `.claude/memoria/task.json` (`tarefa.id` nulo). Se houver, pare e informe (regra 10);
   - o agente `escritor` existe em `.claude/agents/`.
2. Consulte `docs/referencias/README.md`, como manda `.claude/regras/referencias.md`. Se uma referência já responde à dúvida, mostre ao usuário o documento e a seção e pergunte se ele ainda quer o experimento.
3. Se a dúvida não for de spike (ver "O que é e o que não é"), diga qual é o caminho certo e pare.
4. Redija o enquadramento:
   - **Pergunta:** uma só, respondível por sim, não ou um número.
   - **Hipótese:** o que se espera observar, e por quê.
   - **Critério de resposta:** que observação conta como "sim", qual conta como "não". Para medição, a grandeza, a unidade e como medir.
   - **Limite de esforço:** o que o experimento inclui e o que fica fora (por exemplo: "um único endpoint, sem persistência, sem tratamento de erro").
   - **Base:** a worktree parte da branch padrão do repositório (ou do `HEAD` local, se não houver remoto), não das mudanças sem commit da cópia de trabalho. Se a pergunta depender de trabalho ainda não integrado, diga isso ao usuário agora.
5. **Portão 1.** Apresente o enquadramento e pergunte se pode rodar. Ajuste com o usuário até ele confirmar; guarde a frase dele.
6. Confirmado, abra a tarefa pela `nova-memoria` (operação 2). Confira `.claude/memoria/roadmap.json`: se houver roadmap `em_andamento` e o usuário disser que este spike é a tarefa `proxima` dele, use o id e o título de lá; senão é tarefa avulsa (TASK-NNN novo) e o roadmap não muda.
   - `demanda` = a dúvida do usuário; `objetivo` = a pergunta do enquadramento;
   - `criterios_de_aceite` = três: "o usuário aceitou a resposta no Portão 2" (evidência: a frase dele), "o resultado está registrado como D-XXX" (evidência: o ID) e "a worktree e a branch do experimento foram removidas" (evidência: a saída de `git worktree list`);
   - `fora_do_escopo` = o que o limite de esforço excluiu;
   - `plano` = as etapas 1 a 3; `arquivos` fica vazio;
   - `autorizacoes` = `A-1`, com `caminhos` = `.claude/worktrees/**` e `escopo` = "código descartável do spike, só dentro da worktree do experimento";
   - `notas_de_retomada` = a pergunta, a hipótese, o critério, o limite e a frase do Portão 1.

### Etapa 1 — Experimento

1. Invoque `escritor` em modo `experimento`, com isolamento em worktree (parâmetro `isolation: worktree` da invocação). Entregue: a pergunta, a hipótese, o critério de resposta e o limite de esforço, com as palavras confirmadas no Portão 1; o caminho do perfil de stack, se o projeto tiver ADR de base aceita; e o aviso da regra 7.
2. Leia o relatório:
   - **Perguntas para o usuário** → regra 9.
   - **BLOQUEADO** (ambiente sem a ferramenta, dependência inacessível, pergunta que o limite não permite responder) → leve ao usuário: ele ajusta o ambiente ou o limite e você continua com o mesmo agente, ou ele encerra o spike como inconclusivo.
   - **Relatório mal formado** (seção faltando, resposta sem marca de origem, caminho da worktree ausente) → peça ao mesmo agente só a correção do formato, uma vez. Se persistir, pare e informe o usuário.
3. Anote em `notas_de_retomada` o caminho da worktree e o nome da branch que o relatório informa. Sem isso, uma sessão nova não consegue remover o que sobrou.
4. Confira com `git status --porcelain` que a cópia principal não mudou. Se mudou, mostre ao usuário o que apareceu; não desfaça por conta própria.

### Etapa 2 — Resposta

1. Apresente ao usuário, de forma curta e sem reescrever a evidência (regra 5):
   - a pergunta e a hipótese confirmadas no Portão 1;
   - a **resposta**: `sim`, `não`, o número medido, ou `inconclusivo`;
   - a evidência: comandos, saídas relevantes, versões e ambiente, com as marcas de origem;
   - os limites de validade e o que não foi testado;
   - as referências consultadas, as lacunas de referência e as perguntas derivadas.
2. **Portão 2.** Pergunte se ele aceita a resposta.
   - **Aceitou** → Etapa 3.
   - **Pediu complemento dentro da mesma pergunta e do mesmo limite** (rodar de novo, mostrar outra saída, repetir a medição) → continue com o mesmo agente e volte a este portão. Um complemento só: se ainda não bastar, encerre como inconclusivo e sugira um spike novo com outro enquadramento.
   - **Pediu algo que muda a pergunta, o critério ou o limite** → é outro spike (regras 1 e 2): encerre este com o que foi observado.
3. Pergunte também o destino do resultado, só para registro: nenhum, decisão do arquiteto (modo `decisao`, fora deste fluxo) ou outro uso que o usuário indicar. Para cada lacuna de referência, pergunte se ele quer providenciar uma referência nova, fora deste fluxo, ou descartar. Você não inicia nenhum desses trabalhos.

### Etapa 3 — Encerramento

1. Grave o resultado como D-XXX pela `nova-memoria` (operação 5), no formato de `.claude/memoria/decisoes.md`:
   - **título:** `Spike: <pergunta, encurtada>`;
   - **Decisão:** a resposta (`sim`, `não`, número ou `inconclusivo`) em uma ou duas frases, com a data do experimento;
   - **Motivo:** a evidência, copiada do relatório: os comandos principais, a saída que decide, as versões e o ambiente;
   - **Alternativas descartadas:** a hipótese, se foi refutada; as abordagens comparadas que perderam, com o número;
   - **Afeta:** os limites de validade ("vale para X na versão Y; não testado: Z"), o destino que o usuário indicou e as lacunas de referência com a decisão dele.
   Um spike não é uma decisão do projeto: o D-XXX é o único registro versionado que a memória tem, e é por ele que o resultado pode ser citado (`[spike: D-XXX]`) e que ninguém repete o experimento.
2. Remova a worktree e a branch do experimento, pelos caminhos anotados na Etapa 1: `git worktree remove --force <caminho>` e `git branch -D <branch>`. Se o git recusar por trava, rode antes `git worktree unlock <caminho>`. São comandos que apagam trabalho: o usuário os aprova na hora, pelo fluxo normal de permissões. Confira com `git worktree list` e `git branch --list 'worktree-*'` que nada sobrou.
   - Se o escritor não escreveu nada, o Claude Code já removeu a worktree: confira e siga.
3. Feche a tarefa pela `nova-memoria` (operação 6, com resumo e confirmação do usuário). `decisoes.md` é versionado: diga ao usuário que a entrada nova está sem commit e pergunte se ele quer que você a commite (`docs(memoria): spike D-XXX`).

## Cancelamento

O usuário pode desistir em qualquer ponto. Você não desfaz nada por conta própria:

1. Mostre o que existe: a worktree e a branch do experimento (`git worktree list`), se já foram criadas.
2. Pergunte se o que foi observado até ali deve ser registrado. Se sim, grave o D-XXX com a resposta `inconclusivo` e o motivo do cancelamento.
3. Remova a worktree e a branch como na Etapa 3, passo 2.
4. Cancele a tarefa pela `nova-memoria` (operação 6, "Cancelar", com resumo e confirmação).
