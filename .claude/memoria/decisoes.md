# Decisões de pequeno porte

Atualizado: 2026-11-18

## Instruções

- **O que entra:** decisões tomadas durante a implementação que não justificam
  uma ADR, mas que alguém precisaria conhecer para não desfazê-las ou repeti-las
  (ex.: nome de convenção, biblioteca auxiliar, formato de um arquivo interno).
- **Vira ADR, e não entra aqui,** a decisão que atinge vários módulos, muda a
  arquitetura ou a stack, ou é cara de reverter. Na dúvida, pergunte ao usuário.
- **Quando registrar:** logo após a decisão ser tomada ou aprovada.
- **Não apague entradas.** Se uma decisão mudar, marque-a como `substituída por D-XXX`
  ou `promovida a ADR-XXXX` e registre a nova.
- **Disposição de apontamento** (revisão, auditoria) também entra aqui como D-XXX,
  com a `Decisão` no formato "Apontamento <x>: aceito | corrigido | descartado — <motivo>".
- **Resultado de spike** (fluxo `/spike`) também entra aqui como D-XXX, com o título
  "Spike: <pergunta>". Não é uma decisão do projeto: é a evidência de um experimento.
  `Decisão` traz a resposta (sim, não, número ou inconclusivo) e a data; `Motivo`, os
  comandos, a saída que decide e as versões; `Afeta`, os limites de validade. Quem
  decidir com base nele cita `[spike: D-XXX]`.
- Entradas mais recentes no topo. IDs sequenciais: D-001, D-002, ...

### Formato de cada entrada

```markdown
### D-XXX — <título curto da decisão>

- **Data:** AAAA-MM-DD
- **Tarefa:** <TASK-NNN; sem tarefa, descrição curta>
- **Status:** vigente | substituída por D-XXX | promovida a ADR-XXXX
- **Decisão:** <uma ou duas frases, no imperativo ou afirmativo>
- **Motivo:** <por que esta opção>
- **Alternativas descartadas:** <opção — motivo; opcional>
- **Afeta:** <arquivos, módulos ou convenções atingidos>
```

## Registros
