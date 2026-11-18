---
name: auditar-critico
description: Audita o agente senso-critico a partir de um gatilho concreto — uma ADR substituída, um /bugfix cuja causa está num artefato que o crítico examinou, ou a recorrência de recusas por "gatilho improcedente" (3 ou mais nos 10 itens mais recentes). Monta o dossiê com os relatórios SC-R, as respostas e as Descartadas pertinentes, e o apresenta ao usuário, que julga. De uso exclusivo do usuário, que a invoca com /auditar-critico: nenhum fluxo nem skill a invoca ou sugere (os fluxos só informam os gatilhos que detectam). Não roda por calendário nem sem gatilho.
argument-hint: "adr <NNNN> | bugfix <slug> | recorrencia"
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash(git log *) Bash(git show *) Bash(date *)
---

# Auditoria do senso crítico

Você é o **orquestrador**. Quem julga o crítico é o usuário: você monta o dossiê e apresenta. Nenhum agente audita o crítico, porque outra instância do mesmo modelo compartilha os priors dele e não está "de fora". O que está de fora é o usuário e as consequências: o que de fato aconteceu depois da decisão examinada.

Gatilho: `$ARGUMENTS`

## Regra de gatilho

A auditoria segue o mesmo critério de parada do crítico: só começa com um gatilho concreto. São três:

| Gatilho | Origem | Pergunta da auditoria |
| --- | --- | --- |
| `adr <NNNN>` | uma ADR passou a `Substituído por` (Portão 2 do `/feature` ou do `/fundacao`) | o crítico viu o problema que levou à substituição? |
| `bugfix <slug>` | a causa ou a fonte de um defeito está num artefato que o crítico examinou | o crítico viu a premissa que falhou? |
| `recorrencia` | 3 ou mais recusas com o rótulo `gatilho improcedente` nos 10 itens `SC-nnn` mais recentes | o crítico está produzindo objeções genéricas, vindas de priors? |

Sem um desses, não audite: diga ao usuário que falta o gatilho.

## Procedimento

1. **Localize o material.**
   - `adr`: a ADR substituída, a substituta (a seção Contexto diz por que mudou) e os relatórios `docs/senso-critico/SC-R-*.md` cujo cabeçalho cita a ADR substituída, como objeto ou como fundação.
   - `bugfix`: o registro `docs/execucoes/<slug>.md` (causa confirmada, fonte), o enquadramento `docs/testes/<slug>/enquadramento.md` e os relatórios cujo objeto inclui o artefato onde está a causa.
   - `recorrencia`: os 10 itens mais recentes e, entre eles, os recusados por `gatilho improcedente`, com o gatilho que o crítico citou e a resposta que o recusou.
2. **Classifique, para `adr` e `bugfix`,** a relação entre o que aconteceu e o que o crítico registrou:
   - **viu e foi ouvido**: item acatado; a falha veio depois, por outro motivo ou apesar da revisão;
   - **viu e foi recusado**: item recusado ou respondido; o problema é a calibração de quem decidiu, não do crítico;
   - **descartou**: a premissa está em Descartadas; diga por qual filtro (sem gatilho, não estrutural, já justificada, custo baixo, não acionável, fora do orçamento);
   - **não viu**: a premissa não aparece em lugar nenhum (falso negativo); diga se havia gatilho no contexto da época.
3. **Para `recorrencia`,** procure o padrão: a mesma preocupação em objetos diferentes (escala, concorrência, segurança genérica), gatilhos que citam o documento mas não sustentam a dúvida, objeções cujo conteúdo não depende do projeto.
4. **Apresente ao usuário o dossiê**, sem concluir por ele: o gatilho, os relatórios e itens envolvidos (identificadores e caminhos), a classificação com a evidência e as perguntas a decidir:
   - o crítico precisa de ajuste? Qual: um filtro, o orçamento, uma instrução de exame, o limiar de recorrência;
   - a falha é de quem decidiu, e não do crítico?
   - nada a fazer.
5. **Registre a decisão** do usuário como D-XXX pela skill `nova-memoria` (operação 5): título "Auditoria do crítico: <gatilho>", `Decisão` com a frase dele, `Motivo` com a classificação. Um ajuste no agente ou nas skills é alteração em `.claude/`: segue as regras de método (relatório e permissão), fora desta skill.

## Limites

- Você não edita relatórios do crítico nem reabre itens. A auditoria olha para trás; um gatilho novo sobre uma decisão vigente vai ao próximo exame, pelo fluxo normal.
- Não reinvoque o crítico para se defender: a defesa dele é o próprio relatório, que já registra o que viu e o que descartou.
