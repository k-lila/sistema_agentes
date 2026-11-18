# Perfil Java/Spring — arquiteto

Concretiza, para Java/Spring Boot, o que `.claude/agents/arquiteto.md` diz em termos gerais.
Leia junto com o `SKILL.md` desta pasta.

## Contrato de módulo

Em `docs/contracts/modulos/<modulo>.md`, a porta entre módulos é a assinatura da interface Java,
sem implementação:

```java
public interface ConsultaDePedidos {
    /** Pedido pelo id; vazio se não existir. Somente leitura, sem transação própria. */
    Optional<PedidoResumo> porId(PedidoId id);
}
```

Junto da assinatura, em texto: significado de cada método, pré-condições, exceções que pode
lançar (tipos de exceção do domínio) e garantias (idempotência, transação).

## Verificação automática de contrato

Duas formas, a decidir em ADR:

- validador OpenAPI aplicado às respostas nos testes de aceitação (ex.:
  `swagger-request-validator-mockmvc` ou o filtro do RestAssured);
- comparação da especificação gerada pelo springdoc-openapi com `docs/contracts/http/openapi.yaml`
  (ex.: openapi-diff no build).

## Teste estrutural

As diretrizes verificáveis de ADR (camadas, dependências entre pacotes) viram `TA-*` de nível
`arquitetura`, implementados com ArchUnit. A regra falha quando não há classes a verificar
(ver `tester.md`), e esse é o vermelho esperado antes da implementação.

## Ferramentas para a ADR de perfil

A ADR de perfil (no `/fundacao`) escolhe e fixa: Maven ou Gradle; JUnit 5, AssertJ, Mockito;
Testcontainers; ArchUnit; JaCoCo; SpotBugs + FindSecBugs; PMD ou Checkstyle; OWASP
Dependency-Check; validador OpenAPI ou springdoc + openapi-diff; e os comandos de cada uma. A
lista de ferramentas que o gerente-de-qualidade exige está em `qualidade.md`.
