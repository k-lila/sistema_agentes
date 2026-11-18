# Perfil Java/Spring — gerente-de-qualidade

Concretiza, para Java/Spring Boot, o checklist núcleo (`.claude/quality/checklist.md`) e o que
`.claude/agents/gerente-de-qualidade.md` diz em termos gerais. Leia junto com o `SKILL.md`
desta pasta.

- **Versão da extensão:** 1.3.0
- **Alterações:** somente com aprovação humana, como o checklist núcleo.

## Ferramentas exigidas

Todas devem estar configuradas no build do projeto pela fundação. Ausência ou falha de execução
bloqueia a revisão (ver roteamento de ferramenta no agente). Os comandos podem ser redefinidos
pela ADR de perfil.

| ID | Ferramenta | Finalidade | Comando padrão (Maven / Gradle) |
| --- | --- | --- | --- |
| FER-01 | Build com wrapper | Compilar e empacotar | `./mvnw -B verify` / `./gradlew build` |
| FER-02 | JUnit 5 + Spring Boot Test | Testes unitários e de integração | incluído em FER-01 |
| FER-03 | JaCoCo | Cobertura de linhas e ramos | `./mvnw -B verify` com relatório JaCoCo / `./gradlew jacocoTestReport` |
| FER-04 | SpotBugs + FindSecBugs | Análise estática de defeitos e segurança | `./mvnw -B spotbugs:check` / `./gradlew spotbugsMain` |
| FER-05 | PMD ou Checkstyle (um deles, definido na ADR de perfil) | Estilo, complexidade, código morto, duplicação | `./mvnw -B pmd:check` ou `checkstyle:check` / `./gradlew pmdMain` ou `checkstyleMain` |
| FER-06 | OWASP Dependency-Check | Dependências com vulnerabilidades conhecidas | `./mvnw -B org.owasp:dependency-check-maven:check` / `./gradlew dependencyCheckAnalyze` |
| FER-07 | Verificação de contrato (validador OpenAPI nos testes, ou springdoc + openapi-diff) | Conformidade da implementação com `docs/contracts/http/openapi.yaml` | o comando que a ADR registrar; com validador nos testes, incluído em FER-01 |

A FER-07 só é exigida quando uma ADR aceita adota a verificação automática de contrato. Sem
essa ADR, ela não entra na lista `ferramentas` do parecer nem conta como ausente: a
conformidade é conferida por leitura, com achados `inferido`.

A meta de cobertura do núcleo (TES-03) é medida pelo JaCoCo (FER-03). O JaCoCo mede o projeto
inteiro; a meta vale para o **código alterado ou adicionado**. Para obtê-la, liste as classes de
produção tocadas no escopo (`git diff --name-only <escopo> -- src/main/java`) e some, só para
elas, as linhas e os ramos cobertos e perdidos do relatório (`target/site/jacoco/jacoco.csv`,
colunas `LINE_*` e `BRANCH_*`, ou `build/reports/jacoco/` no Gradle). No parecer, use
`cobertura.escopo: "codigo_alterado"`. A granularidade é a classe: uma classe grande tocada
em poucas linhas entra inteira, e isso se diz no resumo quando distorcer o número. Os testes de cada rodada
se filtram pelas tags `rodada-especificacao`, `rodada-regressao` (no `/bugfix`) e `rodada-qualidade`.

## Padrão de codificação segura da stack

**SEI CERT Oracle Coding Standard for Java** (edição do wiki SEI). Ignore as regras ligadas a
SecurityManager e applets. Cite como `<REGRA>-J` (ex.: `ERR00-J`), com o tipo de referência
`padrao_da_stack` no parecer. Só cite regras que você sabe que existem e correspondem ao
problema.

## Como os itens do núcleo se leem nesta stack

| Item do núcleo | Em Java/Spring | Regra CERT |
| --- | --- | --- |
| COR-03 | `catch` vazio, só `log`, `return null` silencioso | ERR00-J |
| COR-06 | sem `catch (NullPointerException)`; `Optional` como retorno, validação na entrada | ERR08-J |
| COR-07 | try-with-resources ou `finally` | FIO04-J |
| COR-08 | `synchronized`, tipos de `java.util.concurrent`, imutabilidade | VNA00-J; LCK07-J |
| COR-09 | `BigDecimal` para dinheiro; nunca `float`/`double` | — |
| COR-10 | `Instant`, `ZonedDateTime`, `OffsetDateTime`; nada de `java.util.Date` novo | — |
| LEG-02 | limites do PMD ou do Checkstyle configurado (FER-05) | — |
| LEG-07 | Javadoc em APIs públicas de módulo | — |
| TES-07 | unitário com JUnit 5 + AssertJ; integração com `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`, Testcontainers (ver `tester.md`) | — |
| TES-09 | `@Disabled` sem justificativa ligada a uma issue | — |
| SEG-04 | SQL, JPQL ou HQL montado por concatenação; use parâmetros nomeados ou Criteria | IDS00-J |
| SEG-05 | `Runtime.exec`/`ProcessBuilder` ou SpEL com entrada externa | IDS07-J |
| SEG-06 | `@Valid` e Bean Validation nos DTOs de entrada | — |
| SEG-07 | `Path.normalize()` / `toRealPath()` e verificação do prefixo | FIO16-J |
| SEG-09 | serialização nativa do Java; Jackson com tipagem polimórfica aberta (`activateDefaultTyping`, `@JsonTypeInfo(use = CLASS)`) | SER12-J |
| SEG-10 | segredos em código ou em `application*.yml` versionado | MSC03-J |
| SEG-11 | `PasswordEncoder` com BCrypt, Argon2 ou PBKDF2 | — |
| SEG-17 | stack trace ou SQL na resposta; use `ProblemDetail` sem detalhes internos | ERR01-J |
| SEG-20 | entidade JPA exposta na API ou preenchida em massa a partir do request | — |
| DSP-01 | N+1 por lazy loading em laço; use fetch join, `@EntityGraph` ou projeção | — |
| DSP-02 | `findAll()` sem `Pageable` em tabela que cresce | — |
| CFG-01 | segredos em `application.yml` versionado | — |
| CFG-02 | H2 console, `debug=true`, logs verbosos fora do perfil de desenvolvimento | — |
| CFG-03 | endpoints do Actuator expostos além do necessário ou sem proteção | — |
| CFG-05 | `spring.jpa.hibernate.ddl-auto` diferente de `validate`/`none` em produção; migrações com Flyway ou Liquibase | — |

## Itens específicos da stack (seção "Idiomas da stack" do parecer)

Use o pilar `idiomas_da_stack` no parecer.

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| JSP-01 | Injeção por construtor; sem `@Autowired` em campo | ADR; 25010 manutenibilidade/testabilidade | R |
| JSP-02 | `@Transactional` em método público chamado de fora da classe (não há proxy em autochamada nem em método privado) | 25010 confiabilidade | B |
| JSP-03 | `@Transactional(readOnly = true)` em leituras; fronteira transacional na camada de serviço | ADR; 25010 eficiência | R |
| JSP-04 | Exceções tratadas de forma centralizada (`@ControllerAdvice`) com respostas padronizadas | ADR; ERR01-J | R |
| JSP-05 | `equals` e `hashCode` definidos juntos e coerentes; entidades JPA não usam campos mutáveis gerados no `hashCode` | MET09-J | R |
| JSP-06 | Campos com a menor visibilidade possível; objetos de valor imutáveis (`record`, `final`) | OBJ01-J; 25010 manutenibilidade | N |
| JSP-07 | `Optional` só como retorno; nunca como campo ou parâmetro | 25010 manutenibilidade/analisabilidade | N |
| JSP-08 | Exceções em `@Async` e em listeners tratadas; não se perdem silenciosamente | ERR00-J; A10:2025 | R |
| JSP-09 | `spring.jpa.open-in-view` desativado, salvo decisão em ADR | ADR; 25010 eficiência | R |
| JSP-10 | Nenhuma saída de build rastreada e o bloco do sistema de agentes do `.gitignore` preservado, pelos comandos de "Saída de build" do `SKILL.md` deste perfil | `SKILL.md` do perfil, "Saída de build"; 25010 manutenibilidade | B |

## Verificação de contrato

Se a ADR adotar validação automática (validador OpenAPI nos testes, ou comparação da
especificação gerada pelo springdoc-openapi com `docs/contracts/http/openapi.yaml`), registre o
resultado como a ferramenta `FER-07`.

## Manutenção

Na tarefa `atualizar-checklist`, verifique também mudanças relevantes no SEI CERT Java
(wiki.sei.cmu.edu) e proponha o diff deste arquivo junto com o do núcleo.

## Histórico

| Versão | Data | Mudança | Aprovado por |
| --- | --- | --- | --- |
| 1.0.0 | 2026-11-11 | Extraído do checklist 1.0.0 (seções 0 e 7 e itens específicos) | usuário (TASK-002, A-1) |
| 1.1.0 | 2026-11-11 | FER-07: verificação de contrato, exigida só quando adotada por ADR | usuário (TASK-003, A-1) |
| 1.2.0 | 2026-11-11 | Como medir a cobertura do código alterado a partir do relatório do JaCoCo | usuário (TASK-007, A-1) |
| 1.2.1 | 2026-11-16 | Tag `rodada-regressao`, do fluxo `/bugfix`, entre as tags de rodada | usuário (TASK-010, A-3) |
| 1.3.0 | 2026-11-17 | JSP-10: saída de build fora do Git e bloco do sistema do `.gitignore` preservado | usuário (TASK-012, A-1) |
