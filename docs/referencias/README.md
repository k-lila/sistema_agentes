# Índice das referências

Referências técnicas do projeto. A regra de uso está em `.claude/regras/referencias.md`: diante de uma dúvida técnica, comece por aqui, escolha o documento pelo que ele responde e leia só a seção pertinente.

Dono da pasta: o orquestrador. Toda referência nova ou renomeada ganha uma entrada neste índice no mesmo passo.

| Documento | Responde a | Data |
| --- | --- | --- |
| `orquestracao-agentes.md` | Como montar e operar o sistema de agentes no Claude Code: contexto, CLAUDE.md, subagentes, skills, hooks, permissões, workflows e a documentação que orienta os agentes | 2026-10-14 |
| `qualidade-de-codigo.md` | Que normas definem qualidade e segurança de código, o que cada uma exige e como citá-las num achado de revisão | 2026-11-10 |

## `orquestracao-agentes.md`

Guia de 1.650 linhas: localize a seção com `Grep` pelo título e leia só o trecho. O próprio guia tem um "Mapa de consulta" perto do fim. As afirmações sobre o Claude Code vêm da documentação oficial de 14 de outubro de 2026 e podem ter mudado.

| Dúvida | Seção |
| --- | --- |
| O que carrega no contexto e quanto custa | 2. Fundamentos: contexto é o recurso escasso |
| CLAUDE.md, imports com `@`, regras por caminho, memória automática | 3. CLAUDE.md, regras e memória automática |
| Frontmatter de subagente, o que ele recebe ao nascer, como acionar | 4. Subagentes: os especialistas |
| Estrutura de uma skill, frontmatter, divulgação progressiva | 5. Skills: os manuais |
| Comando que orquestra agentes, argumentos, boas práticas | 6. Slash commands: a partitura da orquestração |
| Eventos de hook, como o hook responde, onde configurar | 7. Hooks: os fiscais automáticos |
| Regras allow, ask e deny, sintaxe, modos de permissão | 8. Permissões e configurações: o que cada agente pode fazer |
| MCP e empacotamento em plugin | 9. MCP e plugins: conexão externa e empacotamento |
| Plan mode, worktrees, agent teams, paralelismo | 10. Plan mode, worktrees, agent teams e paralelismo |
| Padrões de fluxo entre agentes (cadeia, revisor, paralelo) | 11. Padrões de workflow de agentes |
| Formato e ciclo de vida de ADR | 12. ADRs: a memória das decisões |
| Spec, escopo, requisitos não funcionais, questões em aberto | 13. Escopo, specs, requisitos não funcionais e questões em aberto |
| Convenções, estratégia de testes, definição de pronto | 14. Convenções, testes, definição de pronto e documentos de apoio |
| Regras verificadas por teste ou ferramenta (ArchUnit, migrations) | 15. Regras executáveis: documentação que se verifica sozinha |
| Estado da tarefa em curso | 16. Arquivos de contexto voláteis: onde estamos |
| Estrutura de pastas e quem é dono de cada caminho | 17. Estrutura de pastas e protocolo de propriedade |
| Exemplo de vários agentes numa tarefa e do fluxo completo | 18. Vários agentes, uma tarefa; 19. Orquestração completa |
| Roadmap, rodadas, automação e portões humanos | 20. Roadmaps; 21. Executando o roadmap |
| Erros comuns e limites do que as fontes decidem | 22. Armadilhas e boas práticas |
| Fontes originais | 23. Referências |

## `qualidade-de-codigo.md`

Relatório de 220 linhas, em paráfrase. As normas ISO são pagas e foram consultadas só por prévias e resumos públicos: para citar um trecho literal, vá ao original.

| Dúvida | Seção |
| --- | --- |
| O que é qualidade e como classificar um achado | 1. ISO/IEC 25010:2023 |
| Como medir qualidade no código, base da análise estática | 2. ISO/IEC 5055:2021 |
| Onde estão os maiores riscos de segurança | 3. OWASP Top 10:2025 |
| Que requisito de segurança deve ser cumprido | 4. OWASP ASVS 5.0 |
| Como revisar código com foco em segurança | 5. OWASP Code Review Guide |
| Qual é exatamente a fraqueza e como rotulá-la | 6. CWE e CWE Top 25 (MITRE) |
| Regra de codificação segura em Java | 7. SEI CERT Oracle Coding Standard for Java |
| Quando aprovar, severidade de comentário, impasses | 8. Google Engineering Practices |
| Qual referência usar para qual pergunta e como citar | Síntese: o papel de cada referência no agente revisor |
