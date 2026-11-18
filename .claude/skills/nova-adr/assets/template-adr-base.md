# Conteúdo da ADR de base do projeto

Indica o que a **ADR de base** (título `Base do projeto: ...`) precisa trazer. Ela é proposta
pelo agente `arquiteto` no modo `fundacao` (fluxo `/fundacao`) e é a única ADR que os fluxos
leem para operar: o orquestrador a encontra pelo título, tira dela o perfil de stack que passa
aos agentes, e os agentes tiram dela os comandos. Um item ausente aqui trava o `/feature`.

A estrutura continua sendo a de `template-adr.md`, sem seção a mais nem a menos, e as regras
continuam sendo as do `SKILL.md` desta skill. Este arquivo só diz o que entra em cada seção
quando a ADR é a de base. Ele é independente de stack: o que é próprio da stack (opções de
ferramenta, comandos padrão, identificadores `FER-nn`) vem do perfil escolhido.

## Antes de redigir

- A stack pedida precisa ter um perfil em `.claude/skills/perfil-*/`. Se não tiver, ou se nenhum
  perfil atender à visão, não redija a ADR: leve isso a "Perguntas para o usuário".
- Leia, no perfil escolhido, o `SKILL.md`, o `arquiteto.md` (opções de ferramenta da stack) e o
  `qualidade.md` (a lista de ferramentas exigidas, `FER-nn`).
- Esta ADR é a exceção declarada à regra "uma decisão por ADR": stack, perfil, ferramentas, CI e
  Dockerfile ficam juntos nela. Não a divida e não use essa exceção em nenhuma outra ADR.

## Por seção

### Título

`NNNN. Base do projeto: <stack> com <nome da pasta do perfil>`. O prefixo `Base do projeto:` é
fixo, porque é por ele que a ADR é localizada no índice. Uma ADR que substitua a de base usa o
mesmo prefixo.

### Status

`Proposto`, com a data recebida de quem invocou. Se ela substitui uma ADR de base aceita, a
primeira linha leva `— substitui ADR-NNNN`.

### Contexto

- O que a visão do produto impõe à escolha: público, problema e objetivos que pesam na stack,
  descritos pelo conteúdo, sem citar caminho de arquivo.
- A stack pedida pelo usuário, na frase dele.
- Os perfis de stack disponíveis no sistema. Se só houver um, diga isso: a escolha de stack
  ficou restrita a ele.
- Restrições conhecidas de ambiente e de quem vai manter o projeto.
- Os direcionadores da decisão, em ordem de prioridade.

Cada afirmação factual leva a marca de origem que o arquiteto usa (`[usuário]`, `[suposição]`
e as demais).

### Decisão

Uma frase com a escolha central ("Vamos ..."), seguida destes itens, todos obrigatórios:

1. **Stack:** linguagem e framework, com as versões.
2. **Perfil:** o nome exato da pasta do perfil (o mesmo do título). É o valor que o orquestrador
   repassa aos agentes.
3. **Build:** a ferramenta de build escolhida entre as que o perfil admite, e os comandos de
   build completo com testes, só testes, testes de uma rodada e um teste isolado. Os comandos
   registrados aqui prevalecem sobre os padrões do perfil.
4. **Ferramentas exigidas:** uma tabela com uma linha para **cada** `FER-nn` do `qualidade.md` do
   perfil, sem pular nenhuma:

   | FER | Ferramenta e versão | Comando |
   | --- | --- | --- |

   Onde o perfil oferece alternativas para uma `FER-nn`, registre a escolhida. Uma `FER-nn` que o
   perfil marca como condicional aparece na tabela mesmo assim, com "adotada" (e o comando) ou
   "não adotada" (e o motivo).
5. **Ferramentas de teste:** as bibliotecas de cada nível de teste (unitário, integração,
   aceitação, arquitetura) e se os testes de integração usam serviços reais em contêiner. O
   escritor declara essas dependências no build uma única vez, a partir desta lista.
6. **CI:** o provedor e o que o pipeline executa (ao menos o build e as ferramentas da tabela).
7. **Dockerfile:** adota ou não adota, com o motivo.

### Consequências

- Positivas: o que a base passa a garantir desde a primeira feature.
- Negativas: ao menos estas duas. Trocar qualquer ferramenta desta lista exige uma ADR nova que
  substitua esta inteira; e o que faria a decisão ser revista (os gatilhos de revisão).

### Diretrizes

- A primeira é sempre: a aplicação DEVE subir no perfil de teste.
- Depois, as de estrutura do código que a base já fixa (onde fica a classe ou o módulo
  principal, a estrutura de pacotes), se houver.
- Cada uma verificável e citável como `ADR NNNN/d<n>`. Diretriz que só fará sentido quando
  houver código de produto entra aqui do mesmo jeito; o adiamento do teste dela é registrado
  na especificação de testes da fundação ("Diretrizes adiadas"), não na ADR.

### Verificação

Uma linha por diretriz. A da aplicação que sobe é verificada pelo teste de fumaça. As
estruturais dizem com que ferramenta do perfil são verificadas.

### Alternativas consideradas

- Cada outro perfil disponível que poderia atender à visão, e por que não foi escolhido. Se não
  havia outro perfil, registre isso como a razão de não haver alternativa de stack.
- Cada opção de ferramenta que o perfil oferecia e foi preterida, com o motivo.

## Fora da ADR

- O resumo para quem decide e as questões em aberto vão no relatório do arquiteto ao
  orquestrador, não na ADR.
- Contratos: a base não tem fronteiras de produto.
- Decisões de produto: público, problema e objetivos são da visão.
- Esta ADR passa do tamanho usual de uma ADR por causa da tabela de ferramentas; isso é
  esperado. O que não é decisão de base continua fora dela.
