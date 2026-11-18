# CLAUDE.md

Projeto exploratório para criação de um sistema de agentes de IA para desenvolvimento de softwares. Sub-agentes, Skills, Workflows, assim como o contexto e a memória necessária para que a IA implemente corretamente o que é pedido são temas de curiosidade do atual projeto.

Apresentação didática do sistema de agentes (agentes, fluxos, memória, hooks e regras): `.claude/README.md`. Leia quando precisar explicar o sistema a alguém ou ter a visão do todo; para trabalhar, valem os arquivos que ele cita.

# Mapa do projeto

```
.
├── CLAUDE.md # ponto de entrada: propósito, mapa e importação das regras
├── .claude/ # configuração e contexto da IA
│ ├── README.md # apresentação didática do sistema de agentes, para quem chega
│ ├── settings.json # hooks e permissões do projeto
│ ├── agents/ # os seis agentes do time (gerente-de-produto, arquiteto, tester, escritor, gerente-de-qualidade, senso-critico)
│ ├── hooks/ # scripts dos hooks (contexto inicial, proteção de escrita, validação da memória)
│ ├── memoria/ # memória persistente (estado, decisões, impedimentos), lida no início da sessão
│ ├── quality/ # checklist de qualidade e esquema do parecer, usados pelo gerente-de-qualidade
│ ├── regras/ # regras que a IA deve seguir (importadas abaixo via @)
│ └── skills/<nome>/ # uma pasta por skill, cada uma com seu SKILL.md
└── docs/ # documentação do projeto, lida sob demanda
  ├── adr/ # registros de decisão de arquitetura (ADRs)
  ├── contracts/ # contratos de fronteira (OpenAPI e portas entre módulos), escritos pelo arquiteto; criada pelo /feature
  ├── execucoes/ # registro de cada execução do /feature, do /fundacao ou do /bugfix (commits, portões, mapa de testes), um arquivo por execução
  ├── produto/ # visão, backlog, specs e decisões de produto, escritos pelo gerente-de-produto; criada pelo /fundacao
  ├── referencias/ # referências técnicas do projeto, primeiro caminho para qualquer dúvida técnica; índice em README.md
  ├── senso-critico/ # relatórios SC-R-NNN do senso crítico (exame das propostas antes dos portões), com as respostas gravadas pelo orquestrador; criada pelo primeiro exame
  └── testes/ # por feature: especificação de testes (TA-*) do arquiteto e pareceres do gerente-de-qualidade; por bugfix: enquadramento do defeito (RG-*) e pareceres
```

# Regras

@.claude/regras/inviolaveis.md
@.claude/regras/metodo.md
@.claude/regras/memoria.md
@.claude/regras/referencias.md
