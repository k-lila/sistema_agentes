# Exemplos de ADR

## ADR preenchida

**Entrada:** "Escolhemos PostgreSQL em vez de MongoDB para o user service porque precisamos de
transações e os dados são relacionais, mesmo o time conhecendo melhor o Mongo."

**Saída** (`docs/adr/0001-usar-postgresql-para-persistencia.md`):

```markdown
# 0001. Usar PostgreSQL para persistência

## Status

- Proposto — 2026-08-27
- Aceito — 2026-08-27

## Contexto

O user service armazena contas, papéis e seus relacionamentos, e várias
operações precisam ser atômicas, como criar uma conta e seu papel padrão
juntos. O time tem mais experiência com MongoDB do que com bancos relacionais.

## Decisão

Vamos usar o PostgreSQL como camada de persistência do user service.

## Consequências

Positivas:

- Transações ACID cobrem as operações atômicas que precisamos.
- O modelo relacional mapeia naturalmente nossas entidades via chaves
  estrangeiras.

Negativas:

- O time precisará investir tempo aprendendo modelagem relacional e SQL.

## Diretrizes

1. A persistência do user service DEVE usar PostgreSQL.
2. Operações que gravam mais de uma entidade DEVEM rodar numa única transação.

## Verificação

- d1: teste de integração contra uma instância real de PostgreSQL.
- d2: revisão humana dos serviços que gravam mais de uma entidade.

## Alternativas consideradas

- **MongoDB** — familiar ao time, mas transações entre múltiplos documentos
  são complicadas e os dados são naturalmente relacionais.
```

## Substituição

Status da ADR nova (`0007`), após ser aceita:

```markdown
- Proposto — 2027-03-02 — substitui ADR-0001
- Aceito — 2027-03-10
```

Status da ADR antiga (`0001`), com a linha acrescentada no mesmo dia:

```markdown
- Proposto — 2026-08-27
- Aceito — 2026-08-27
- Substituído por ADR-0007 — 2027-03-10
```
