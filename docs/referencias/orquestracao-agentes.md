# Orquestração de agentes no Claude Code — guia didático

Oct 14, 2026 · @klila

## Resumo

**Objetivo.** Mostrar como montar, com as peças do Claude Code e com documentação de projeto, um ecossistema de agentes em que cada agente sabe o que fazer, com que regras, a partir de que estado e como provar que terminou.

**Conclusões, em ordem de prioridade:**

1. **Contexto é o recurso escasso.** Carregue só o que a tarefa pede: CLAUDE.md curto e como mapa, skills sob demanda, subagentes em contexto isolado.
2. **Instrução é pedido; hook, permissão e teste são garantia.** O que precisa valer sempre deve ser imposto por um mecanismo, não só escrito.
3. **Separe constituição, conhecimento e estado**, porque misturá-los é a causa mais comum de agentes "perdidos".
4. **Um subagente não vê a conversa.** O que ele precisa saber tem de estar no prompt dele, no CLAUDE.md ou num arquivo que ele saiba ler.
5. **A documentação do projeto dá aos agentes critério de decisão e de parada** (ADRs, escopo, specs, requisitos não funcionais, definição de pronto), e as regras executáveis impedem que ela envelheça.
6. **Para muitas rodadas, o roadmap mantém a coerência**, e a automação desloca os portões humanos, sem eliminá-los.

**Perfil da evidência.** As afirmações sobre o Claude Code vêm da documentação oficial consultada em 14 de outubro de 2026 e podem mudar rápido; vários recursos são experimentais ou de prévia. ADRs, ArchUnit, migrations e estratégia de testes são práticas gerais de engenharia. A estrutura de pastas, a pasta `memoria/`, o protocolo de propriedade e as skills de exemplo são propostas deste guia, não da documentação.

## Como ler este guia

### Fontes e pesos

| Tipo de fonte | Exemplos | Peso | Limite |
| --- | --- | --- | --- |
| Documentação oficial do Claude Code | As páginas da seção 23, consultadas em 14 de outubro de 2026 | Alto, para o comportamento do produto naquela data | É o fornecedor descrevendo o próprio produto; números, limites e nomes de campo mudam |
| Referência de hooks em outro domínio | Hooks reference em docs.anthropic.com, conferida na revisão | Alto, para o ponto conferido | Usada só para o código de saída 2 por evento |
| Práticas gerais de engenharia de software | ADRs (Nygard, 2011), ArchUnit, migrations, estratégia de testes | Médio | Sem fonte específica citada neste guia |
| Propostas deste guia | `memoria/`, protocolo de propriedade, `/feature`, `/handoff`, `/roadmap`, `/fechar-marco` | De proposta | Escolhas do autor, montadas sobre as peças documentadas; não foram executadas aqui |

### Princípios de ponderação

1. **A documentação descreve o produto numa data.** Confira a página correspondente antes de configurar algo grande.
2. **Recurso experimental, de prévia ou beta vale menos como base de processo.** O estado de cada um vem marcado no texto.
3. **Prática geral sem fonte citada é convenção, não fato verificado.**
4. **Proposta do guia é escolha, não exigência.** Pode ser trocada sem contrariar a documentação.
5. **Garantia vale mais do que instrução.** É o critério dos três níveis de garantia da seção 15.

### Tipo de cada afirmação

Cada afirmação do guia é de um destes tipos: **Documentado** (está na documentação oficial consultada em 14 de outubro de 2026), **Prática geral** (engenharia de software, fora da documentação do Claude Code), **Proposta deste guia** (escolha do autor) ou **Inferência** (conclusão que decorre das fontes indicadas, marcada como **Inferência** (de …)). Quando um recurso é experimental, de prévia ou beta, o texto o diz.

| Seções | Tipo predominante | Estado dos recursos citados |
| --- | --- | --- |
| 2 a 9 | Documentado | Hooks do tipo `agent` marcados como experimentais |
| 10 | Documentado | Agent view em prévia de pesquisa; agent teams experimental e desativado por padrão |
| 11 | Documentado (padrões do guia de boas práticas) | — |
| 12 e 15 | Prática geral, com ligações documentadas (hooks, permissões) | — |
| 13 e 14 | Prática geral e Proposta deste guia; elementos de uma boa spec documentados | — |
| 16 e 17 | Proposta deste guia, apoiada em comportamento documentado | — |
| 18 e 19 | Proposta deste guia (exemplo) | — |
| 20 e 21 | Proposta deste guia; laço com `claude -p` documentado | Projects em beta pública, segundo a documentação |
| 22 | Documentado e Proposta deste guia | — |

Depois da seção 22 vêm, sem numeração, os exemplos e o que demonstram, o que as fontes não decidem, os limites, o checklist e o mapa de consulta.

### Conceitos

| Termo | Definição | Fonte |
| --- | --- | --- |
| CLAUDE.md | Instruções persistentes lidas no início de toda sessão, tratadas como contexto e não como configuração imposta | [Memory](https://code.claude.com/docs/en/memory.md) |
| Regra (`.claude/rules/`) | Arquivo de instruções por tema; com `paths`, só carrega ao trabalhar com arquivos que casam | Memory |
| Auto memory | Anotações que o próprio Claude escreve, locais da máquina | Memory |
| Subagente | Assistente especializado com janela de contexto, prompt, ferramentas e permissões próprios, que devolve só um resumo | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| Fork | Subagente que herda a conversa inteira | Subagents |
| Skill | Pasta com um `SKILL.md` de conhecimento ou procedimento, cujo corpo só carrega quando é usada | [Skills](https://code.claude.com/docs/en/skills.md) |
| Divulgação progressiva | Carregar só o que a tarefa pede, no momento em que pede | [Features overview](https://code.claude.com/docs/en/features-overview.md); Skills |
| Hook | Comando executado em ponto fixo do ciclo de vida, como controle determinístico | [Hooks](https://code.claude.com/docs/en/hooks-guide.md) |
| Regra de permissão | `allow`, `ask` ou `deny`, aplicada pelo Claude Code e não pelo modelo | [Permissions](https://code.claude.com/docs/en/permissions.md) |
| MCP | Protocolo que conecta o Claude a serviços fora do repositório | Features overview |
| Plugin | Pacote instalável de skills, subagentes, hooks e servidores MCP | [Plugins](https://code.claude.com/docs/en/plugins/create.md) |
| Plan mode | Modo em que o Claude lê e roda comandos somente leitura, sem editar código-fonte | Permissions; [Best practices](https://code.claude.com/docs/en/best-practices.md) |
| Worktree | Segunda cópia de trabalho do repositório, numa branch própria | [Agents](https://code.claude.com/docs/en/agents.md) |
| Agent teams | Líder que distribui trabalho a teammates que trocam mensagens; experimental | Agents |
| ADR | Registro de uma decisão arquitetural, com contexto, escolha e consequências | Prática geral (Nygard, 2011) |
| Walking skeleton | Esqueleto que compila, testa e roda o CI antes de qualquer feature | Prática geral |
| Deriva | Rodadas localmente corretas cujo conjunto perde coerência | Proposta deste guia |

## 1. Introdução

Um ecossistema de agentes funciona bem quando cada agente sabe **o que fazer, com que regras, a partir de que estado e como provar que terminou**. O Claude Code oferece as peças para isso (CLAUDE.md, subagentes, skills, comandos, hooks, permissões, MCP, plugins, worktrees e agent teams), mas elas só rendem quando apoiadas em documentação de projeto bem organizada.

Este guia tem três partes:

| Parte | Seções | Pergunta que responde |
| --- | --- | --- |
| Ferramentas do Claude Code | 2 a 11 | Com que peças se monta um sistema de agentes? |
| Documentação do projeto | 12 a 17 | Que arquivos dão contexto e regras aos agentes? |
| Orquestração na prática | 18 a 22 | Como tudo trabalha junto numa tarefa e ao longo de muitas rodadas? |

Todo ecossistema bem montado responde a quatro perguntas, e cada arquivo descrito adiante responde a pelo menos uma delas:

- **Por quê?** Decisões e seus motivos (ADRs, requisitos não funcionais).
- **Para quê?** O que o sistema deve e não deve fazer (escopo, specs).
- **Como fazemos aqui?** Convenções, estratégia de testes, definição de pronto.
- **Onde estamos?** Estado atual, plano em andamento, histórico.

As afirmações sobre o Claude Code foram conferidas na documentação oficial em outubro de 2026 (links na seção 23). O produto evolui rápido: números de versão, limites e nomes de campos podem mudar, então confira a página correspondente antes de configurar algo grande.

## 2. Fundamentos: contexto é o recurso escasso

Todo recurso do Claude Code consome janela de contexto, e contexto demais não só esgota a janela como gera ruído: skills deixam de disparar e convenções se perdem. A documentação oficial resume o custo de cada recurso assim:

| Recurso | Quando carrega | O que carrega | Custo de contexto |
| --- | --- | --- | --- |
| CLAUDE.md | Início da sessão | Conteúdo completo | Em toda requisição |
| `.claude/rules/` | Início da sessão, ou ao abrir arquivos que casam com `paths` | Conteúdo da regra | Em toda requisição, ou só quando relevante |
| Skills | Início (descrição) e ao usar (corpo) | Nome e descrição; corpo sob demanda | Baixo até ser usada |
| Servidores MCP | Início da sessão | Nomes das ferramentas; esquemas sob demanda | Baixo até usar uma ferramenta |
| Subagentes | Quando criados | Contexto novo e isolado | Isolado da sessão principal |
| Hooks | No evento | Nada, a menos que o hook devolva saída | Zero, salvo a saída |

Disso saem três princípios que orientam todo o guia.

**Divulgação progressiva.** Carregue só o que a tarefa pede, no momento em que pede. O CLAUDE.md fica curto (a documentação recomenda menos de 200 linhas) e aponta para o resto; material de referência vai para skills ou regras com escopo de caminho.

**Instrução é pedido; hook é garantia.** A documentação é explícita: uma regra como "nunca edite `.env`" no CLAUDE.md ou numa skill é um pedido, e um hook `PreToolUse` que bloqueia a edição é imposição. O que precisa valer sempre vira hook, permissão ou teste.

**Camadas de volatilidade.** Separe o que muda raramente do que muda a cada sessão, porque misturar os dois é a causa mais comum de agentes "perdidos":

| Camada | Frequência de mudança | Exemplos | Onde mora |
| --- | --- | --- | --- |
| Constituição | Raramente | Regras inegociáveis, comandos, mapa | `CLAUDE.md`, `.claude/rules/` |
| Conhecimento | A cada decisão | ADRs, specs, contratos, glossário | `docs/` |
| Estado | A cada sessão | Plano atual, progresso, pendências | `memoria/` |

A documentação também sugere montar o ecossistema aos poucos, por gatilho, em vez de configurar tudo de uma vez:

| Quando acontece isto | Acrescente |
| --- | --- |
| Claude erra a mesma convenção duas vezes | Uma linha no CLAUDE.md |
| Você digita o mesmo prompt para iniciar uma tarefa | Uma skill invocável |
| Você cola o mesmo procedimento pela terceira vez | Uma skill de referência |
| Uma tarefa lateral inunda a conversa com saída | Um subagente |
| Algo precisa acontecer sempre, sem pedir | Um hook |
| Você copia dados de um sistema que Claude não vê | Um servidor MCP |
| Outro repositório precisa da mesma configuração | Um plugin |

## 3. CLAUDE.md, regras e memória automática

O CLAUDE.md é a **constituição** do projeto: instruções persistentes que o Claude lê no início de toda sessão. A documentação ressalta que ele é tratado como contexto, não como configuração imposta, então instruções concretas e verificáveis funcionam melhor que vagas ("rode `./mvnw test` antes de commitar" em vez de "teste suas mudanças").

### Onde ficam e como carregam

| Escopo | Local | Para quê |
| --- | --- | --- |
| Usuário | `~/.claude/CLAUDE.md` | Preferências pessoais em todos os projetos |
| Projeto | `./CLAUDE.md` ou `./.claude/CLAUDE.md` | Regras do time, versionadas no Git |
| Local | `./CLAUDE.local.md` (no `.gitignore`) | Preferências pessoais só neste projeto |
| Subpasta | `backend/CLAUDE.md` etc. | Regras de um módulo, carregadas sob demanda |

Os arquivos não se sobrescrevem: são **concatenados**, do diretório raiz até o de trabalho. Os de subpastas só entram quando o Claude lê ou edita um arquivo naquela pasta, o que mantém o contexto enxuto em projetos com vários módulos.

### Imports com `@` e a armadilha do custo

Um CLAUDE.md pode importar outros arquivos com `@caminho/arquivo.md` (até quatro níveis de profundidade). Atenção: arquivos importados **carregam inteiros no início da sessão**. Importar organiza, mas não reduz o custo de contexto.

Por isso, num CLAUDE.md que funciona como mapa, cite os documentos grandes **entre crases**, sem `@`. A documentação confirma que um caminho entre crases não é importado; ele fica como texto, e o agente lê o arquivo quando precisar.

### `.claude/rules/`: regras por tema e por caminho

Para não inchar o CLAUDE.md, divida instruções em arquivos de `.claude/rules/`. Uma regra com o campo `paths` só carrega quando o Claude trabalha com arquivos que casam com o padrão:

```markdown
---
paths:
  - "src/main/java/**/security/**"
---
# Regras de segurança
- Toda senha passa por BCrypt; nunca armazene texto puro.
- Tokens nunca aparecem em logs.
- Consulte `docs/seguranca.md` antes de alterar fluxos de login.
```

### Memória automática

Além do CLAUDE.md (que você escreve), existe a **auto memory** (que o Claude escreve): anotações sobre correções, preferências e contexto que não se deduz do código. Fica em `~/.claude/projects/<projeto>/memory/`, com um índice `MEMORY.md` cujas primeiras 200 linhas ou 25 KB carregam em toda sessão. Ela é local da máquina e não é compartilhada pelo Git, então não substitui os arquivos de estado versionados da seção 16.

### Exemplo de CLAUDE.md como mapa

```markdown
# IdP Java/Spring

## Regras inegociáveis
- Nunca altere testes para fazê-los passar.
- Não altere contratos em `docs/contratos/` sem ADR aceita.
- Dados sensíveis nunca vão para logs.

## Comandos
- Testes: `./mvnw test`   - Build: `./mvnw package`

## Onde está cada coisa (leia quando relevante)
- Início de sessão: `memoria/estado.md`
- Visão geral: `docs/visao-geral.md`
- Decisões: `docs/adr/` (vale só status "aceita")
- Autenticação: `docs/seguranca.md`
- Termos do domínio: `docs/glossario.md`
- Problemas de ambiente: `docs/armadilhas.md`
- Próximo trabalho: `docs/roadmap.md` (item com status "próximo")

## Protocolo de memória
- Ao fim de cada etapa, atualize `memoria/estado.md`.
- Decisão arquitetural nova: proponha ADR com status "proposta".
```

Ferramentas úteis: `/init` gera um CLAUDE.md inicial, `/memory` lista e abre os arquivos de memória, `/context` mostra quais carregaram, e `/doctor prompt-audit` procura instruções desatualizadas ou contraditórias.

### Cinco lugares de instrução e memória que costumam se confundir

| | CLAUDE.md | Regras (`.claude/rules/`) | Skills | Auto memory | Memória de subagente |
| --- | --- | --- | --- | --- | --- |
| Quem escreve | Você | Você | Você | O Claude, por iniciativa | O próprio subagente |
| Quando carrega | Início da sessão, inteiro; os de subpasta sob demanda | Início da sessão, ou ao trabalhar com arquivos que casam com `paths` | Descrição no início; corpo ao ser usada | Primeiras 200 linhas ou 25 KB do `MEMORY.md`, em toda sessão | — |
| Onde fica | `./CLAUDE.md`, `./.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`, subpastas | `.claude/rules/` | `.claude/skills/<nome>/SKILL.md` e outros locais | `~/.claude/projects/<projeto>/memory/` | `.claude/agent-memory/<nome>/` (com `memory: project`) |
| Compartilhado pelo Git | Sim, no escopo de projeto | Sim | Sim, no escopo de projeto | Não, é local da máquina | Sim |
| Para quê | Constituição e mapa | Instruções por tema ou por caminho | Procedimentos e conhecimento sob demanda | Correções, preferências e contexto que não se deduz do código | Aprendizado de longo prazo de um especialista |
| Fonte | Memory | Memory; Features overview | Skills | Memory | Subagents |

"—" indica que o guia não registra o ponto. A pasta `memoria/` (seção 16) é outro mecanismo: uma proposta deste guia para o estado da tarefa em curso.

## 4. Subagentes: os especialistas

Um subagente é um assistente especializado que roda na **própria janela de contexto**, com prompt de sistema, ferramentas e permissões próprios, e devolve só um resumo à conversa principal. A documentação lista cinco usos: preservar contexto, impor restrições de ferramentas, reutilizar configurações, especializar comportamento e controlar custo usando modelos mais baratos.

### Onde ficam

| Local | Escopo | Prioridade |
| --- | --- | --- |
| Configuração gerenciada | Organização | 1 (maior) |
| Flag `--agents` (JSON) | Sessão atual | 2 |
| `.claude/agents/` | Projeto (versionado) | 3 |
| `~/.claude/agents/` | Todos os seus projetos | 4 |
| Pasta `agents/` de um plugin | Onde o plugin está ativo | 5 (menor) |

Se dois têm o mesmo `name`, vence o de maior prioridade. As pastas são lidas recursivamente, então dá para organizar em `agents/revisao/`, `agents/pesquisa/` etc.

### Anatomia de um subagente

É um Markdown com frontmatter YAML; o corpo vira o prompt de sistema. Só `name` e `description` são obrigatórios. Os campos mais úteis para orquestração:

| Campo | Para que serve |
| --- | --- |
| `description` | Critério de roteamento: o Claude usa para decidir quando delegar |
| `tools` / `disallowedTools` | Lista de permitidas ou negadas (ex.: revisor sem `Edit` e `Write`) |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, ID completo ou `inherit` |
| `permissionMode` | Modo de permissão do subagente (ex.: `plan` para só leitura) |
| `skills` | Skills pré-carregadas inteiras no início |
| `memory` | Memória persistente própria: `user`, `project` ou `local` |
| `isolation: worktree` | Roda numa cópia isolada do repositório (worktree Git temporária) |
| `hooks` | Hooks válidos só enquanto esse subagente roda |
| `maxTurns` | Limite de turnos antes de parar |

### O que o subagente recebe ao nascer

O subagente **não vê o histórico da conversa** nem os arquivos que o Claude já leu. Ele recebe: seu próprio prompt (não o prompt de sistema completo do Claude Code), a mensagem de delegação escrita pelo Claude, os arquivos CLAUDE.md, um retrato do `git status` e as skills listadas em `skills`. Os nativos Explore e Plan pulam o CLAUDE.md e o git status, e o campo `omitClaudeMd: true` faz o mesmo num subagente seu.

Consequência prática: tudo que o subagente precisa saber tem de estar no prompt dele, no CLAUDE.md ou num arquivo que ele saiba ler. É aqui que os documentos das seções 12 a 16 entram.

### Subagentes nativos

| Nome | Ferramentas | Uso |
| --- | --- | --- |
| Explore | Só leitura | Busca e análise do código |
| Plan | Só leitura | Pesquisa durante o plan mode |
| general-purpose | Todas as disponíveis | Tarefas com exploração e modificação |

### Exemplo: revisor somente leitura

```markdown
---
name: revisor
description: Revisa diffs contra ADRs e docs/seguranca.md. Use após qualquer implementação.
tools: Read, Grep, Glob, Bash
model: inherit
memory: project
---
Você é um revisor sênior. Ao ser chamado:
1. Rode `git diff` e foque nos arquivos alterados.
2. Confira cada mudança contra `docs/seguranca.md` e as ADRs aceitas em `docs/adr/`.
3. Responda em três blocos: Crítico (bloqueia), Aviso, Sugestão.
4. Aprove só se não houver item Crítico.
Consulte sua memória por problemas recorrentes e registre novos padrões ao final.
```

Um detalhe que a documentação registra: com o campo `memory`, o Claude Code habilita **Read, Write e Edit** automaticamente para o subagente cuidar da própria memória. **Inferência** (da página de subagentes): este revisor ganha permissão de escrita mesmo sem `Edit` em `tools`. Se a garantia de que ele nunca edita código for essencial, remova `memory` ou acrescente um hook `PreToolUse` no frontmatter dele que só permita escrita em `.claude/agent-memory/`.

### Como acionar

- **Automático:** o Claude delega quando a tarefa casa com a `description`. Frases como "use proativamente" na descrição incentivam a delegação.
- **Por linguagem natural:** "Use o subagente revisor para olhar minhas mudanças".
- **Por @-menção:** `@agent-revisor` garante que aquele subagente rode.
- **Sessão inteira:** `claude --agent revisor` faz a thread principal assumir o prompt, as ferramentas e o modelo dele.

### Limites e correções em relação a versões antigas

- Subagentes **podem** criar subagentes próprios, até três níveis abaixo da conversa principal por padrão (ajustável com `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). Versões antigas não permitiam; guias desatualizados ainda dizem o contrário.
- Por padrão, até 20 subagentes rodam ao mesmo tempo numa sessão.
- O Claude pode **retomar** um subagente terminado com `SendMessage`, mantendo todo o histórico dele.
- Um **fork** (comando `/subtask`) é um subagente que herda a conversa inteira, útil quando explicar o contexto custaria demais.

## 5. Skills: os manuais

Uma skill é uma pasta com um `SKILL.md` contendo conhecimento ou um procedimento. Diferente do CLAUDE.md, o **corpo da skill só carrega quando é usada**, então material longo custa quase nada até ser necessário. A documentação sugere criar uma skill quando você cola as mesmas instruções várias vezes ou quando uma parte do CLAUDE.md virou procedimento em vez de fato.

### Dois tipos de conteúdo

| Tipo | O que contém | Exemplo | Como costuma ser acionada |
| --- | --- | --- | --- |
| Referência | Conhecimento aplicado ao trabalho atual | Convenções de API, padrões de erro | Pelo Claude, quando relevante |
| Tarefa | Passo a passo de uma ação | Deploy, commit, gerar ADR | Por você, com `/nome` |

### Onde ficam

| Local | Caminho | Carrega em |
| --- | --- | --- |
| Pessoal | `~/.claude/skills/<nome>/SKILL.md` | Todos os seus projetos |
| Projeto | `.claude/skills/<nome>/SKILL.md` | Este repositório (versionável) |
| Aninhada | `<subpasta>/.claude/skills/<nome>/SKILL.md` | Quando o Claude trabalha naquela subpasta |
| Plugin | `<plugin>/skills/<nome>/SKILL.md` | Onde o plugin está ativo, como `/plugin:nome` |

### Divulgação progressiva em três níveis

1. **Descrição:** fica sempre no contexto para o Claude saber que a skill existe (limitada a 1.536 caracteres somando `description` e `when_to_use`).
2. **Corpo do `SKILL.md`:** carrega quando a skill é invocada. A recomendação é ficar abaixo de 500 linhas.
3. **Arquivos de apoio:** referências, exemplos e scripts na mesma pasta, lidos ou executados só quando o corpo manda.

```text
.claude/skills/nova-adr/
├── SKILL.md          # instruções e navegação
├── template.md       # modelo de ADR, lido quando necessário
└── scripts/
    └── proximo-numero.sh   # executado, não carregado
```

### Campos de frontmatter mais úteis

| Campo | Efeito |
| --- | --- |
| `description` | Critério para o Claude carregar a skill sozinho |
| `disable-model-invocation: true` | Só você aciona; use para ações com efeito colateral |
| `user-invocable: false` | Só o Claude aciona; use para conhecimento de fundo |
| `allowed-tools` | Ferramentas pré-aprovadas no turno em que a skill roda |
| `context: fork` + `agent` | Executa a skill num subagente isolado (ex.: `agent: Explore`) |
| `paths` | Só ativa automaticamente ao trabalhar com arquivos que casam |
| `arguments`, `argument-hint` | Argumentos nomeados e dica de uso |

### Exemplo: skill de tarefa que gera ADR

```markdown
---
name: nova-adr
description: Cria uma ADR numerada a partir do template do projeto.
argument-hint: <título da decisão>
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/proximo-numero.sh)
---
Próximo número: !`${CLAUDE_SKILL_DIR}/scripts/proximo-numero.sh`

Crie `docs/adr/<número>-<slug>.md` com o título "$ARGUMENTS",
seguindo [template.md](template.md). Status inicial: "proposta".
Preencha Contexto com os requisitos de `docs/requisitos-nao-funcionais.md`
que motivam a decisão. Não marque como "aceita": isso é decisão humana.
```

A linha com `` !`...` `` é **injeção de contexto dinâmico**: o comando roda antes de o Claude ler a skill, e a saída substitui a linha. Comandos injetados nunca pedem permissão: fora do modo auto, se a checagem de permissão não resultar em "permitir", a skill é abortada. Por isso o script está pré-aprovado em `allowed-tools`.

Note também que esta skill **não** usa `disable-model-invocation`: o orquestrador `/feature` precisa chamá-la, e com esse campo o Claude Code bloquearia a chamada feita pelo Claude. O portão humano continua garantido pelo status "proposta" e pela regra `ask` em `docs/adr/**` (seção 8).

### Skills e subagentes se combinam nos dois sentidos

| Abordagem | Prompt de sistema | Tarefa | Quando usar |
| --- | --- | --- | --- |
| Skill com `context: fork` | Do tipo de agente escolhido | O conteúdo do `SKILL.md` | Procedimento autocontido que deve rodar isolado |
| Subagente com campo `skills` | O corpo do subagente | A mensagem de delegação | Especialista que precisa de um manual sempre à mão |

Cuidado: com `context: fork`, a skill precisa conter uma **tarefa** explícita. Uma skill só de diretrizes rodando em fork recebe as regras mas nenhum pedido, e volta sem resultado útil.

## 6. Slash commands: a partitura da orquestração

Um slash command é o roteiro que você aciona com uma palavra. Enquanto a delegação automática depende de o Claude **decidir** chamar um subagente, um comando torna o fluxo **explícito e repetível**: mesma sequência, mesmos critérios, mesmos pontos de parada.

### Comandos e skills agora são a mesma coisa

A documentação atual informa que os comandos personalizados foram incorporados às skills. Um arquivo em `.claude/commands/deploy.md` e uma skill em `.claude/skills/deploy/SKILL.md` criam o mesmo `/deploy` e funcionam igual. O formato antigo continua válido e aceita o mesmo frontmatter, exceto `name` e `paths`. Para algo novo, prefira a pasta de skill, que comporta templates e scripts junto.

| Formato | Caminho | Comando gerado |
| --- | --- | --- |
| Skill (recomendado) | `.claude/skills/feature/SKILL.md` | `/feature` |
| Comando (legado) | `.claude/commands/feature.md` | `/feature` |
| Comando em subpasta | `.claude/commands/backend/api.md` | `/backend:api` |

### Recursos que tornam um comando orquestrador

| Recurso | Sintaxe | Uso na orquestração |
| --- | --- | --- |
| Todos os argumentos | `$ARGUMENTS` | Descrição da feature |
| Argumento por posição | `$0`, `$1` ou `$ARGUMENTS[0]` | Módulo, prioridade |
| Argumentos nomeados | campo `arguments: [modulo, issue]` e `$modulo` | Legibilidade |
| Contexto pré-carregado | `` !`git status --short` `` | Estado real antes de começar |
| Bloco de comandos | bloco cercado aberto com ```` ```! ```` | Vários comandos de diagnóstico |
| Pré-aprovação | `allowed-tools: Bash(./mvnw *)` | Rodar testes sem pedir permissão |
| Só você aciona | `disable-model-invocation: true` | Fluxos com efeito colateral |

Um comando injetado que falha (código de saída diferente de zero) **aborta a skill inteira**. Para scripts de checagem que retornam 1 quando encontram problemas, acrescente `|| true`.

### Exemplo: `/feature`

```markdown
---
name: feature
description: Implementa uma feature com plano, TDD e revisão independente
argument-hint: <descrição da feature>
disable-model-invocation: true
allowed-tools: Bash(./mvnw *) Bash(git status *) Bash(git diff *)
---
Feature: $ARGUMENTS

Estado do repositório: !`git status --short`

1. Leia `memoria/estado.md` e `docs/escopo.md`.
2. Use o subagente `explorador` para mapear os arquivos afetados.
3. Escreva o plano em `memoria/plano-atual.md`.
   PARE e aguarde minha aprovação.
4. Use o subagente `testador` para escrever os testes da spec. Confirme que falham.
5. Implemente até os testes passarem, sem alterar os testes.
6. Use o subagente `revisor` para revisar o diff.
7. Se houve decisão arquitetural, rode /nova-adr. Atualize `estado.md`.
8. Apresente o relatório do revisor. Não faça commit.
```

### Outros comandos úteis num ecossistema de agentes

- **`/revisar`:** injeta `git diff` e chama o revisor, sem implementar nada.
- **`/nova-adr <título>`:** gera a próxima ADR a partir do template (seção 5).
- **`/handoff`:** atualiza `estado.md` e move detalhes para o histórico antes de encerrar a sessão.
- **`/auditar-seguranca <módulo>`:** roda o checklist de segurança sobre um módulo.

### Boas práticas

- Um comando, um fluxo. Se ele tem modos demais, divida.
- Pontos de parada explícitos nas decisões importantes; é ali que entra o julgamento humano.
- Referencie documentos por caminho, sem copiá-los no comando.
- Versione `.claude/` no repositório: o processo passa a fazer parte do projeto.

Um cuidado de configuração: use `disable-model-invocation: true` só nos **pontos de entrada** que você aciona, como `/feature`. Uma skill que outro orquestrador manda rodar (como `/nova-adr` ou `/handoff`) não pode ter esse campo, porque o Claude Code bloqueia a invocação feita pelo próprio Claude.

## 7. Hooks: os fiscais automáticos

Hooks são comandos que o Claude Code executa em pontos fixos do seu ciclo de vida. A documentação os define como **controle determinístico**: certas ações sempre acontecem, em vez de depender de o modelo escolher executá-las. É a ferramenta para transformar "por favor, faça X" em "X acontece".

### Eventos mais úteis para orquestração

| Evento | Quando dispara | Uso típico |
| --- | --- | --- |
| `SessionStart` | Início ou retomada de sessão (matcher `startup`, `resume`, `compact`...) | Injetar `estado.md` no contexto |
| `PreToolUse` | Antes de uma ferramenta rodar; pode bloquear | Proteger arquivos e comandos |
| `PostToolUse` | Depois de uma ferramenta rodar com sucesso | Rodar formatador, linter ou testes |
| `SubagentStart` / `SubagentStop` | Subagente começa ou termina | Preparar e limpar recursos, registrar |
| `Stop` | O Claude termina de responder | Verificar se a tarefa está completa |
| `PreCompact` / `PostCompact` | Antes e depois da compactação | Salvar e reinjetar contexto crítico |
| `InstructionsLoaded` | CLAUDE.md ou regra carregada | Depurar quais regras entraram |

### Como um hook se comunica

O hook recebe um JSON pela entrada padrão (com `tool_name`, `tool_input` etc.) e responde pelo código de saída:

| Saída | Efeito |
| --- | --- |
| Código 0 | Sem objeção. Em `SessionStart` e `UserPromptSubmit`, o texto impresso entra no contexto do Claude |
| Código 2 | Erro bloqueante, com efeito que depende do evento: em PreToolUse cancela a ferramenta e o stderr volta ao Claude; em PostToolUse a ferramenta já rodou e o stderr é mostrado ao Claude como feedback |
| JSON estruturado | Controle fino, como `permissionDecision: "deny"` com motivo |

### Onde configurar

| Local | Escopo |
| --- | --- |
| `.claude/settings.json` | Projeto, versionado |
| `.claude/settings.local.json` | Projeto, só na sua máquina |
| `~/.claude/settings.json` | Todos os seus projetos |
| Frontmatter de subagente | Só enquanto o subagente roda |
| Frontmatter de skill | Do momento em que a skill é invocada até o fim da sessão |

### Exemplo: três garantias para um ecossistema de agentes

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [
        { "type": "command",
          "command": "cat \"$CLAUDE_PROJECT_DIR\"/memoria/estado.md" }
      ]}
    ],
    "PreToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [
          { "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/proteger-adr-aceita.sh" }
      ]}
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [
          { "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && ./mvnw -q test 1>&2 || exit 2" }
      ]}
    ]
  }
}
```

1. **`SessionStart`** imprime o estado atual, que entra no contexto: toda sessão começa sabendo onde parou.
2. **`PreToolUse`** roda um script que lê `tool_input.file_path` e sai com código 2 se o alvo for uma ADR com status "aceita", obrigando a criar uma nova ADR em vez de reescrever a decisão.
3. **`PostToolUse`** roda os testes após cada edição. Se falharem, a saída vai para stderr e o comando sai com código 2; em PostToolUse, isso faz o Claude Code mostrar o erro ao Claude, que pode corrigir em seguida (a edição em si não é desfeita). Em projetos grandes, troque por um subconjunto rápido.

### Hooks que usam julgamento

Além de comandos, há hooks do tipo `prompt` (uma chamada de modelo que decide) e `agent` (um subagente com ferramentas que verifica antes de decidir; marcado como experimental). Exemplo: um hook `Stop` do tipo `agent` que roda a suíte de testes e só deixa o Claude encerrar se tudo passar.

### Hooks e permissões

Um `PreToolUse` que nega uma ação bloqueia mesmo no modo `bypassPermissions`. O contrário não vale: um hook que aprova não supera regras de negação das configurações. Para bloqueios duros, a documentação recomenda o sistema de permissões (seção 8); o filtro `if` dos hooks é "melhor esforço".

## 8. Permissões e configurações: o que cada agente pode fazer

As regras de permissão são aplicadas pelo próprio Claude Code, não pelo modelo. A documentação é direta: instruções no prompt ou no CLAUDE.md moldam o que o Claude tenta fazer, mas não mudam o que o Claude Code permite. É aqui que o "protocolo de quem escreve o quê" (seção 17) deixa de ser pedido e vira regra.

### Três tipos de regra

| Tipo | Efeito | Precedência |
| --- | --- | --- |
| `deny` | Bloqueia | Avaliada primeiro; sempre vence |
| `ask` | Pede confirmação | Avaliada em segundo |
| `allow` | Libera sem perguntar | Avaliada por último |

Uma regra `allow` não abre exceção dentro de uma `deny`. Se qualquer nível de configuração nega algo, nenhum outro nível consegue liberar.

### Sintaxe das regras

| Regra | Significado |
| --- | --- |
| `Bash(./mvnw *)` | Qualquer comando que começa com `./mvnw` |
| `Bash(git push *)` | Qualquer `git push` |
| `Edit(/docs/adr/**)` | Edição em `docs/adr/` (relativo à raiz do projeto, em configuração de projeto) |
| `Read(./.env)` | Leitura do `.env` |
| `Agent(Explore)` | O subagente Explore |
| `Agent(isolation:worktree)` | Chamadas de subagente que pedem worktree (regras por parâmetro só valem em deny e ask) |

### Onde ficam as configurações

| Arquivo | Escopo | Versionado |
| --- | --- | --- |
| `~/.claude/settings.json` | Todos os seus projetos | Não |
| `.claude/settings.json` | Projeto | Sim |
| `.claude/settings.local.json` | Projeto, só você | Não |
| Configuração gerenciada | Organização | Definida pelo administrador |

### Modos de permissão

| Modo | Comportamento |
| --- | --- |
| `default` (Manual) | Pergunta no primeiro uso de cada ferramenta |
| `plan` | Só explora e lê; não edita código-fonte |
| `acceptEdits` | Aceita edições e comandos comuns de arquivo no diretório de trabalho |
| `auto` | Um classificador em segundo plano revisa ações antes de rodarem |
| `dontAsk` | Nega tudo que pediria confirmação, exceto o pré-liberado |
| `bypassPermissions` | Pula as confirmações; use só em contêiner ou VM isolada |

### Exemplo: `.claude/settings.json` de um projeto com agentes

```json
{
  "permissions": {
    "allow": [
      "Bash(./mvnw *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Edit(/src/**)",
      "Edit(/memoria/**)"
    ],
    "ask": [
      "Edit(/docs/adr/**)",
      "Edit(/docs/contratos/**)",
      "Bash(git commit *)",
      "Edit(/src/main/resources/db/migration/**)"
    ],
    "deny": [
      "Read(./.env)",
      "Bash(git push *)"
    ]
  }
}
```

O efeito: agentes trabalham livremente no código e no estado, mas qualquer mudança em ADRs ou contratos pede sua confirmação, commits passam por você, e qualquer escrita na pasta de migrations também pede confirmação. **Inferência** (da página de permissões): uma regra deny ali bloquearia até a criação de migrations novas, porque as regras de Edit valem para todas as ferramentas que escrevem arquivos; para impedir só a edição das já existentes, some um hook PreToolUse que recusa (código 2) quando o arquivo-alvo já existe.

### Duas camadas complementares

- **Por agente:** os campos `tools` e `disallowedTools` de cada subagente (seção 4). O revisor nem recebe `Edit`.
- **Por projeto:** as regras acima valem para a conversa principal e para os subagentes.

Para restrições de rede e sistema de arquivos que não dependam do texto do comando, a documentação indica o **sandbox**: regras de Bash casam o texto escrito, e uma variação como `/bin/rm` em vez de `rm` escapa delas.

## 9. MCP e plugins: conexão externa e empacotamento

### MCP: acesso a sistemas externos

O Model Context Protocol conecta o Claude a serviços fora do repositório: banco de dados, GitHub, rastreador de issues, navegador. A documentação distingue bem os papéis: **MCP dá as ferramentas; skill ensina a usá-las**. Por exemplo, um servidor MCP conecta ao banco, e uma skill documenta o esquema e os padrões de consulta do projeto.

O custo de contexto é baixo: no início da sessão carregam só os nomes das ferramentas, e os esquemas completos ficam adiados até o uso. Servidores de projeto ficam em `.mcp.json` e podem ser versionados.

Para orquestração, o recurso mais útil é dar MCP **só a um subagente**, pelo campo `mcpServers` do frontmatter. Assim a conversa principal não carrega as ferramentas daquele servidor:

```markdown
---
name: testador-e2e
description: Testa fluxos de login no navegador real
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
---
Use as ferramentas do Playwright para executar o fluxo descrito
em `docs/specs/login.md` e reporte cada critério de aceitação.
```

### Plugins: o ecossistema como pacote

Um plugin empacota skills, subagentes, hooks e servidores MCP numa unidade instalável e versionada. Skills de plugin ganham prefixo (`/meu-plugin:revisar`), o que evita conflito entre pacotes. A documentação sugere criar um plugin quando um **segundo repositório** precisa da mesma configuração.

```text
meu-plugin/
├── .claude-plugin/
│   └── plugin.json      # manifesto
├── skills/
│   └── nova-adr/SKILL.md
├── agents/
│   └── revisor.md
├── hooks/
│   └── hooks.json
└── .mcp.json
```

Duas restrições importam: as pastas `skills/`, `agents/` e `hooks/` ficam na raiz do plugin, não dentro de `.claude-plugin/`; e, por segurança, subagentes vindos de plugin ignoram os campos `hooks`, `mcpServers` e `permissionMode`. Hooks e MCP do plugin vão em `hooks/hooks.json` e `.mcp.json`, valendo sempre que o plugin estiver ativo.

**Proposta deste guia:** para um portfólio, comece com tudo em `.claude/` do próprio repositório; empacotar como plugin faz sentido quando você reutilizar o mesmo processo em vários projetos.

## 10. Plan mode, worktrees, agent teams e paralelismo

### Plan mode: pensar antes de editar

No plan mode, o Claude lê arquivos e roda comandos somente leitura, mas **não edita código-fonte**. Quando precisa entender o código, delega a pesquisa ao subagente nativo Plan, que roda em contexto separado. É o ponto de controle mais barato do processo: corrigir um plano custa menos que corrigir código. No terminal, alterna-se de modo com Shift+Tab.

### Worktrees: isolamento de arquivos

Uma worktree Git é uma segunda cópia de trabalho do repositório, numa branch própria. Ela resolve o problema de dois agentes editando o mesmo arquivo:

- **Sessões suas em paralelo:** inicie cada uma com a flag `--worktree`.
- **Subagentes:** `isolation: worktree` no frontmatter dá ao subagente uma worktree temporária, limpa automaticamente se ele não fizer mudanças.
- **`/batch`:** skill nativa que divide uma mudança grande em 5 a 30 subagentes, cada um em sua worktree.

### As cinco formas de rodar agentes em paralelo

| Abordagem | Quem coordena | Os agentes conversam? | Quando usar |
| --- | --- | --- | --- |
| Subagentes | O Claude, dentro de uma sessão | Reportam ao agente que os criou | Tarefa lateral que inundaria a conversa |
| Agent view (`claude agents`) | Você despacha e acompanha | Só reportam a você | Várias tarefas independentes em segundo plano |
| Agent teams | Um líder que planeja, distribui e supervisiona | Sim: mensagens diretas e lista de tarefas compartilhada | Projeto dividido em partes que precisam ficar sincronizadas |
| Dynamic workflows | Um script escrito pelo Claude | Resultados verificados entre si | Auditoria do código inteiro, migração de centenas de arquivos |
| Projects (nuvem) | O Claude, em várias sessões na nuvem | Compartilham instruções e memória | Trabalho de dias ou semanas |

A documentação marca agent view como prévia de pesquisa e **agent teams como experimental e desativado por padrão**. **Proposta deste guia:** para um projeto de portfólio, subagentes com worktrees cobrem quase tudo.

### Três perguntas para escolher

1. **Quem coordena?** O Claude turno a turno (subagentes), você (agent view), um líder (agent teams) ou um script (workflows).
2. **Os trabalhadores precisam se falar?** Subagentes só devolvem resultado a quem os criou; teammates de um agent team trocam mensagens entre si.
3. **Mexem nos mesmos arquivos?** Isole com worktrees. Atenção: agent teams **não** isolam teammates em worktrees, então divida o trabalho para que cada teammate seja dono de um conjunto diferente de arquivos.

### Acompanhando o que está rodando

| Comando | Mostra |
| --- | --- |
| `/tasks` | Tudo que roda em segundo plano na sessão, inclusive subagentes |
| `claude agents` | Agent view: todas as sessões em segundo plano |
| `/workflows` | Execuções de dynamic workflows e a fase de cada uma |

Rodar vários agentes ao mesmo tempo multiplica o consumo de tokens. Paralelize quando as tarefas forem de fato independentes.

## 11. Padrões de workflow de agentes

O guia de boas práticas do Claude Code parte de uma restrição: o contexto enche rápido e o desempenho cai à medida que enche. Os padrões abaixo existem para economizar contexto e para dar ao agente **um sinal objetivo de que acertou**. Sem uma checagem que ele possa rodar, "parece pronto" é o único sinal disponível, e você vira o laço de verificação.

### Padrão 1: Explorar → Planejar → Implementar → Commitar

É o fluxo recomendado pela documentação, em quatro fases:

1. **Explorar** em plan mode: o Claude lê arquivos e responde perguntas sem mudar nada.
2. **Planejar:** pedir um plano detalhado; `Ctrl+G` abre o plano no editor para você ajustar.
3. **Implementar:** sair do plan mode e codificar verificando contra o plano, com testes.
4. **Commitar:** mensagem descritiva e, se for o caso, PR.

A documentação avisa que planejar tem custo: para mudanças que cabem numa frase, pule o plano.

### Padrão 2: Entrevista e spec antes do código

Para features maiores, peça que o Claude **entreviste você** (com a ferramenta `AskUserQuestion`) sobre implementação, casos de borda e trade-offs, e escreva uma spec completa. Depois, comece uma sessão nova para executá-la, com contexto limpo. Segundo a documentação, as specs mais úteis nomeiam arquivos e interfaces, dizem o que está fora do escopo e terminam com uma verificação de ponta a ponta.

### Padrão 3: TDD guiado por agente

1. Um agente escreve os testes a partir da spec, sabendo que a implementação ainda não existe.
2. Você confirma que falham pelo motivo certo e faz commit dos testes.
3. Outro agente (ou outra sessão) implementa até passarem, **sem alterar os testes**.

A documentação sugere exatamente isso: um Claude escreve os testes, outro escreve o código que os satisfaz.

### Padrão 4: Escritor e revisor em contextos separados

| Sessão A (escritor) | Sessão B (revisor) |
| --- | --- |
| Implementa o rate limiter |  |
|  | Revisa o diff procurando casos de borda e inconsistências |
| Corrige com base no relatório de B |  |

O contexto limpo é o essencial: um revisor que viu o raciocínio do escritor tende a concordar com ele. Dentro de uma sessão, o mesmo efeito vem de um subagente revisor, ou da skill nativa `/code-review`. Um cuidado registrado na documentação: um revisor instruído a achar problemas quase sempre acha algum; peça que aponte só o que afeta corretude ou requisitos, para não cair em superengenharia.

### Padrão 5: Orquestrador e trabalhadores

Um agente principal divide a tarefa e delega a subagentes especializados, cada um em contexto próprio, recebendo só resumos. É o que a documentação chama de usar subagentes para investigação: "use subagentes para investigar X" mantém a conversa principal limpa para a implementação.

### Padrão 6: Laço avaliador–otimizador

Gerar, avaliar, refinar, repetir até o critério ser atingido. O Claude Code oferece quatro formas de impor o critério, da mais leve à mais rígida:

| Forma | Como funciona |
| --- | --- |
| No prompt | "Rode os testes e itere até passarem" |
| `/goal` | Um avaliador separado reconfere a condição a cada turno |
| Hook `Stop` | Um script bloqueia o fim do turno até a checagem passar |
| Segunda opinião | Um subagente ou dynamic workflow tenta refutar o resultado |

### Padrão 7: Paralelo com worktrees

Tarefas independentes rodam em sessões ou subagentes isolados em worktrees (seção 10). Também serve para gerar duas soluções do mesmo problema e escolher a melhor.

### Falhas comuns segundo a documentação

| Falha | Correção |
| --- | --- |
| Sessão "pia de cozinha", com tarefas misturadas | `/clear` entre tarefas não relacionadas |
| Corrigir o mesmo erro várias vezes | Depois de duas correções, `/clear` e um prompt melhor |
| CLAUDE.md inchado | Podar; converter regras importantes em hooks |
| Implementação plausível sem casos de borda | Sempre dar uma forma de verificação |
| Exploração infinita | Delimitar ou delegar a subagentes |

## 12. ADRs: a memória das decisões

Uma ADR (Architecture Decision Record) registra **uma** decisão arquitetural: o contexto que a motivou, a escolha feita e suas consequências. O formato foi popularizado por Michael Nygard em 2011 e é deliberadamente curto. Para agentes, ADRs resolvem um problema específico: sem elas, cada sessão "redescobre" decisões já tomadas e pode desfazê-las sem saber.

### Regras que fazem ADRs funcionarem com agentes

- **Imutáveis depois de aceitas.** Mudou de ideia? Crie uma ADR nova que **substitui** a anterior, e marque a antiga como "substituída por 00NN". O histórico do raciocínio fica preservado.
- **Status explícito.** Um agente que lê uma ADR substituída como vigente toma decisões erradas. Instrua no CLAUDE.md: "vale só status aceita".
- **Numeradas e com data.** `0001-...`, `0002-...` dão ordem e permitem referência curta em commits.
- **Agente propõe, humano aceita.** Agentes podem criar ADRs com status "proposta"; mudar para "aceita" é decisão sua (a regra `ask` em `docs/adr/**` da seção 8 garante a confirmação).

### Ciclo de vida

| Status | Significado | Quem define |
| --- | --- | --- |
| Proposta | Decisão em discussão | Agente ou você |
| Aceita | Vigente; agentes devem seguir | Você |
| Rejeitada | Considerada e descartada (vale registrar por quê) | Você |
| Substituída | Trocada por outra ADR, que é citada | Você |

### Template

```markdown
# 0002 — Tokens JWT assinados com RS256

- Status: aceita (substitui 0001)
- Data: 2026-10-14
- Requisitos relacionados: RNF-03 (validação distribuída)

## Contexto
Outros serviços precisam validar tokens sem compartilhar segredo.

## Opções consideradas
1. HS256 com segredo compartilhado
2. RS256 com chave pública via JWKS

## Decisão
RS256; a chave pública é exposta no endpoint JWKS.

## Consequências
+ Validação distribuída sem segredo compartilhado.
− Exige rotação de chaves (ver `docs/runbooks/rotacao-chaves.md`).

## Verificação
Teste `JwtSigningTest` garante que tokens HS256 são rejeitados.
```

A seção **Verificação** é o elo com a seção 15: sempre que possível, a decisão é acompanhada de um teste que quebra se alguém a violar.

### Como agentes usam ADRs

| Momento | Agente | Uso |
| --- | --- | --- |
| Planejamento | Planejador | Lê ADRs aceitas antes de propor mudanças |
| Implementação | Implementador | Segue as decisões; não as rediscute |
| Revisão | Revisor | Confere o diff contra as ADRs aceitas |
| Decisão nova | Qualquer um | Propõe ADR via `/nova-adr`; você aceita ou rejeita |
| Commit | Implementador | Cita a ADR na mensagem: `feat(token): RS256 (ADR-0002)` |

Para você, há um ganho a mais: cada ADR registra o porquê de uma escolha técnica. Ler as ADRs que os agentes propuseram é uma forma direta de aprender a justificar decisões que você ainda não domina.

## 13. Escopo, specs, requisitos não funcionais e questões em aberto

As ADRs dizem **por que** algo foi feito. Estes quatro documentos dizem **o que** fazer, **o que não fazer**, **quão bem** e **o que ainda não se sabe**. Juntos, formam o contrato que os agentes executam.

### Escopo e não-objetivos (`docs/escopo.md`)

Agentes tendem a construir demais: cache, filas e abstrações "para o futuro". Os não-objetivos são o freio. A própria documentação do Claude Code lista "o que está fora do escopo" entre os elementos de uma boa spec.

```markdown
# Escopo
## Objetivo
IdP OIDC para a plataforma X: login e emissão de tokens.
## Não-objetivos (nesta versão)
- Federação com provedores externos (Google etc.)
- Painel administrativo
- Multi-tenancy
```

### Specs com critérios de aceitação (`docs/specs/`)

Uma spec por feature, em linguagem verificável. O formato "dado / quando / então" vira teste quase diretamente, e é o tipo de documento que quem especifica sabe defender.

```markdown
# Spec: endpoint /token (authorization code + PKCE)
## Critérios de aceitação
- CA1: dado um code válido e code_verifier correto, quando POST /token,
  então retorna 200 com access_token RS256 e expires_in = 900.
- CA2: dado code_verifier incorreto, então retorna 400 invalid_grant.
- CA3: dado code já usado, então retorna 400 e revoga tokens emitidos com ele.
## Fora do escopo
- Refresh token (ver Q3 em questoes-em-aberto.md)
## Verificação de ponta a ponta
- Teste de integração `TokenEndpointIT` cobre CA1 a CA3.
```

### Requisitos não funcionais (`docs/requisitos-nao-funcionais.md`)

As specs dizem o que o sistema faz; os RNFs dizem **quão bem**. Sem eles, o agente não tem critério para escolher entre uma solução simples e uma robusta. Muitos RNFs são o motivo de ADRs.

| ID | Requisito | Como se verifica |
| --- | --- | --- |
| RNF-01 | Nenhum dado sensível em log | Teste que captura logs e procura padrões proibidos |
| RNF-02 | Serviço sobe com uma única variável de ambiente obrigatória | Teste de inicialização |
| RNF-03 | Tokens validáveis por outros serviços sem segredo compartilhado | ADR-0002 + teste |

### Questões em aberto (`docs/questoes-em-aberto.md`)

O registro do que **ainda não foi decidido**. Sem ele, o agente decide sozinho e em silêncio; com ele, sabe que deve parar e perguntar. Quando uma questão é resolvida, vira ADR e sai da lista.

```markdown
# Questões em aberto
- Q3: tempo de vida do refresh token? (bloqueia spec refresh.md)
- Q4: sessões em Redis ou no banco? (candidata a ADR)
```

### O ciclo de uma decisão

| Etapa | Documento |
| --- | --- |
| Dúvida surge | Questões em aberto |
| Opções avaliadas, uma escolhida | ADR (proposta → aceita) |
| Comportamento definido | Spec com critérios de aceitação |
| Qualidade exigida | Requisitos não funcionais |
| Garantia automática | Teste ou regra executável (seção 15) |

## 14. Convenções, testes, definição de pronto e documentos de apoio

Estes documentos respondem "como fazemos aqui?" e "quando está pronto?". São os que mais reduzem retrabalho, porque cada um elimina uma classe inteira de decisões que o agente tomaria de forma aleatória.

### Definição de pronto (`docs/definicao-de-pronto.md`)

O checklist que vale para toda tarefa e funciona como critério de parada. Sem ele, o agente para quando "parece pronto".

```markdown
# Definição de pronto
- [ ] Critérios de aceitação da spec cobertos por testes
- [ ] `./mvnw verify` passando (testes, ArchUnit, lint)
- [ ] Nenhuma violação de `docs/seguranca.md`
- [ ] Revisor sem itens Críticos
- [ ] ADR proposta se houve decisão arquitetural
- [ ] `estado.md` atualizado
```

### Estratégia de testes (`docs/estrategia-de-testes.md`)

Diz o que se testa em cada nível. Sem ela, um agente escreve quarenta testes unitários triviais e nenhum de integração, ou o contrário.

| Nível | O que cobre | Ferramenta típica (Java/Spring) |
| --- | --- | --- |
| Unitário | Regras de domínio puras | JUnit 5 |
| Integração | Banco, segurança, endpoints | Spring Boot Test + Testcontainers |
| Contrato | Fronteiras entre serviços | Validação do OpenAPI, testes de contrato |
| Arquitetura | Dependências entre camadas | ArchUnit |
| Não se testa | Getters, setters, código gerado | — |

### Convenções (`docs/convencoes.md` ou `.claude/rules/`)

Estrutura de pacotes, nomes, tratamento de erros, formato de log. Regras que valem só para parte do código vão em `.claude/rules/` com `paths` (seção 3), para carregar só quando relevantes. A documentação recomenda incluir apenas o que **difere** do padrão da linguagem; o que o Claude já faz certo sem instrução é ruído.

### Glossário (`docs/glossario.md`)

Define os termos do domínio e evita nomes inconsistentes entre classes, rotas e tabelas.

| Termo | Significado | Não confundir com |
| --- | --- | --- |
| Usuário | Pessoa que se autentica | Cliente (aplicação OIDC) |
| Cliente | Aplicação registrada que pede tokens | Usuário |
| Sessão | Login ativo no IdP | Token (credencial emitida) |

### Armadilhas conhecidas (`docs/armadilhas.md`)

O que já deu errado e por quê: "o container do Postgres precisa subir antes dos testes de integração", "a chave de teste fica em `src/test/resources`". A documentação do Claude Code inclui "pegadinhas comuns ou comportamentos não óbvios" entre o que vale registrar. Qualquer agente pode acrescentar itens; é o arquivo que mais economiza retrabalho.

### Visão geral e modelo de dados (`docs/visao-geral.md`, `docs/modelo-dados.md`)

Uma página com os módulos, como se comunicam e onde fica cada coisa; o primeiro arquivo que um agente novo deve ler. O modelo de dados pode ir num diagrama Mermaid. Atenção ao conselho da documentação: o `/doctor` corta do CLAUDE.md o que o Claude pode derivar do código, como listas de diretórios. Por isso a visão geral fica em `docs/`, explicando **relações e motivos**, não listando arquivos.

### Runbooks (`docs/runbooks/`)

Como rodar, testar, fazer deploy e rotacionar chaves, passo a passo. Procedimentos repetidos são bons candidatos a virar skill de tarefa (seção 5).

### README e changelog

O README é a porta de entrada humana: o que é, como rodar em poucos comandos, onde está a documentação. Para um portfólio, é o primeiro arquivo que um recrutador abre. O changelog registra o que mudou por versão; commits no padrão Conventional Commits (`feat:`, `fix:`) permitem gerá-lo automaticamente.

## 15. Regras executáveis: documentação que se verifica sozinha

Uma ADR é texto e pode ser ignorada; uma regra executável **quebra o build**. Este é o elemento mais poderoso de todo o ecossistema, porque documentação que se verifica sozinha não envelhece. O princípio: sempre que uma regra puder virar teste, transforme-a, e deixe o texto só para explicar o porquê.

Ele também é a resposta à recomendação central da documentação do Claude Code: dar ao agente uma checagem que ele possa rodar. Testes de arquitetura transformam decisões em checagens.

### ArchUnit: ADRs que viram testes (Java)

O ArchUnit é uma biblioteca que testa a estrutura do código Java: quem depende de quem, onde ficam as anotações, convenções de nome.

```java
@AnalyzeClasses(packages = "br.com.exemplo.idp")
class ArquiteturaTest {

    // ADR-0003: o domínio não conhece a infraestrutura
    @ArchTest
    static final ArchRule dominioIndependente =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

    // Convenção: controllers só na camada web
    @ArchTest
    static final ArchRule controllersNaWeb =
        classes().that().areAnnotatedWith(RestController.class)
            .should().resideInAPackage("..web..");
}
```

Se um agente (ou você) violar a ADR-0003, o teste falha, o hook `PostToolUse` da seção 7 mostra a falha ao agente, e ele corrige antes de você ver o código.

### Mapa de decisões para verificações

| Decisão documentada | Verificação executável |
| --- | --- |
| Camadas e dependências | ArchUnit |
| Contrato de API | Validação do `openapi.yaml`; testes de contrato |
| Esquema do banco | Migrations versionadas (Flyway ou Liquibase) |
| Estilo de código | Linter e formatador no CI |
| Dependências proibidas | Regras de build (ex.: Maven Enforcer) |
| Segurança | Análise estática e scanner de dependências no CI |
| Nenhum dado sensível em log (RNF-01) | Teste que captura a saída de log e procura padrões proibidos |

### Migrations: histórico executável do modelo de dados

Cada mudança de esquema é um arquivo novo e numerado (`V1__cria_usuario.sql`, `V2__adiciona_mfa.sql`). Migrations já aplicadas **nunca** são editadas, só sucedidas por novas. A regra `ask` da seção 8 faz toda escrita na pasta passar por você, e um hook PreToolUse pode recusar de vez a edição de arquivos que já existem.

### CI: a última linha de defesa

O pipeline de integração contínua roda tudo isso a cada push. Mesmo que um hook seja desativado ou uma sessão rode sem as configurações do projeto, o CI garante que nada fora das regras chega à branch principal.

### Três níveis de garantia, do mais fraco ao mais forte

| Nível | Exemplo | Pode ser ignorado? |
| --- | --- | --- |
| Instrução | "O domínio não depende da infraestrutura" no CLAUDE.md | Sim, é um pedido |
| Hook ou permissão | `PostToolUse` roda os testes; `ask` em migrations | Não, na sessão configurada |
| Teste no build e no CI | ArchUnit falha o `./mvnw verify` | Não, em nenhum ambiente |

## 16. Arquivos de contexto voláteis: onde estamos

Cada sessão do Claude Code começa com contexto vazio, e cada subagente nasce sem ver a conversa. Os arquivos voláteis são a memória de trabalho compartilhada: respondem "onde paramos?" para quem chega agora. São voláteis porque mudam a cada sessão, ao contrário das ADRs e specs.

**Por que fora de `.claude/`.** A documentação de modos de permissão trata `.claude` como caminho protegido: fora do modo `bypassPermissions`, escritas ali nunca são aprovadas automaticamente, nem por regra `allow`. **Inferência** (da mesma documentação): como o estado muda a cada etapa, guardá-lo em `.claude/` faria cada atualização pedir confirmação, e num laço com `dontAsk` a escrita seria negada. Por isso, como **proposta deste guia**, ele mora em `memoria/`, na raiz do repositório.

### Os quatro arquivos de `memoria/`

| Arquivo | Conteúdo | Tamanho alvo | Quem escreve |
| --- | --- | --- | --- |
| `estado.md` | Objetivo atual, feito, próximo passo, bloqueios | Uma tela | Orquestrador |
| `plano-atual.md` | Plano aprovado da tarefa em curso, com etapas marcáveis | Uma ou duas telas | Planejador; você aprova |
| `pendencias.md` | Débitos e tarefas adiadas, cada uma com motivo | Curto | Qualquer agente acrescenta |
| `historico/AAAA-MM-DD.md` | Resumo de sessões encerradas | Livre, mas nunca carregado inteiro | Comando `/handoff` |

### `estado.md`: curto e sempre atual

```markdown
# Estado — atualizado 2026-10-14
## Objetivo atual
Endpoint /token com authorization code + PKCE (spec token.md).
## Feito
- Testes de integração CA1–CA3 escritos (falhando, esperado)
## Próximo passo
Implementar validação do code_verifier.
## Bloqueios
Q3 (tempo de vida do refresh token) — fora do escopo desta tarefa.
```

### `plano-atual.md`: o plano como lista de tarefas

```markdown
# Plano: /token com PKCE (aprovado em 2026-10-14)
- [x] 1. Explorar TokenService e AuthorizationCodeRepository
- [x] 2. Testes CA1–CA3 (testador)
- [ ] 3. Validar code_verifier (S256)
- [ ] 4. Revogar tokens em reuso de code (CA3)
- [ ] 5. Revisão (revisor) e atualização do estado
```

### Regras para não se perder

- **O presente fica curto.** `estado.md` cabe numa tela; o passado vai para `historico/`. Assim o contexto não incha com o que já terminou.
- **Rotação explícita.** Um comando `/handoff` ao fim da sessão move detalhes para o histórico e reescreve o estado.
- **Injeção garantida.** O hook `SessionStart` da seção 7 imprime `estado.md`, e toda sessão começa sabendo onde parou, inclusive após compactação (matcher `compact`).
- **Fatos, não narrativa.** "Testes CA1–CA3 escritos" é melhor que "passei a tarde nos testes".
- **Datas sempre.** Um estado sem data não diz se está atualizado.

### Diferença para as memórias nativas do Claude Code

| Mecanismo | Quem escreve | Onde fica | Compartilhado pelo Git |
| --- | --- | --- | --- |
| `memoria/` (esta seção) | Seus agentes, por protocolo | No repositório | Sim |
| Auto memory | O Claude, por iniciativa | `~/.claude/projects/<projeto>/memory/` | Não, é local da máquina |
| Memória de subagente (`memory: project`) | O próprio subagente | `.claude/agent-memory/<nome>/` | Sim |

Os três convivem. A memória de subagente é útil para aprendizado de longo prazo de um especialista (o revisor anotando padrões recorrentes); `memoria/` é o estado da tarefa em curso, explícito e auditável.

## 17. Estrutura de pastas e protocolo de propriedade

O critério de separação: **`docs/` contém o que um humano novo no projeto também precisaria ler**; **`.claude/` contém a configuração dos agentes, e memoria/ guarda o estado de trabalho deles**. Assim a documentação continua útil para colegas e recrutadores, e o estado dos agentes não polui o repositório "oficial".

### Estrutura completa

```text
projeto/
├── CLAUDE.md                     # constituição + mapa (menos de 200 linhas)
├── README.md
├── docs/                         # conhecimento (humanos e agentes)
│   ├── escopo.md                 # objetivo e não-objetivos
│   ├── roadmap.md                # marcos, itens, dependências, status
│   ├── visao-geral.md
│   ├── glossario.md
│   ├── convencoes.md
│   ├── seguranca.md
│   ├── requisitos-nao-funcionais.md
│   ├── estrategia-de-testes.md
│   ├── definicao-de-pronto.md
│   ├── questoes-em-aberto.md
│   ├── armadilhas.md
│   ├── modelo-dados.md
│   ├── adr/
│   │   ├── 0001-usar-spring-security.md
│   │   └── 0002-jwt-rs256.md
│   ├── specs/
│   │   └── token.md
│   ├── contratos/
│   │   └── openapi.yaml
│   └── runbooks/
│       └── deploy.md
├── src/
│   ├── main/resources/db/migration/   # migrations versionadas
│   └── test/java/.../ArquiteturaTest.java
├── memoria/                      # estado volátil (fora de .claude/, ver seção 16)
│   ├── estado.md
│   ├── plano-atual.md
│   ├── pendencias.md
│   └── historico/
└── .claude/
    ├── settings.json             # permissões e hooks (versionado)
    ├── settings.local.json       # ajustes pessoais (não versionado)
    ├── rules/
    │   └── seguranca.md          # com paths: só carrega no código de segurança
    ├── agents/
    │   ├── explorador.md
    │   ├── testador.md
    │   └── revisor.md
    ├── skills/
    │   ├── feature/SKILL.md      # orquestrador /feature
    │   ├── nova-adr/             # SKILL.md + template.md + scripts/
    │   └── handoff/SKILL.md
    └── hooks/
        └── proteger-adr-aceita.sh
```

### Protocolo: quem escreve o quê

Muita confusão vem de vários agentes editando os mesmos arquivos. Defina donos e, sempre que possível, **imponha** com ferramentas e permissões em vez de só pedir.

| Arquivo | Quem escreve | Quem só lê | Como se impõe |
| --- | --- | --- | --- |
| `CLAUDE.md`, `convencoes.md` | Você | Todos | Regra `ask` em edição |
| ADRs | Agentes propõem; você aceita | Todos | `ask` em `docs/adr/**`; hook bloqueia ADR aceita |
| Specs, escopo | Você, com ajuda | Testador, implementador | `ask` em `docs/specs/**` |
| Contratos | Só via ADR | Todos | `ask` em `docs/contratos/**` |
| Testes | Testador | Implementador | Instrução + revisão; o revisor reprova teste alterado |
| Código-fonte | Implementador | Revisor, explorador | `tools` sem `Edit` no revisor e no explorador |
| `estado.md`, `plano-atual.md` | Orquestrador | Subagentes | Instrução no prompt dos subagentes |
| `armadilhas.md`, `pendencias.md` | Qualquer agente acrescenta | Todos | Instrução: só acrescentar, nunca apagar |
| Migrations existentes | Ninguém | Todos | `ask` na pasta + hook que recusa arquivo existente |

### O Git também é memória

- **Commits pequenos e descritivos** permitem reconstruir a história com `git log`; os subagentes recebem um retrato do `git status` ao nascer.
- **Referências cruzadas** na mensagem ligam o código ao porquê: `feat(token): valida PKCE (spec token.md, ADR-0002)`.
- **Branches por feature** isolam experimentos; worktrees permitem trabalhar em várias ao mesmo tempo.

### Sete regras práticas

1. Separe constituição, conhecimento e estado.
2. O CLAUDE.md é um mapa, não uma enciclopédia.
3. Todo documento de decisão tem status e data.
4. O estado atual cabe numa tela; o passado vai para o histórico.
5. Cada arquivo tem um dono definido.
6. Hooks, permissões e testes impõem a disciplina que instruções só pedem.
7. Uma informação mora num lugar só; os outros apontam para ela.

## 18. Vários agentes, uma tarefa: exemplo passo a passo

Tarefa: implementar o endpoint `/token` com PKCE no IdP, conforme `docs/specs/token.md`. Três especialistas trabalham sob a conversa principal, que atua como **orquestradora**. Cada um tem uma responsabilidade, ferramentas mínimas e um critério de saída claro.

### O elenco

| Agente | Ferramentas | Modelo | Responsabilidade | Critério de saída |
| --- | --- | --- | --- | --- |
| Orquestrador (conversa principal) | Todas | Sessão | Coordena, implementa, atualiza estado | Definição de pronto cumprida |
| `explorador` | Read, Grep, Glob | `haiku` | Mapear arquivos afetados | Resumo de até 15 linhas com caminhos |
| `testador` | Read, Grep, Glob, Edit, Write, Bash | `inherit` | Escrever testes a partir da spec | Testes compilam e falham pelo motivo certo |
| `revisor` | Read, Grep, Glob, Bash | `inherit` | Revisar diff contra ADRs e segurança | Relatório Crítico / Aviso / Sugestão |

### Definições resumidas

```markdown
---
name: explorador
description: Mapeia arquivos e dependências relevantes para uma tarefa. Somente leitura.
tools: Read, Grep, Glob
model: haiku
---
Leia `docs/visao-geral.md` primeiro. Devolva no máximo 15 linhas:
arquivos a alterar, classes envolvidas e riscos. Não proponha código.
```

```markdown
---
name: testador
description: Escreve testes a partir de critérios de aceitação de uma spec.
tools: Read, Grep, Glob, Edit, Write, Bash
---
Leia a spec indicada e `docs/estrategia-de-testes.md`.
Escreva um teste por critério de aceitação, citando o ID (CA1, CA2...).
Edite apenas arquivos em `src/test/`. Rode os testes e confirme que
falham porque a funcionalidade não existe, não por erro de compilação.
```

### A execução, passo a passo

&#91;embedded content: fluxo da tarefa · 4 agentes, 2 portões humanos, 1 laço de revisão\]

Os dois quadros destacados são os únicos pontos em que o fluxo espera por você; o laço entre revisor e orquestrador repete até não restar item Crítico.

| # | Quem | Lê | Escreve | Portão |
| --- | --- | --- | --- | --- |
| 1 | Hook `SessionStart` | `estado.md` | Contexto inicial | Automático |
| 2 | Orquestrador | `escopo.md`, `specs/token.md` | — | — |
| 3 | `explorador` | `visao-geral.md`, código | Resumo para o orquestrador | — |
| 4 | Orquestrador | Resumo, ADRs aceitas | `plano-atual.md` | **Você aprova o plano** |
| 5 | `testador` | Spec, estratégia de testes | Testes em `src/test/` | Testes falham pelo motivo certo |
| 6 | Orquestrador | Plano, testes | Código em `src/main/` | Hook roda testes a cada edição |
| 7 | Orquestrador | Saída dos testes | Correções | Todos verdes, inclusive ArchUnit |
| 8 | `revisor` | `git diff`, ADRs, `seguranca.md` | Relatório | Nenhum item Crítico |
| 9 | Orquestrador | Relatório | Ajustes; ADR proposta se houve decisão nova | Definição de pronto |
| 10 | Orquestrador | — | `estado.md`, `plano-atual.md` | **Você faz o commit** |

Se o revisor aponta um item Crítico no passo 8, o orquestrador volta ao passo 6 e chama o revisor de novo. É o laço escritor–revisor da seção 11, com o revisor em contexto limpo.

### Por que isso funciona

- **Contexto isolado onde convém:** a exploração (muitos arquivos lidos) e a revisão (julgamento independente) acontecem fora da conversa principal, que recebe só resumos.
- **Verificação objetiva em cada portão:** testes falhando no passo 5, testes passando no 7, revisor no 8. Nenhuma etapa depende de "parece pronto".
- **Arquivos como meio de passagem:** a spec liga você ao testador; o plano liga o orquestrador às etapas; o estado liga esta sessão à próxima.
- **Dois pontos humanos, nos lugares certos:** aprovar o plano (barato de mudar) e fazer o commit (o que fica).

## 19. Orquestração completa: tudo junto

A seção 18 mostrou uma tarefa. Esta mostra o **ciclo inteiro**: como os arquivos de referência alimentam os agentes, como os arquivos de contexto passam o estado entre sessões e como a própria orquestração **produz documentação** (ADRs, armadilhas, pendências, histórico) à medida que o código evolui.

&#91;embedded content: arquitetura da orquestração · referência, execução, produção e contexto\]

A orquestração lê a referência e gera produção; o contexto liga uma sessão à seguinte; e só o seu aceite move uma ADR proposta para o lado da referência.

### Três tipos de arquivo, três papéis

| Tipo | Exemplos | Papel na orquestração | Muda quando |
| --- | --- | --- | --- |
| Referência | CLAUDE.md, ADRs aceitas, specs, RNFs, convenções, glossário | Entrada: o que os agentes consultam para decidir | Há uma decisão |
| Contexto | `estado.md`, `plano-atual.md`, `pendencias.md` | Passagem: liga etapas e sessões | A cada etapa |
| Produção | ADRs propostas, `armadilhas.md`, `historico/`, changelog | Saída: o que a orquestração deixa registrado | Ao fim de etapas e sessões |

### O ciclo de uma sessão

1. **Abertura (automática).** O hook `SessionStart` injeta `estado.md`. O CLAUDE.md carrega com as regras e o mapa.
2. **Disparo.** Você digita `/feature <descrição>` (ou `/feature` sem argumento para continuar o plano atual).
3. **Planejamento.** O explorador mapeia o código; o orquestrador lê escopo, spec, RNFs e ADRs aceitas, e escreve `plano-atual.md`. Se encontrar dúvida sem resposta, registra em `questoes-em-aberto.md` e para.
4. **Aprovação humana** do plano.
5. **Testes primeiro.** O testador transforma critérios de aceitação em testes.
6. **Implementação com verificação contínua.** Hook `PostToolUse` roda testes; ArchUnit garante as ADRs.
7. **Revisão independente.** O revisor confere diff contra ADRs e `seguranca.md`, consultando sua memória de padrões recorrentes.
8. **Produção de documentação** (ver abaixo).
9. **Fechamento.** `/handoff` atualiza `estado.md`, move detalhes para `historico/`, e você faz o commit.

### Como a orquestração produz documentação

| Gatilho durante o trabalho | Documento produzido | Quem produz | Status inicial |
| --- | --- | --- | --- |
| Escolha entre alternativas técnicas | ADR via `/nova-adr` | Orquestrador | Proposta (você aceita) |
| Dúvida que a spec não responde | Item em `questoes-em-aberto.md` | Qualquer agente | Aberta |
| Questão resolvida por você | ADR; item removido da lista | Orquestrador | Proposta |
| Problema de ambiente contornado | Item em `armadilhas.md` | Qualquer agente | — |
| Débito ou tarefa adiada | Item em `pendencias.md` | Qualquer agente | — |
| Padrão recorrente na revisão | Nota na memória do revisor | Revisor | — |
| Fim de sessão | `historico/AAAA-MM-DD.md` | `/handoff` | — |
| Feature concluída | Entrada no changelog (via commits) | Você, no commit | — |

### O orquestrador completo: `.claude/skills/feature/SKILL.md`

```markdown
---
name: feature
description: Implementa uma feature com plano aprovado, TDD, revisão e registro de decisões
argument-hint: <descrição da feature ou vazio para continuar>
disable-model-invocation: true
allowed-tools: Bash(./mvnw *) Bash(git status *) Bash(git diff *) Bash(git log *)
---
Pedido: $ARGUMENTS
Commits recentes: !`git log --oneline -5`
Arquivos alterados: !`git status --short`

## Antes de tudo
- Se o pedido estiver vazio, continue `memoria/plano-atual.md`.
- Confira `docs/escopo.md`. Se o pedido cair em não-objetivo, PARE e avise.

## Etapas
1. Use o subagente `explorador` para mapear o código afetado.
2. Leia a spec em `docs/specs/`, os RNFs e as ADRs com status "aceita".
   Dúvida sem resposta: registre em `docs/questoes-em-aberto.md` e PARE.
3. Escreva o plano em `memoria/plano-atual.md` como lista de tarefas.
   PARE e aguarde aprovação.
4. Use o subagente `testador` com a spec. Confirme falhas pelo motivo certo.
5. Implemente até `./mvnw verify` passar. Não altere testes.
6. Use o subagente `revisor`. Item Crítico: corrija e revise de novo.

## Registro
- Escolheu entre alternativas técnicas? Rode /nova-adr com o título da decisão.
- Contornou problema de ambiente? Acrescente em `docs/armadilhas.md`.
- Adiou algo? Acrescente em `memoria/pendencias.md` com o motivo.

## Fechamento
- Confira `docs/definicao-de-pronto.md` item a item, com evidência.
- Rode /handoff. Apresente: testes, relatório do revisor, ADRs propostas.
- Não faça commit.
```

### O que garante cada parte

| Garantia | Mecanismo | Seção |
| --- | --- | --- |
| Toda sessão sabe onde parou | Hook `SessionStart` + `estado.md` | 7, 16 |
| Agentes não constroem demais | `escopo.md` com não-objetivos | 13 |
| Decisões não são desfeitas em silêncio | ADRs aceitas + ArchUnit + hook que protege ADR aceita | 12, 15, 7 |
| Código satisfaz a spec | Testes escritos antes, por outro agente | 11, 18 |
| Revisão sem viés | Subagente revisor em contexto limpo, somente leitura | 4, 11 |
| Ações sensíveis passam por você | Regras `ask` e `deny`; `disable-model-invocation` | 8, 5 |
| Nada fora das regras chega à branch principal | CI rodando o build completo | 15 |
| O porquê fica registrado | `/nova-adr`, `armadilhas.md`, histórico | 12, 14, 16 |

## 20. Roadmaps: implementar em várias rodadas

Quando a aplicação não cabe numa rodada de `/feature`, o **roadmap** é o documento que mantém a coerência entre rodadas: diz o que vem a seguir, em que ordem, por quê, e quando um conjunto de entregas está pronto. Cada rodada começa com contexto vazio; o roadmap é o que impede que a rodada 37 trabalhe às cegas em relação às 36 anteriores.

### Roadmap não é lista de tarefas

| Aspecto | Lista de tarefas | Roadmap para agentes |
| --- | --- | --- |
| Unidade | Qualquer coisa a fazer | Item que cabe numa rodada e termina verificável |
| Ordem | Implícita ou nenhuma | Dependências explícitas entre itens |
| Agrupamento | Nenhum | Marcos com critério de saída |
| Rastreabilidade | Texto solto | Cada item aponta para spec e ADRs |
| Estado | Riscado à mão | Coluna de status atualizada pelo `/handoff` |

### Sete princípios

1. **Rodada zero primeiro.** Antes de qualquer feature, um esqueleto que compila, testa e roda o CI (o chamado *walking skeleton*), com ADRs fundacionais, contratos, testes de arquitetura e a pasta `.claude/`. Tudo o que vem depois só acrescenta, e as regras executáveis protegem a fundação.
2. **Fatias verticais, não camadas.** Um item atravessa todas as camadas e termina funcionando de ponta a ponta. Fatias horizontais geram rodadas que não podem ser verificadas.
3. **Itens do tamanho de uma rodada.** Heurística: uma spec, critérios de aceitação que cabem numa revisão atenta, descrição numa frase. Se o plano de uma rodada não cabe numa tela, divida o item.
4. **Dependências explícitas e contratos cedo.** Cada item declara do que depende. Contratos (OpenAPI, eventos) definidos cedo deixam módulos avançarem em paralelo sem se pisar.
5. **Riscos primeiro.** Coloque cedo os itens que mais podem invalidar decisões (assinatura de tokens, modelo de dados central). Descobrir na rodada 3 que uma ADR estava errada custa menos que na rodada 30.
6. **Detalhe só no próximo marco.** Planeje em detalhe o marco atual; os seguintes ficam em linhas gerais e só ganham specs quando chegar a vez deles. Specs escritas cedo demais envelhecem antes de serem usadas.
7. **Marcos com critério de saída verificável.** Um marco termina quando algo observável funciona e a suíte completa passa, não quando a lista acaba.

&#91;embedded content: roadmap · 4 marcos, 3 portões, detalhe decrescente\]

O marco atual e o anterior têm itens e specs escritos; os seguintes ficam mais grossos quanto mais distantes, e cada portão exige um critério observável antes de o próximo marco começar.

### Fatias boas e ruins

| Ruim (horizontal ou vago) | Bom (vertical e verificável) |
| --- | --- |
| "Criar todas as entidades JPA" | "Cadastro de usuário: POST /usuarios persiste e retorna 201" |
| "Camada de segurança" | "Login com senha retorna sessão; senha errada retorna 401" |
| "Melhorar o token" | "/token com PKCE: critérios CA1 a CA3 de `specs/token.md`" |

### Formato do `docs/roadmap.md`

```markdown
# Roadmap — IdP
Atualizado: 2026-10-14 · Marco atual: M1

## M0 — Esqueleto (concluído)
Critério de saída: CI verde; ArchUnit ativo; ADR-0001 a 0003 aceitas.
| ID   | Item                       | Status | Depende de | Spec |
| R0.1 | Projeto Spring, CI, ArchUnit | feito | —        | —    |

## M1 — Login mínimo (em andamento)
Critério de saída: cadastro e login de ponta a ponta; suíte completa
verde; revisão de marco sem item Crítico.
| ID   | Item               | Status    | Depende de | Spec               |
| R1.1 | Cadastro de usuário | feito     | R0.1       | specs/usuario.md   |
| R1.2 | Login com senha     | próximo   | R1.1       | specs/login.md     |
| R1.3 | Sessão no IdP       | bloqueado | R1.2       | specs/sessao.md    |

## M2 — OIDC (planejamento grosso)
- /authorize · /token com PKCE · JWKS · documento de descoberta

## Fora do roadmap
- Ver não-objetivos em `docs/escopo.md`.
```

### Vocabulário de status

| Status | Significado | Quem muda |
| --- | --- | --- |
| planejado | Existe, mas ainda não está na vez | `/roadmap` |
| próximo | Dependências feitas; é o que `/feature` pega | `/handoff` |
| em andamento | Uma rodada trabalhou nele e não terminou | `/handoff` |
| bloqueado | Depende de item ou questão em aberto (cite o Q#) | Qualquer etapa |
| feito | Critérios de aceitação verdes e revisão sem Crítico | `/handoff` |
| adiado | Saiu do marco; motivo em `pendencias.md` | Você |

### Onde o roadmap se encaixa

O roadmap é **híbrido**. A estrutura (marcos, ordem, dependências, critérios de saída) é **referência**: muda por decisão sua, por meio da skill `/roadmap` (seção 21). Já a coluna de status é **estado**: o `/handoff` atualiza ao fim de cada rodada, e só ela. Essa divisão evita que um agente reordene o projeto por conta própria enquanto mantém o status sempre atual.

Na estrutura de pastas da seção 17, ele mora em `docs/roadmap.md`, ao lado do escopo, e o CLAUDE.md o cita no mapa: "Próximo trabalho: `docs/roadmap.md`, item com status próximo".

## 21. Executando o roadmap: rodadas, paralelismo e automação

Um roadmap só funciona se o processo em volta dele for repetível. A ideia central é uma **hierarquia de orquestradores**: uma skill planeja o marco, outra executa um item por rodada, outra fecha a rodada e outra fecha o marco.

### Hierarquia de skills

| Nível | Skill | Responsabilidade | Frequência | Portão humano |
| --- | --- | --- | --- | --- |
| Marco | `/roadmap` | Quebrar o próximo marco em itens, ordenar, escrever specs | Por marco | Você aprova o marco |
| Rodada | `/feature` | Executar um item (fluxo da seção 19) | Por item | Você aprova o plano |
| Sessão | `/handoff` | Atualizar status, estado e histórico | Por sessão | Você faz o commit |
| Marco | `/fechar-marco` | Regressão, revisão de marco, consolidação | Por marco | Você aceita o marco |

### `/roadmap`: planejar o próximo marco

```markdown
---
name: roadmap
description: Detalha o próximo marco do roadmap em itens verticais com specs e dependências
argument-hint: <ID do marco, ex.: M2>
disable-model-invocation: true
---
Marco: $ARGUMENTS

1. Leia `docs/roadmap.md`, `docs/escopo.md`, os requisitos não funcionais,
   as ADRs aceitas e `docs/questoes-em-aberto.md`.
2. Use o subagente `explorador` para mapear o que já existe no código.
3. Proponha itens como fatias verticais, cada um com: ID, descrição numa frase,
   dependências e critérios de aceitação. Itens de maior risco primeiro.
4. Proponha o critério de saída do marco, verificável.
5. Liste decisões arquiteturais que o marco exige: viram questões em aberto
   ou ADRs propostas (/nova-adr). Nunca as decida em silêncio.
6. PARE e apresente a proposta. Só após aprovação: escreva as specs em
   `docs/specs/` e atualize a seção do marco em `docs/roadmap.md`.
```

### `/feature` escolhendo o próximo item

O orquestrador da seção 19 ganha uma regra no topo: sem argumento, ele pega o trabalho do roadmap.

```markdown
## Antes de tudo
- Se houver `plano-atual.md` em andamento, continue-o.
- Senão, se o pedido estiver vazio, pegue em `docs/roadmap.md` o primeiro item
  com status "próximo" cujas dependências estejam "feito". Leia a spec dele.
- Se nenhum item estiver desbloqueado, PARE e diga o que bloqueia cada um.
```

### O ciclo de uma rodada

1. **Sessão nova.** Uma rodada por sessão (ou `/clear` entre rodadas). O guia de boas práticas do Claude Code recomenda exatamente isso: escrita a spec, executá-la numa sessão nova com contexto limpo.
2. **Abertura.** O hook `SessionStart` injeta `estado.md`; o CLAUDE.md aponta para o roadmap.
3. **Execução.** `/feature` pega o item, planeja, testa, implementa e revisa.
4. **Fechamento.** `/handoff` marca o item como feito (ou em andamento, com o motivo), promove para "próximo" os itens que acabaram de ser desbloqueados, atualiza `estado.md` e grava o histórico.
5. **Commit** feito por você, citando o ID: `feat(login): senha com BCrypt (R1.2, ADR-0004)`.

### `/fechar-marco`: a defesa contra deriva

O maior risco de muitas rodadas é a **deriva**: cada rodada é localmente correta, mas o conjunto perde coerência. O fechamento de marco é a rodada que olha para o todo:

- [ ] Suíte completa e regressão verdes, não só os testes das features do marco.
- [ ] Critério de saída do marco demonstrado com evidência (saída de testes, chamada real ao endpoint).
- [ ] Subagente revisor em contexto limpo compara o código com o roadmap, as ADRs aceitas e os requisitos não funcionais.
- [ ] Consolidação: remover duplicações, atualizar `visao-geral.md` e `modelo-dados.md`.
- [ ] `/doctor prompt-audit` para achar instruções desatualizadas ou contraditórias no CLAUDE.md, regras, skills e subagentes.
- [ ] Correções que você repetiu durante o marco viram linha no CLAUDE.md, hook ou teste.
- [ ] Itens não terminados: adiados com motivo ou movidos para o próximo marco.
- [ ] Você aceita o marco e roda `/roadmap` para o seguinte.

### Paralelizar itens independentes

Quando o roadmap mostra itens sem dependência entre si, eles podem rodar ao mesmo tempo. A coluna "Depende de" é o que torna isso seguro de decidir.

| Forma | Como | Cuidado |
| --- | --- | --- |
| Sessões em worktrees | Uma sessão por item com `claude --worktree`, cada uma em sua branch; integração por PR | Atualizar o status no roadmap só no merge, para não haver conflito no próprio arquivo |
| Subagentes isolados | `isolation: worktree` no frontmatter | Bom para itens pequenos dentro de uma sessão |
| Agent teams | Um líder distribui itens a teammates | Experimental e desativado por padrão; sem worktree, então cada teammate deve ser dono de arquivos diferentes |
| `/batch` | Divide uma mudança grande em 5 a 30 subagentes em worktrees | Para mudanças mecânicas, não para features com decisões |
| Dynamic workflows | Script que roda muitos subagentes e cruza os resultados | Migrações e auditorias de grande escala |

### Automatizar o laço entre rodadas

Com o processo estável e bem testado, as rodadas podem rodar com menos intervenção. O guia de boas práticas mostra o padrão de laço com `claude -p`, pré-aprovando ferramentas com `--allowedTools` e usando `--permission-mode dontAsk`, que nega tudo que exigiria aprovação:

```bash
# Roda itens do marco atual até um falhar ou acabarem
for i in 1 2 3; do
  claude -p "/feature-auto" \
    --allowedTools "Edit,Write,Bash(./mvnw *),Bash(git status *),Bash(git diff *)" \
    --permission-mode dontAsk || break
done
```

Atenção: o `/feature` deste guia **para no plano** esperando sua aprovação. **Inferência** (do exemplo `/feature` e do comportamento do modo `dontAsk`): num laço não interativo, isso encerraria cada rodada sem implementar nada. Por isso o laço chama uma variante, `/feature-auto`, igual ao `/feature` mas sem essa parada: os portões passam a ser só os automáticos (testes falhando antes, `./mvnw verify` verde, revisor sem item Crítico), e a aprovação humana se desloca para o `/fechar-marco`. O `|| break` interrompe o laço quando uma execução termina com erro.

O mesmo guia recomenda testar em dois ou três itens, ajustar o prompt e só então rodar o restante. Outras formas de manter o trabalho andando:

- **`/goal`:** um avaliador separado reconfere uma condição a cada turno ("todos os testes do M1 passam").
- **Hook `Stop`:** impede o fim do turno enquanto a checagem não passar.
- **Projects:** conversa contínua na nuvem que dispara sessões paralelas, pensada para trabalho de dias ou semanas (beta pública nos planos Pro e Max, segundo a documentação).

Automatizar não elimina os portões humanos: desloca-os. Em vez de aprovar cada plano, você aprova cada marco no `/fechar-marco`.

### Qual estratégia usar

| Situação | Estratégia principal |
| --- | --- |
| Projeto de portfólio, uma pessoa | Rodada zero + roadmap + uma sessão por item, com portões em plano e commit |
| Módulos independentes com contratos claros | Itens em paralelo, cada um numa worktree |
| Mudança mecânica em muitos arquivos | `/batch` ou dynamic workflows |
| Processo estável, testes confiáveis | Laço com `claude -p`, portão humano por marco |
| Trabalho longo que deve seguir sem sua máquina | Projects na nuvem |

**Proposta deste guia:** comece pela primeira linha. Paralelismo e automação só entram depois que o processo provou, em alguns marcos, que mantém a qualidade sem supervisão a cada passo.

## 22. Armadilhas e boas práticas

| Armadilha | Sintoma | Correção |
| --- | --- | --- |
| CLAUDE.md inchado | Regras ignoradas; perguntas já respondidas no arquivo | Menos de 200 linhas; mover procedimentos para skills e regras para `.claude/rules/` com `paths` |
| Importar documentos grandes com `@` | Contexto cheio desde o início da sessão | Citar o caminho entre crases; o agente lê quando precisa |
| Documento desatualizado | Agente obedece a uma regra que já mudou | Tratar docs como código: revisar no mesmo PR; rodar `/doctor prompt-audit` |
| Instruções contraditórias | O Claude escolhe uma delas, às vezes a errada | Uma informação num lugar só; ADR com status |
| Regra crítica só como instrução | Às vezes é seguida, às vezes não | Converter em hook, permissão ou teste |
| Descrições de subagentes vagas ou sobrepostas | Delegação errada ou ausente | Descrições curtas e específicas, uma responsabilidade por agente |
| Subagente sem contexto suficiente | Resultado genérico | Lembrar que ele não vê a conversa: pôr o necessário no prompt dele ou num arquivo que ele saiba ler |
| Revisor que acha problema em tudo | Superengenharia | Pedir só o que afeta corretude e requisitos |
| Paralelismo sem isolamento | Agentes sobrescrevendo arquivos uns dos outros | Worktrees; em agent teams, dividir arquivos por dono |
| Conteúdo externo tratado como ordem | Instruções escondidas em issues ou páginas web | Tratar como dado; o Claude Code já marca e escaneia relatórios de subagentes, mas permissões continuam sendo a defesa |
| Corrigir o mesmo erro repetidamente | Contexto poluído por tentativas falhas | Após duas correções, `/clear` e um prompt melhor |

### Por onde começar

Não é preciso montar tudo de uma vez. A documentação sugere crescer por gatilho, e uma ordem razoável para um projeto de portfólio é:

1. CLAUDE.md curto, `escopo.md` com não-objetivos e `definicao-de-pronto.md`.
2. Um subagente `revisor` somente leitura.
3. ADRs para as decisões que já existem, e a skill `/nova-adr`.
4. Testes de arquitetura (ArchUnit) para as ADRs mais importantes.
5. `memoria/estado.md` com o hook `SessionStart`.
6. O orquestrador `/feature`, quando o fluxo já estiver claro na prática.

Quando o projeto deixar de caber numa rodada, acrescente o roadmap e a rodada zero (seções 20 e 21) antes de pensar em paralelismo ou automação.

Uma pasta `.claude/` e uma pasta `docs/` bem organizadas mostram a quem avalia o repositório que você **projeta o processo** de desenvolvimento com agentes, e não só que usa IA. E as ADRs, lidas com atenção, são o caminho para passar a justificar as escolhas técnicas que hoje você delega.

## Os exemplos e o que cada um demonstra

Os exemplos deste guia são ilustrações montadas sobre o comportamento documentado; nenhum foi executado para este documento.

| Exemplo | O que ilustra | O que não está demonstrado |
| --- | --- | --- |
| CLAUDE.md como mapa (seção 3) | Constituição curta que aponta para documentos por caminho | Que esse conteúdo baste para um projeto real |
| Revisor somente leitura (seção 4) | Ferramentas mínimas e memória própria | Que fique sem escrita: com `memory`, ganha Read, Write e Edit |
| Skill `nova-adr` (seção 5) | Injeção de contexto dinâmico e script pré-aprovado | O script `proximo-numero.sh`, que não é mostrado |
| Hooks de três garantias (seção 7) | `SessionStart`, `PreToolUse` e `PostToolUse` | O script `proteger-adr-aceita.sh`, que não é mostrado; o custo de rodar a suíte a cada edição em projetos grandes |
| `settings.json` (seção 8) | `allow`, `ask` e `deny` combinados | Que bloqueie variações de comando: regras de Bash casam o texto escrito |
| Tarefa `/token` (seção 18) | Quatro agentes, dois portões humanos e um laço de revisão | Que o fluxo produza o resultado esperado; é um roteiro, não um relato de execução |
| Laço com `claude -p` (seção 21) | Padrão documentado no guia de boas práticas | A skill `/feature-auto`, só descrita |

## O que as fontes não decidem

- **Quantos subagentes e com que modelo cada um.** A documentação descreve os campos e os limites; a divisão é do projeto.
- **Onde guardar o estado da tarefa.** A pasta `memoria/` é proposta deste guia; a documentação oferece auto memory e memória de subagente, com outros propósitos.
- **O tamanho de uma rodada.** A heurística da seção 20 é deste guia.
- **Quando automatizar o laço entre rodadas.** O guia de boas práticas recomenda testar em dois ou três itens antes; o momento é do projeto.
- **Que subconjunto de testes rodar no `PostToolUse` em projetos grandes.**
- **Que formato de ADR usar.** O de Nygard é um entre vários; a escolha é convenção.
- **Quando passar de `.claude/` a plugin.** A documentação sugere quando um segundo repositório precisar da mesma configuração; o resto é julgamento.

## Limites

- **Volatilidade.** As afirmações sobre o Claude Code valem para a documentação consultada em 14 de outubro de 2026; números de versão, limites e nomes de campos podem mudar.
- **Recursos não estáveis.** Agent view está em prévia de pesquisa; agent teams é experimental e desativado por padrão; hooks do tipo `agent` são experimentais; Projects está em beta pública.
- **Práticas gerais sem fonte citada.** ADRs, ArchUnit, migrations e estratégia de testes não vêm da documentação do Claude Code.
- **Exemplos não executados.** Ver "Os exemplos e o que cada um demonstra".
- **Modo de leitura não registrado.** As referências não indicam se cada página foi lida inteira.
- **Páginas relacionadas não citadas diretamente.** Agent teams, worktrees, dynamic workflows, hooks reference e plugins têm páginas próprias, das quais só duas foram conferidas na revisão.

## Checklist

Cada item traz o tipo da afirmação e, depois do travessão, o nível de garantia da seção 15: **teste** (no build e no CI), **hook ou permissão** (na sessão configurada) ou **instrução** (um pedido). A ordem vai do nível mais forte ao mais fraco.

**Teste no build e no CI**

- [ ] ADRs mais importantes verificadas por ArchUnit (Prática geral) — teste
- [ ] CI roda o build completo a cada push (Prática geral) — teste
- [ ] Nenhum dado sensível em log verificado por teste que captura a saída (Proposta deste guia) — teste

**Hook ou permissão**

- [ ] `deny` para leitura do `.env` e para `git push`; `ask` para ADRs, contratos, commits e migrations (Proposta deste guia, sobre regras documentadas) — hook ou permissão
- [ ] Hook `SessionStart` injeta `memoria/estado.md`, inclusive após compactação (Proposta deste guia, sobre hook documentado) — hook ou permissão
- [ ] Hook `PreToolUse` impede reescrever ADR aceita e editar migration existente (Proposta deste guia) — hook ou permissão
- [ ] Hook `PostToolUse` roda os testes, ou um subconjunto rápido, após cada edição (Proposta deste guia) — hook ou permissão
- [ ] Subagentes com `tools` mínimas; revisor e explorador sem `Edit`, considerando o efeito do campo `memory` (Documentado) — hook ou permissão
- [ ] `disable-model-invocation: true` só nos pontos de entrada que você aciona (Documentado) — hook ou permissão
- [ ] Sandbox para restrições de rede e de sistema de arquivos que não dependam do texto do comando (Documentado) — hook ou permissão
- [ ] Conteúdo externo tratado como dado, com permissões como defesa (Documentado) — hook ou permissão

**Instrução**

- [ ] CLAUDE.md com menos de 200 linhas, como mapa, com documentos grandes citados entre crases e sem `@` (Documentado) — instrução
- [ ] Regras de parte do código em `.claude/rules/` com `paths` (Documentado) — instrução
- [ ] Procedimentos repetidos como skills, com corpo abaixo de 500 linhas (Documentado) — instrução
- [ ] Skill em `context: fork` com tarefa explícita (Documentado) — instrução
- [ ] Tudo que o subagente precisa no prompt dele, no CLAUDE.md ou num arquivo que ele saiba ler (Documentado) — instrução
- [ ] Descrições de subagentes curtas, específicas e sem sobreposição (Documentado) — instrução
- [ ] Revisor instruído a apontar só o que afeta corretude ou requisitos (Documentado) — instrução
- [ ] ADRs numeradas, com status e data; aceitas tratadas como imutáveis (Prática geral) — instrução
- [ ] Escopo com não-objetivos; specs com arquivos, fora do escopo e verificação de ponta a ponta (Documentado) — instrução
- [ ] Definição de pronto como critério de parada (Proposta deste guia) — instrução
- [ ] `estado.md` numa tela, com data; `/handoff` move o passado para o histórico (Proposta deste guia) — instrução
- [ ] Paralelismo só com tarefas independentes; worktrees; em agent teams, arquivos divididos por dono (Documentado) — instrução
- [ ] Recurso experimental ou de prévia não usado como base sem ressalva (Documentado) — instrução
- [ ] Laço automatizado testado em dois ou três itens antes de rodar o restante (Documentado) — instrução
- [ ] `/doctor prompt-audit` ao fechar cada marco (Documentado) — instrução

## Mapa de consulta

| Dúvida | Seção | Página oficial |
| --- | --- | --- |
| Quanto contexto cada recurso consome? | 2 | Features overview |
| O que vai no CLAUDE.md e o que vai em regras? | 3 | Memory |
| Como criar um subagente e o que ele recebe? | 4 | Subagents |
| Skill de referência ou de tarefa? | 5 | Skills |
| Como montar um comando orquestrador? | 6 | Skills |
| Como garantir que algo sempre aconteça? | 7 | Hooks; Hooks reference |
| Como restringir o que cada agente pode fazer? | 8 | Permissions |
| Como conectar sistemas externos ou reutilizar a configuração? | 9 | Plugins |
| Como rodar agentes em paralelo? | 10 | Agents |
| Que fluxo de trabalho seguir? | 11 | Best practices |
| Como registrar decisões e requisitos? | 12 a 14 | — (prática geral) |
| Como transformar uma regra em teste? | 15 | — (prática geral) |
| Onde guardar o estado de trabalho? | 16 e 17 | Memory; Permissions (proposta deste guia) |
| Como fica uma tarefa completa? | 18 e 19 | — (proposta deste guia) |
| Como trabalhar em várias rodadas? | 20 e 21 | Best practices; Agents |
| O que costuma dar errado? | 22 | Best practices |

## 23. Referências

Páginas da documentação oficial do Claude Code consultadas em 14/10/2026. O modo de leitura de cada página (inteira ou em partes) não foi registrado. Todas são documentação do fornecedor sobre o próprio produto.

| Página | Leitura | Peso | Usada para |
| --- | --- | --- | --- |
| [Extend Claude Code (visão geral dos recursos e custos de contexto)](https://code.claude.com/docs/en/features-overview.md) | Não registrado | Alto, para o produto na data | Seção 2: custos de contexto e crescimento por gatilho |
| [How Claude remembers your project (CLAUDE.md, regras, auto memory)](https://code.claude.com/docs/en/memory.md) | Não registrado | Alto, para o produto na data | Seções 3 e 16 |
| [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | Não registrado | Alto, para o produto na data | Seções 4 e 16 |
| [Extend Claude with skills (inclui comandos personalizados)](https://code.claude.com/docs/en/skills.md) | Não registrado | Alto, para o produto na data | Seções 5 e 6 |
| [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide.md) | Não registrado | Alto, para o produto na data | Seção 7 |
| [Configure permissions](https://code.claude.com/docs/en/permissions.md) | Não registrado | Alto, para o produto na data | Seções 8 e 16 |
| [Run agents in parallel](https://code.claude.com/docs/en/agents.md) | Não registrado | Alto, para o produto na data; recursos experimentais ou de prévia | Seções 10 e 21 |
| [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices.md) | Não registrado | Alto, para o produto na data | Seções 11, 13, 14 e 21 |
| [Índice completo da documentação](https://code.claude.com/docs/llms.txt) | Índice | — | Localizar as páginas |

Conferidas na revisão do documento:

| Página | Leitura | Peso | Usada para |
| --- | --- | --- | --- |
| [Create a Claude Code plugin (estrutura de pastas do plugin)](https://code.claude.com/docs/en/plugins/create.md) | Ponto conferido: estrutura de pastas | Alto, para o ponto | Seção 9 |
| [Hooks reference (comportamento do código de saída 2 por evento)](https://docs.anthropic.com/en/docs/claude-code/hooks) | Ponto conferido: código de saída 2 por evento | Alto, para o ponto | Seção 7 |

Páginas relacionadas, não citadas diretamente aqui, para aprofundar: agent teams, worktrees, dynamic workflows, hooks reference e plugins, todas listadas no índice acima.

Conteúdo sobre ADRs, ArchUnit, migrations e estratégia de testes vem de práticas gerais de engenharia de software, não da documentação do Claude Code.
