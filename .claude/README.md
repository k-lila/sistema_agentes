# Sistema de agentes: apresentação

Este documento apresenta o sistema de agentes como um todo: quem são os agentes, como trabalham juntos, quais fluxos existem e o que mantém tudo funcionando entre uma sessão e outra. Ele é uma porta de entrada. O detalhe de cada parte está nos arquivos citados ao longo do texto, e são eles que valem se houver diferença.

## 1. A ideia central

O sistema funciona como um pequeno time de software em que **cada membro tem um papel só e não faz o trabalho do outro**:

- quem decide **o que** o produto faz não escreve código;
- quem escreve o código não escreve os testes;
- quem revisa não corrige.

A separação existe para que ninguém corrija a própria prova. Um teste escrito olhando o código só "fotografa" o que o código faz, bugs incluídos. Uma revisão feita por quem escreveu tende a concordar consigo mesma.

Cada membro do time é um **subagente** (`.claude/agents/`). A conversa principal faz o papel de **orquestrador**, que:

- decide quem trabalha em cada momento;
- entrega a cada agente **só o contexto que ele deve receber**, passando caminhos de arquivo, e não resumos;
- faz os commits e guarda o estado do trabalho na memória;
- leva a você as decisões importantes, nos **portões**.

O orquestrador **não arbitra conteúdo**. Se dois agentes discordam, ele leva a questão ao dono do artefato e repassa a resposta, sem decidir quem tem razão.

**Você decide nos portões.** Os agentes propõem e verificam, mas a aprovação de uma spec, a aceitação de uma ADR e a autorização de merge ou push são sempre suas.

## 2. Os seis agentes

| Agente | Responde por | Escreve em | Não faz |
| --- | --- | --- | --- |
| **gerente-de-produto** | o quê e o porquê: visão, spec, histórias, critérios de aceite (`CA-xx.y`), backlog | `docs/produto/` | código, testes, arquitetura técnica |
| **arquiteto** | as decisões estruturais (as caras de mudar depois): ADRs, contratos de fronteira e a bateria de testes de especificação (`TA-*`) | `docs/adr/`, `docs/contracts/`, `docs/testes/<slug>/especificacao.md` | código de produção ou de teste |
| **tester** | os testes automatizados, sempre a partir de exigências escritas (`TA-*`, `RG-*`, `TQ-*`) | código de teste | código de produção; decidir o comportamento esperado; enfraquecer um teste para ele passar |
| **escritor** | o código de produção e a documentação factual; o diagnóstico de defeitos; os experimentos descartáveis | código de produção, build, configuração, CI, Dockerfile, README | testes; mudar contrato ou ADR; decisões arquiteturais |
| **gerente-de-qualidade** | o parecer: veredito, achados (`GQ-*`) e demanda de testes (`TQ-*`) | nada (o orquestrador grava o parecer) | escrever ou corrigir código e testes |
| **senso-critico** | o exame das premissas de uma proposta antes de ela virar fundação: objeções, tensões e escaladas (`SC-*`) | só o próprio relatório novo, em `docs/senso-critico/SC-R-NNN.md` | decidir, vetar, implementar, avaliar qualidade de código |

### Dois agentes que costumam gerar dúvida

**gerente-de-qualidade.** Ele julga, não produz. Roda build, testes, cobertura e análise estática e avalia a mudança com base em normas técnicas: ISO/IEC 25010 e 5055, OWASP Top 10 e ASVS, CWE e o padrão de codificação segura da stack. O parecer tem:

| Campo | Valores |
| --- | --- |
| veredito | `aprovado`, `aprovado_com_ressalvas`, `bloqueado` |
| ação do orquestrador | `integrar`, `ciclo_de_correcao`, `pausar_e_escalar` |
| severidade de cada achado | **bloqueante** (impede a integração), **recomendado** (deve ser resolvido, mas não impede), **nit** (polimento) |

Pressão de prazo ou número de rodadas não mudam o veredito: só evidência muda.

**senso-critico.** Ele não confere se o trabalho cumpre os critérios (isso é do gerente-de-qualidade). Ele examina se **os critérios e as premissas** são os certos. Algumas regras dele:

- **Não é do contra.** Um relatório sem objeções é um resultado legítimo.
- **Só com gatilho.** Cada dúvida precisa apontar algo concreto no projeto (um arquivo, uma seção, um critério). Dúvida sem gatilho é descartada.
- **No máximo 5 itens** por relatório. O excedente vai para "Descartadas", descrito para ser retomado.
- **Três tipos de item:**
  - **objeção**: dirigida ao autor do artefato;
  - **tensão com fundação**: o autor da fundação dá parecer e outra parte decide;
  - **escalada**: depende de um fato ou de um juízo de valor que só você pode fornecer.
- Não examina código, `/bugfix` nem `/spike`.

### As regras de isolamento

Algumas informações são escondidas de propósito:

| Quem | Nunca recebe | Por quê |
| --- | --- | --- |
| gerente-de-qualidade | o relatório do escritor | para revisar o código sem ser guiado pela justificativa de quem o escreveu |
| tester | explicações do escritor sobre o resultado esperado | porque o esperado vem da spec, do contrato ou da ADR, nunca do código |
| senso-critico | os relatórios dos agentes e as explicações do orquestrador sobre os pontos `[INFERIDO]` | para examinar a proposta pelo que está escrito nela |

O princípio do tester resume a ideia: **o oráculo não é o código**. O tester pode ler o código para saber *como chamar* algo, mas nunca para saber *o que esperar*. Se a única forma de saber o esperado é olhar a implementação, ele devolve a exigência em vez de inventar.

### Os modos de cada agente

Cada agente trabalha em **modos**, e cada fluxo usa os modos de que precisa:

| Agente | Modos nos fluxos | Modo avulso (fora dos fluxos) |
| --- | --- | --- |
| gerente-de-produto | `discovery`, `lacuna`, `validacao`, `visao`, `critica` | `priorizacao` |
| arquiteto | `pacote`, `contestacao`, `fundacao` | `decisao` |
| tester | `especificacao`, `regressao`, `qualidade` | nenhum |
| escritor | `implementacao`, `correcao`, `fundacao`, `diagnostico`, `experimento` | nenhum |
| gerente-de-qualidade | uma revisão por rodada | nenhum |
| senso-critico | `exame` | nenhum |

Os agentes técnicos (arquiteto, tester, escritor, gerente-de-qualidade) não dependem da stack. O que é específico de uma linguagem ou framework (build, pastas, comandos, ferramentas) vem de um **perfil de stack**, como `.claude/skills/perfil-java-spring/`, escolhido na ADR de base do projeto.

## 3. Os identificadores

O sistema usa códigos curtos para que cada coisa possa ser citada e rastreada:

| Código | O que é | Quem cria |
| --- | --- | --- |
| `CA-xx.y` | critério de aceite de uma spec | gerente-de-produto |
| `TA-nnn` | teste de especificação, escrito **antes** do código | arquiteto |
| `TQ-nnn` | teste da demanda de qualidade, pedido **depois** da revisão | gerente-de-qualidade |
| `RG-nnn` | exigência de teste de regressão de um bug | orquestrador, no enquadramento do `/bugfix` |
| `GQ-nnn` | achado de revisão | gerente-de-qualidade |
| `SC-nnn` / `SC-R-NNN` | item e relatório do senso crítico | senso-critico |
| `ADR-NNNN` | registro de decisão de arquitetura | arquiteto (proposta); você (aceitação) |
| `TASK-NNN` | tarefa na memória | orquestrador |
| `A-N` | autorização de escrita dentro de uma tarefa | orquestrador, a partir da sua aprovação |
| `D-XXX` / `I-XXX` | decisão e impedimento registrados na memória | orquestrador |

## 4. Os fluxos de trabalho

Os fluxos são **skills** invocadas por você com `/`. Cada um tem etapas fixas e portões em que você decide.

### Qual fluxo usar

| Situação | Fluxo |
| --- | --- |
| projeto ainda sem base (visão, stack, build) | `/fundacao criar` |
| a base precisa mudar (visão, stack, ferramenta, CI) | `/fundacao alterar` |
| construir algo novo, ou mudar uma regra do produto | `/feature` |
| código já integrado diverge do que está escrito numa spec, contrato ou ADR | `/bugfix` |
| uma dúvida técnica que só se responde executando algo | `/spike` |
| retomar um fluxo interrompido | `/feature retomar <slug>`, `/fundacao retomar <slug>`, `/bugfix retomar <slug>` |

A ordem natural é: **`/fundacao` primeiro**, porque o `/feature` exige um projeto fundado; depois, um `/feature` por funcionalidade; `/bugfix` e `/spike` quando surgirem.

### `/fundacao`: a base do projeto

Produz um **projeto fundado**: a visão do produto (`docs/produto/visao.md`), uma ADR aceita que escolhe o perfil de stack e as ferramentas, e o build com essas ferramentas configuradas e verificadas.

```
0 Preparação
1 Visão .............. gerente-de-produto (visao)
                       → senso-critico → respostas   ── PORTÃO 1: você aprova a visão
2 Decisão de base .... arquiteto (fundacao)
                       → senso-critico → respostas   ── PORTÃO 2: você grava "Aceito" na ADR e aprova a especificação
3 Build e CI ......... escritor
4 Teste de fumaça .... tester                         → vermelho: a aplicação ainda não existe
5 Aplicação mínima ... escritor                       → fumaça verde
6 Verificação ........ orquestrador roda todas as ferramentas do perfil
7 Encerramento ........................................ ── PORTÃO 3: você autoriza o merge
```

- O gerente-de-qualidade não participa. A base é verificada pela execução das próprias ferramentas (Etapa 6), e a primeira revisão acontece no primeiro `/feature`.
- No modo `alterar`, só rodam as etapas que a mudança afeta. Uma ADR aceita nunca é editada: a mudança vira uma ADR nova que substitui a antiga.

### `/feature`: o fluxo principal

```
0 Preparação
1 Produto ............ gerente-de-produto (discovery)
                       → senso-critico → respostas   ── PORTÃO 1: você aprova a spec
2 Pacote técnico ..... arquiteto (pacote)
                       → senso-critico → respostas   ── PORTÃO 2: você aceita ADRs, contratos e especificação de testes
3 Testes primeiro .... tester (especificacao)         → testes vermelhos pelo motivo certo
4 Implementação ...... escritor (implementacao)       → testes da etapa 3 verdes
5 Revisão ............ gerente-de-qualidade (rodada n)
      ├─ integrar ............ → 7
      ├─ ciclo_de_correcao ... → 6 → 5 (rodada n+1)
      └─ pausar_e_escalar .... → dono do problema → retoma
6 Correção ........... tester (qualidade) → escritor (correcao)
7 Validação .......... gerente-de-produto (validacao) confere os critérios de aceite
8 Encerramento ........................................ ── PORTÃO 3: você autoriza merge, push ou PR
```

O que vale entender neste fluxo:

- **Os testes vêm antes do código** (Etapa 3). Cada `TA-*` declara se deve falhar antes da implementação, e um resultado diferente do declarado é tratado como suspeito.
- **Há duas listas de testes.** A primeira (`TA-*`) é do arquiteto, escrita antes do código. A segunda (`TQ-*`) é do gerente-de-qualidade e cobre o que só se enxerga com o código pronto.
- **O limite é de 3 rodadas de revisão.** Se a rodada 3 terminar com veredito `bloqueado`, o fluxo para e você decide como seguir.
- **Cada etapa gera dois commits:** o do agente, só com os arquivos do papel dele, e o do orquestrador, com o registro da execução (`docs/execucoes/<slug>.md`). Isso permite ao gerente-de-qualidade conferir, commit a commit, que cada etapa só tocou os caminhos do próprio papel.
- **O registro da execução** guarda commits, portões, mapa de testes e disposições. É por ele que um fluxo se retoma em outra sessão.
- **Nada de push, merge ou rebase** sem a sua autorização no Portão 3.

### `/bugfix`: corrigir um defeito

Bug, aqui, é **código integrado que diverge de uma fonte escrita**: um critério de aceite, um contrato ou uma diretriz de ADR aceita. Sem essa fonte não há como dizer qual é o comportamento correto, e o caso não é bugfix.

| Não é `/bugfix` | Caminho |
| --- | --- |
| nenhuma fonte define o comportamento esperado | gerente-de-produto (modo `lacuna`) ou `/feature` |
| a fonte define o comportamento, mas você quer outro | `/feature` |
| a correção exige mudar contrato, ADR ou a estrutura entre módulos | arquiteto (modo `decisao`) e depois `/feature` |
| o defeito está numa branch de feature ainda não integrada | o ciclo de correção do próprio `/feature` |
| a base do projeto está quebrada (build, ferramenta, pipeline) | `/fundacao alterar` |

```
0 Enquadramento ...... orquestrador: sintoma, reprodução, esperado × observado, fonte
1 Diagnóstico ........ escritor (diagnostico), sem alterar nada
                                                  ── PORTÃO 1: você confirma o diagnóstico e o escopo
2 Regressão .......... tester (regressao)          → teste vermelho pelo motivo do bug
3 Correção ........... escritor (correcao)         → regressão verde, suíte inteira verde
4 Revisão ............ gerente-de-qualidade (rodada n), com ciclo de correção
5 Encerramento .................................. ── PORTÃO 2: você autoriza merge ou push
```

- A correção é **mínima e fica no escopo confirmado** no Portão 1. Um arquivo a mais volta a você.
- O `/bugfix` não muda spec, contrato nem ADR e não refatora. Melhorias notadas no caminho viram sugestões, apresentadas no Portão 2.
- Vale o mesmo limite de 3 rodadas de revisão.

### `/spike`: experimento descartável

Responde a **uma** pergunta cuja resposta depende de executar algo neste projeto, com esta stack e estas versões. Serve para viabilidade, comportamento de ferramenta, comparação entre abordagens ou medição.

```
0 Enquadramento ...... orquestrador        ── PORTÃO 1: você confirma pergunta, hipótese, critério e limite
1 Experimento ........ escritor (experimento), numa worktree isolada
2 Resposta ........... orquestrador        ── PORTÃO 2: você aceita a resposta
3 Encerramento ....... D-XXX, remoção da worktree, fechamento da tarefa
```

- **O critério vem antes do resultado.** A pergunta, a hipótese e o critério ficam fixos no Portão 1.
- **O código não sobrevive.** Nada da worktree vai para a cópia principal, nem a pedido. Uma ideia boa volta pelo `/feature`.
- **Resultado negativo ou inconclusivo também é resultado.** Todo spike termina num `D-XXX`, com a evidência.
- **O spike informa, não decide.** Não cria ADR nem muda spec, contrato ou referência.
- **Só roda sem tarefa ativa.** Uma dúvida que surja dentro de outro fluxo vira impedimento lá.

### O que acontece num portão

Antes dos portões 1 e 2 do `/feature` e do `/fundacao`, roda a **rodada do senso crítico**:

1. O crítico examina a proposta.
2. Cada item vai a quem deve responder.
3. O orquestrador grava as respostas no relatório.
4. Você vê tudo no portão: os itens, as respostas, as lacunas e as suposições dos artefatos.

A rodada não substitui o portão: prepara o que você vai julgar.

No portão você aprova, pede mudanças ou decide os itens que são seus (tensões com a visão ou a spec, e escaladas).

Uma regra importante: **a linha `Aceito` de uma ADR é gravada por você, à mão**. Nem o orquestrador nem os agentes a gravam, e o hook de escrita impede que a IA a escreva.

## 5. A infraestrutura por trás

### Regras (`.claude/regras/`)

São carregadas em toda sessão pelo `CLAUDE.md`:

| Arquivo | O que define |
| --- | --- |
| `inviolaveis.md` | só criar, modificar ou excluir com permissão explícita; não refatorar fora do escopo; não tratar erros impossíveis; perguntar antes quando a tarefa envolve mais de 3 arquivos |
| `metodo.md` | o relatório antes de cada alteração (razões, arquivos a criar, arquivos a modificar) e o formato das perguntas (opção, justificativa, ao menos um pró e um contra) |
| `memoria.md` | o protocolo de memória (ver abaixo) |
| `referencias.md` | a regra das referências técnicas (ver abaixo) |

Dentro dos fluxos, as confirmações da Etapa 0 e dos portões substituem o relatório prévio e a permissão arquivo a arquivo, só para os caminhos autorizados da tarefa.

### Memória (`.claude/memoria/`)

É o que dá continuidade ao trabalho entre sessões.

| Arquivo | Conteúdo | No Git? |
| --- | --- | --- |
| `task.json` | a tarefa em execução: objetivo, critérios de aceite, plano, autorizações, próximo passo | não (estado local) |
| `roadmap.json` | a visão de um trabalho com várias tarefas | não (estado local) |
| `decisoes.md` | decisões `D-XXX` | sim (histórico) |
| `impedimentos.md` | impedimentos `I-XXX`, abertos e resolvidos | sim (histórico) |

- **Estado, não histórico.** `task.json` e `roadmap.json` descrevem o agora e voltam ao modelo vazio quando a tarefa ou o roadmap fecha. O histórico fica em `decisoes.md`, `impedimentos.md`, nas ADRs e em `docs/execucoes/`.
- **Só o orquestrador escreve**, seguindo a skill `nova-memoria`. Os subagentes devolvem a informação.
- **Algumas operações exigem sua confirmação**, com um resumo antes: abrir ou reestruturar um roadmap, fechar ou cancelar uma tarefa, reiniciar arquivos. As atualizações de rotina não pedem.
- **A tarefa só fecha** com todos os critérios de aceite verificados e com evidência, sem pendências e sem impedimento aberto.
- **Autorizações.** Com uma tarefa ativa, escrever fora das autorizações dela (`A-N`) faz o sistema pedir confirmação.

### Hooks (`.claude/hooks/`)

São scripts que o Claude Code roda automaticamente, configurados em `.claude/settings.json`:

| Hook | Quando roda | O que faz |
| --- | --- | --- |
| `memoria_contexto.py` | início de sessão | injeta um resumo do estado da memória e recria `task.json` e `roadmap.json` a partir dos modelos, se faltarem (num clone novo, por exemplo) |
| `proteger_escrita.py` | antes de cada escrita | nega a subagentes escrever na memória ou em caminhos de outro papel; pede confirmação para escrita fora das autorizações da tarefa ativa; nega a gravação de `Aceito` ou `Substituído por` em ADR |
| `validar_memoria.py` | depois de cada escrita | valida a estrutura da memória. Erro estrutural volta para correção na hora. Também roda à mão: `python3 -I .claude/hooks/validar_memoria.py --tudo` |

Limite conhecido: escrita via Bash fora da memória não passa pela checagem de autorizações. A conferência por git do orquestrador e do gerente-de-qualidade cobre esse caso.

### Referências (`docs/referencias/`)

São as referências técnicas do projeto e o **primeiro caminho para qualquer dúvida técnica**, de todos os agentes. Como usá-las:

- **Consulta.** Comece pelo índice `docs/referencias/README.md` e leia só a seção pertinente, nunca o documento inteiro.
- **Rastro.** Quem usa uma referência a cita (`[ref: <documento> §<seção>]`). Quem não achou a resposta registra a lacuna.
- **Hierarquia.** A referência informa, mas não decide: ADR aceita, contrato e spec continuam valendo. Uma contradição é relatada a quem decide.

### Outras peças

| Peça | Para quê |
| --- | --- |
| `.claude/quality/` | o checklist de qualidade e o esquema JSON do parecer, usados pelo gerente-de-qualidade |
| skill `nova-memoria` | como escrever na memória |
| skill `nova-adr` | como criar e gerenciar ADRs (formato de Michael Nygard, com alternativas consideradas) |
| skill `perfil-java-spring` | o perfil de stack Java/Spring Boot; não é invocado diretamente |
| skill `auditar-critico` | auditoria do senso crítico, de uso exclusivo seu, só com gatilho concreto (ADR substituída, bug numa premissa examinada pelo crítico ou recusas recorrentes). O orquestrador monta o dossiê e você julga |

## 6. Onde está cada coisa

| Caminho | Conteúdo |
| --- | --- |
| `CLAUDE.md` | ponto de entrada da IA: propósito, mapa do projeto e importação das regras |
| `.claude/agents/` | a definição de cada agente: papel, modos, limites e formato do relatório |
| `.claude/skills/<nome>/SKILL.md` | cada fluxo e skill, etapa por etapa |
| `.claude/regras/` | as regras que a IA segue |
| `.claude/memoria/` | o estado e o histórico do trabalho |
| `.claude/hooks/` e `.claude/settings.json` | os fiscais automáticos e as permissões |
| `docs/produto/` | visão, backlog e specs |
| `docs/adr/` | as decisões de arquitetura |
| `docs/contracts/` | os contratos de fronteira |
| `docs/testes/` | especificações de teste, enquadramentos de bug e pareceres |
| `docs/senso-critico/` | os relatórios do senso crítico |
| `docs/execucoes/` | o registro de cada execução de fluxo |
| `docs/referencias/` | as referências técnicas |

Para aprofundar, leia o `SKILL.md` do fluxo e o arquivo do agente envolvido. Este documento resume; eles definem.
