# Impedimentos

Atualizado: 2026-11-11

## Instruções

- **O que entra:** algo que trava ou impede a continuidade de uma tarefa e que a IA
  não pode resolver sozinha (decisão pendente do usuário, informação faltando,
  dependência externa, erro sem solução encontrada).
- **Não entra:** dívida técnica ou tarefa adiada por escolha. Isso não trava nada.
- **Quando registrar:** assim que o travamento for identificado, antes de parar
  ou mudar de tarefa.
- **Ao resolver:** preencha `Resolução`, mude o status e mova a entrada para
  "Resolvidos". Se a resolução gerou uma decisão, registre-a em `decisoes.md`
  e cite o ID.
- **Início de sessão:** leia "Abertos" antes de retomar qualquer tarefa.
- IDs sequenciais: I-001, I-002, ...

### Formato de entrada aberta

```markdown
### I-XXX — <título curto do impedimento>

- **Aberto em:** AAAA-MM-DD
- **Tarefa travada:** <TASK-NNN; sem tarefa, descrição curta>
- **Tipo:** decisão pendente | informação faltante | dependência externa | erro técnico
- **Descrição:** <o que está travando, em fatos>
- **O que destrava:** <ação ou resposta concreta necessária>
- **Depende de:** usuário | IA | terceiro
```

### Formato de entrada resolvida

```markdown
### I-XXX — <título>

- **Aberto em:** AAAA-MM-DD · **Resolvido em:** AAAA-MM-DD
- **Tarefa travada:** <TASK-NNN; sem tarefa, descrição curta>
- **Resolução:** <como foi destravado; cite D-XXX se gerou decisão>
```

## Abertos

## Resolvidos
