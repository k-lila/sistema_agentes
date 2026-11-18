# Perfil Java/Spring — tester

Concretiza, para Java/Spring Boot, o que `.claude/agents/tester.md` diz em termos gerais.
Leia junto com o `SKILL.md` desta pasta.

## Onde o tester escreve

Tudo sob `src/test/`: código (`src/test/java/`), recursos e fixtures
(`src/test/resources/`), `application-test.yml`, scripts SQL de teste. Nunca arquivos de
build (ver `SKILL.md`).

## Ferramentas

JUnit 5 e AssertJ em todos os níveis; Mockito para dublês nas bordas; MockMvc ou RestAssured
para HTTP; Testcontainers para banco real; `spring-security-test` para segurança; ArchUnit para
testes estruturais; validador OpenAPI (ex.: `swagger-request-validator`) para conformidade com
o contrato. Só use as que a ADR de perfil adota e o build já configura.

## Níveis de teste

| O que se verifica | Nível | Como |
| --- | --- | --- |
| Comportamento de um endpoint visto de fora (status, corpo, erro) | aceitação | `@SpringBootTest` + MockMvc ou RestAssured |
| Persistência, queries, mapeamento JPA, migrações | integração | `@DataJpaTest` + Testcontainers (banco real, não H2, salvo ADR em contrário) |
| Segurança (quem pode o quê) | integração | `@SpringBootTest` / `@WebMvcTest` + `spring-security-test` |
| Serialização e validação de entrada | integração | `@WebMvcTest` |
| Regra de negócio isolada, cálculo, máquina de estados | unitário | JUnit 5 + AssertJ, dublês só nas bordas |
| Diretriz estrutural de ADR (camadas, dependências) | arquitetura | ArchUnit |
| Conformidade com o contrato HTTP | aceitação | validador OpenAPI sobre as respostas, se adotado |

## Modo `especificacao`

- Teste pela fronteira via HTTP (`@SpringBootTest` + MockMvc ou RestAssured), com corpo de
  requisição e resposta como JSON literal ou estrutura genérica (`Map`, `JsonNode`, JSONPath).
  Não importe DTOs, controllers nem services da feature: eles ainda não existem.
- Falha "por outro motivo", e portanto defeito seu: erro de compilação, contexto Spring que não
  sobe, fixture quebrada.
- **Teste estrutural (ArchUnit).** Configure a regra para falhar quando não houver classes a
  verificar: `failOnEmptyShould` ativo (padrão a partir do ArchUnit 1.0; não use
  `allowEmptyShould(true)`). Antes da implementação, o vermelho correto é a falha por regra
  vazia. Importe as classes do pacote raiz do projeto com `@AnalyzeClasses`.

## Modo `regressao`

No fluxo `/bugfix`, com o código integrado e defeituoso: as mesmas ferramentas do modo
`qualidade`, no nível mais baixo em que o defeito do enquadramento se manifesta (ver "Níveis
de teste"). Os tipos de produção existentes podem ser importados. Falha "por outro motivo", e
portanto defeito seu: erro de compilação, contexto Spring que não sobe, fixture quebrada.

## Modo `qualidade`

Com o código existindo: unidades internas (JUnit 5 + AssertJ, Mockito nas bordas), fatias do
Spring (`@WebMvcTest`, `@DataJpaTest`), integração com banco real (Testcontainers) e regressões.

## Rastreabilidade no código

```java
@Tag("rodada-especificacao")
class CadastroApiTest {

    @Test
    @DisplayName("TA-003 · cadastro com e-mail duplicado retorna 409")
    void cadastroComEmailDuplicado() { ... }
}
```

- Identificador no `@DisplayName` (`TA-nnn`, `TQ-nnn`, `RG-nnn` ou `IND-nnn`); tag da rodada com
  `@Tag("rodada-especificacao")`, `@Tag("rodada-regressao")` ou `@Tag("rodada-qualidade")`, na
  classe ou no método.
- Os identificadores são únicos no projeto (numeração global). Para achar o próximo `IND-*`:
  `grep -rhoE 'IND-[0-9]+' src/test | sort -t- -k2 -n | tail -1`.
- Mensagem de falha com `as(...)` / `describedAs(...)` do AssertJ quando o valor sozinho não
  explicar o que se esperava.
- Teste desativado é `@Disabled`; suposição artificial é `assumeTrue`. Nenhum dos dois para
  fazer um teste passar.
- Relógio por `java.time.Clock` injetado; nada de `Thread.sleep`.
