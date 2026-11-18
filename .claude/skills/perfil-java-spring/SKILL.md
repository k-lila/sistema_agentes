---
name: perfil-java-spring
description: Perfil de stack Java/Spring Boot. Reúne o que é específico dessa stack para os agentes do sistema (tester, escritor, arquiteto, gerente-de-qualidade) — build, estrutura de pastas, comandos, níveis e ferramentas de teste, ferramentas de qualidade e itens de checklist. Não é invocado diretamente: o orquestrador lê na ADR de perfil do projeto qual perfil usar e passa aos agentes o caminho desta pasta.
user-invocable: false
---

# Perfil de stack — Java/Spring Boot

Este perfil é material de consulta. Os agentes do sistema são independentes da stack: o que
eles dizem em termos gerais ("o arquivo de build", "a ferramenta de testes estruturais", "a
documentação de API pública") é concretizado aqui.

**Como é usado.** A ADR de perfil do projeto (criada pelo `/fundacao`) escolhe este perfil e
as ferramentas. No `/feature`, o orquestrador lê essa ADR na Etapa 0 e passa a cada agente o
caminho desta pasta. Cada agente lê este `SKILL.md` e o arquivo do próprio papel.

**Precedência.** Uma ADR aceita do projeto prevalece sobre este perfil: se a ADR escolher
Gradle em vez de Maven, ou Checkstyle em vez de PMD, vale a ADR.

## Arquivos por papel

| Arquivo | Quem lê | Conteúdo |
| --- | --- | --- |
| `tester.md` | tester | níveis de teste, ferramentas, rastreabilidade no código de teste, teste estrutural |
| `escritor.md` | escritor | documentação de API pública, geração a partir do contrato, convenções de código |
| `arquiteto.md` | arquiteto | contrato de módulo, verificação automática de contrato, ferramentas para a ADR de perfil |
| `qualidade.md` | gerente-de-qualidade | ferramentas exigidas e comandos, extensão do checklist, padrão de codificação segura da stack |

## Comum a todos os papéis

### Build

- Build com wrapper versionado no repositório: Maven (`./mvnw`) ou Gradle (`./gradlew`),
  conforme a ADR de perfil.
- **Arquivos de build:** `pom.xml`, `mvnw`, `mvnw.cmd`, `.mvn/**` (Maven) ou `build.gradle`,
  `build.gradle.kts`, `settings.gradle*`, `gradle.properties`, `gradlew`, `gradlew.bat`,
  `gradle/**` (Gradle), e o `.gitignore` (ver "Saída de build"). São do escritor; o tester
  nunca os edita.
- Versões de dependências e plugins fixas.

### Saída de build (`.gitignore`)

O que o build gera nunca entra no Git. O escritor, na passagem `build` do `/fundacao`,
acrescenta ao `.gitignore` as entradas da ferramenta que a ADR adota:

| Ferramenta | Entradas |
| --- | --- |
| Maven | `target/` |
| Gradle | `build/`, `.gradle/` |

Ferramenta adotada depois (por ADR) que gere arquivos fora dessas pastas traz a entrada
dela no mesmo commit que a configura.

O `.gitignore` começa com o **bloco do sistema de agentes** (memória local e worktrees),
marcado por comentário: ele não é editado nem removido. As entradas do projeto vão abaixo
dele. Arquivos de IDE e do sistema operacional são do ambiente de cada pessoa
(`core.excludesFile`), não do projeto.

Verificação, no `/fundacao` (Etapa 6) e em toda revisão (`JSP-10` de `qualidade.md`):

- depois do build completo, `git status --porcelain` não lista nada gerado pelo build;
- `git ls-files target build .gradle` não devolve nada;
- `git check-ignore .claude/memoria/task.json .claude/memoria/roadmap.json .claude/worktrees/x`
  lista os três caminhos (o bloco do sistema continua valendo; um caminho ausente da saída
  é um bloco alterado).

### Estrutura de pastas

| Conteúdo | Caminho |
| --- | --- |
| Código de produção | `src/main/java/` |
| Configuração e recursos de produção | `src/main/resources/` (`application.yml`, `application-<perfil>.yml`, migrações) |
| Código de teste | `src/test/java/` |
| Recursos de teste | `src/test/resources/` (`application-test.yml`, fixtures, scripts SQL de teste) |

Arquivo de teste por convenção de nome: `*Test.java` (unitário e fatias), `*IT.java`
(integração com Failsafe, se adotado).

### Comandos

| Ação | Maven | Gradle |
| --- | --- | --- |
| Build completo com testes | `./mvnw -B verify` | `./gradlew build` |
| Só testes | `./mvnw -B test` | `./gradlew test` |
| Testes de uma rodada | `./mvnw -B test -Dgroups=<tag da rodada>` (`rodada-especificacao`, `rodada-regressao` ou `rodada-qualidade`) | `./gradlew test` com filtro de tag configurado |
| Um teste | `./mvnw -B test -Dtest=Classe#metodo` | `./gradlew test --tests 'Classe.metodo'` |

Os comandos definidos na ADR de perfil prevalecem sobre esta tabela.

### Pré-requisitos de ambiente

O que a máquina precisa ter para a base deste perfil ser criada e verificada. O orquestrador
do `/fundacao` roda estes comandos logo depois de a ADR de base ser aceita, antes de qualquer
build; só valem os itens que a ADR adota.

| Item | Necessário quando | Como conferir |
| --- | --- | --- |
| JDK na versão da ADR | sempre | `java -version` |
| Maven ou Gradle instalado | só na fundação, para gerar o wrapper | `mvn -v` ou `gradle -v` |
| Acesso ao repositório de dependências | sempre | `curl -sI https://repo.maven.apache.org/maven2/` responde `200` |
| Docker em execução | a ADR adota Testcontainers ou Dockerfile | `docker info` |
| Acesso à base de vulnerabilidades (NVD) | sempre (FER-06) | `curl -sI https://nvd.nist.gov/` responde; sem chave de API (`NVD_API_KEY`) a primeira execução é lenta e pode ser limitada |

Item que falta não se contorna no build (pular testes, desligar a ferramenta): é falha de
ambiente e volta ao usuário.

