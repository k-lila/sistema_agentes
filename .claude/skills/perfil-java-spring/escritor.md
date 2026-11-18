# Perfil Java/Spring — escritor

Concretiza, para Java/Spring Boot, o que `.claude/agents/escritor.md` diz em termos gerais.
Leia junto com o `SKILL.md` desta pasta.

## Onde o escritor escreve

Código de produção em `src/main/java/`, configuração e recursos em `src/main/resources/`,
arquivos de build (ver `SKILL.md`), CI e README. Nunca em `src/test/`. Dependências de
escopo de teste (`<scope>test</scope>`, `testImplementation`) só na passagem `build` do modo
`fundacao`, conforme a ADR de perfil e ferramentas; fora dela, nunca.

**Arquivos de CI:** `.github/workflows/*.yml` (GitHub Actions, provedor padrão deste perfil;
a ADR pode escolher outro, e então vale o caminho que ela indicar). `Dockerfile` na raiz, só
se a ADR o adotar.

## Fundação (modo `fundacao`)

### Passagem `build`

- Wrapper versionado (`mvn -N wrapper:wrapper` ou `gradle wrapper`) e o build com o
  Spring Boot (parent ou plugin) e as dependências que a ADR adota.
- Um plugin ou configuração por ferramenta `FER-nn` do `qualidade.md` deste perfil, com os
  comandos que a ADR registra; o build não pode ignorar falhas delas.
- Dependências de teste da ADR (JUnit 5, AssertJ, Spring Boot Test, ArchUnit,
  Testcontainers, RestAssured etc.), declaradas aqui de uma vez.
- CI: um workflow que, em todo push e pull request, faz checkout, instala o JDK da ADR e
  roda o build completo com testes e as ferramentas `FER-nn`.
- Dockerfile (se adotado): build em múltiplos estágios, imagem de runtime só com JRE,
  usuário não root.

### Passagem `aplicacao`

- A classe `@SpringBootApplication` no pacote raiz da ADR, com `main` e nada mais.
- Os pacotes que as diretrizes da ADR definem, vazios ou só com `package-info.java`.
- `application.yml` mínimo; o perfil de teste não exige banco nem serviço externo, a menos
  que a ADR os adote.

## Documentação de API pública

- **Javadoc** em toda classe, interface e método público: o que faz, `@param`, `@return`,
  `@throws` e pré-condições.
- Geração: `./mvnw -B javadoc:javadoc` ou `./gradlew javadoc`, se a ADR de perfil adotar.

## Contrato HTTP

- Se a ADR adotar geração a partir do contrato (openapi-generator, gerador `spring` com
  `interfaceOnly`), implemente as interfaces geradas em vez de declarar as suas.
- Se o projeto gera a especificação pelo springdoc-openapi, as anotações (`@Operation`,
  `@ApiResponse`, `@Schema`) devem descrever fielmente o que o código faz. A especificação
  gerada serve para comparar com `docs/contracts/http/openapi.yaml`, não o substitui.
- Formato de erro: `ProblemDetail` (RFC 9457) quando o contrato adota `application/problem+json`.

## Convenções que tornam o código testável

- Injeção por construtor; sem `@Autowired` em campo.
- Relógio por `java.time.Clock` injetado; geradores de ID e aleatoriedade atrás de interfaces.
- Exceções tratadas de forma centralizada (`@RestControllerAdvice`).
- Configuração por `@ConfigurationProperties`, com variáveis de ambiente documentadas no README.
