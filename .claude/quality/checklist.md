# Checklist de qualidade — núcleo

- **Versão:** 2.0.0
- **Data:** 2026-11-11
- **Usado por:** agente `gerente-de-qualidade`
- **Complemento:** o arquivo `qualidade.md` do perfil de stack do projeto (ferramentas exigidas,
  leitura dos itens do núcleo na stack, itens específicos e padrão de codificação segura)
- **Alterações:** somente com aprovação humana (ver "Histórico")

## Referências e versões

| Referência | Versão adotada |
| --- | --- |
| ISO/IEC 25010 | 2023 |
| ISO/IEC 5055 | 2021 |
| OWASP Top 10 | 2025 |
| OWASP ASVS | 5.0.0, nível L2 (L3 onde ADR definir) |
| CWE Top 25 | 2025 |
| Padrão de codificação segura da stack | definido pelo perfil de stack |
| Google Engineering Practices (code review) | site público, repositório arquivado em 2025-11 |

## Como ler este checklist

Cada item tem: identificador, o que verificar, referência e severidade padrão (B = bloqueante, R = recomendado, N = nit). A severidade padrão pode ser ajustada pelo agente apenas nos casos previstos no prompt (por exemplo, trecho comprovadamente inalcançável por entrada externa). Os itens sempre bloqueantes definidos no prompt prevalecem sobre este arquivo.

Os itens estão escritos sem supor uma stack. O perfil de stack diz como cada item se lê na stack do projeto (construções, anotações, regras do padrão de codificação) e acrescenta itens próprios. Um item do perfil tem a mesma força de um item do núcleo.

---

## 0. Ferramentas exigidas

Definidas pelo perfil de stack (`qualidade.md`, IDs `FER-nn`), com comandos que a ADR de perfil pode redefinir. Todas devem estar configuradas no build do projeto. Ausência ou falha de execução bloqueia a revisão.

---

## 1. Correção

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| COR-01 | Cada critério de aceitação da demanda está implementado | Demanda; 25010 adequação funcional/completude | B |
| COR-02 | Casos de borda e caminhos de erro previstos na demanda estão tratados | Demanda; 25010 adequação funcional/correção | B |
| COR-03 | Nenhuma exceção ou erro é engolido (captura vazia, só log, retorno silencioso de valor nulo) | CWE-390; A10:2025 | R |
| COR-04 | Falha não deixa o sistema "aberto": erro em checagem de segurança nega por padrão | A10:2025; CWE-636 | B |
| COR-05 | Estado permanece consistente após falha (transação, compensação, rollback) | 25010 confiabilidade/tolerância a falhas; A10:2025 | B |
| COR-06 | Ausência de valor tratada na origem (tipo opcional, validação); sem capturar erro de referência nula | CWE-476 | R |
| COR-07 | Recursos (arquivos, conexões, locks) liberados de forma garantida, mesmo em caso de erro | CWE-404 | R |
| COR-08 | Acesso concorrente a estado compartilhado é sincronizado ou imutável | CWE-362 | B |
| COR-09 | Valores monetários usam tipo decimal exato; nunca ponto flutuante | 25010 adequação funcional/correção | B |
| COR-10 | Datas e horas com fuso explícito; sem tipos de data legados ou ambíguos | 25010 adequação funcional/correção | R |

## 2. Design

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| DES-01 | Camadas e direção das dependências seguem as ADRs (ex.: domínio não depende de web nem de persistência) | ADR; 25010 manutenibilidade/modularidade | B |
| DES-02 | Sem dependência circular entre pacotes ou módulos | CWE-1047; 5055 | B |
| DES-03 | Cada unidade (classe, módulo) tem uma responsabilidade clara; serviço não acumula regras de domínios diferentes | 25010 manutenibilidade/modularidade | R |
| DES-04 | Regra de negócio fica no domínio ou serviço, não na camada de entrada nem na de persistência | ADR; 25010 manutenibilidade/analisabilidade | R |
| DES-05 | Contratos públicos (API, eventos, objetos de transferência) estão versionados ou compatíveis com consumidores existentes | ADR; 25010 compatibilidade/interoperabilidade | B |
| DES-06 | Decisão nova de arquitetura sem ADR que a cubra | ADR (lacuna) → destino Arquiteto | R |
| DES-07 | Acoplamento excessivo: unidade com dependências externas demais | CWE-1048; 5055 | R |

## 3. Legibilidade e manutenibilidade

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| LEG-01 | Nomes revelam intenção e seguem a convenção definida em ADR | ADR; 25010 manutenibilidade/analisabilidade | R |
| LEG-02 | Funções curtas e com complexidade controlada (limites da ferramenta de estilo configurada) | CWE-1121; 5055 | R |
| LEG-03 | Sem duplicação de lógica (copiar e colar) | CWE-1041; 5055 | R |
| LEG-04 | Sem código morto nem código comentado | CWE-561; CWE-1085; 5055 | R |
| LEG-05 | Sem números e strings mágicos repetidos; constantes nomeadas | CWE-1052; 5055 | N |
| LEG-06 | Comentários explicam o porquê, não repetem o código; nenhum comentário desatualizado | 25010 manutenibilidade/analisabilidade | N |
| LEG-07 | Documentação de API pública de módulo presente, quando exigida por ADR | ADR | R |

## 4. Testes

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| TES-01 | Todos os testes passam | 25010 adequação funcional/correção | B |
| TES-02 | Cada critério de aceitação tem ao menos um teste que falharia se ele quebrasse | Demanda; 25010 manutenibilidade/testabilidade | B |
| TES-03 | Cobertura de linhas e ramos ≥ 80% no código alterado ou adicionado | 25010 manutenibilidade/testabilidade | R |
| TES-04 | Caminhos de erro e regras de segurança têm teste | 25010 confiabilidade; ASVS v5.0.0 | B |
| TES-05 | Sem testes inúteis: sem asserção significativa, só verificação de dublê, espelho da implementação | 25010 manutenibilidade/testabilidade | R |
| TES-06 | Sem testes de caminhos impossíveis (estados inalcançáveis pelo código, tipos ou validações) | 25010 manutenibilidade/testabilidade | R |
| TES-07 | Tipo de teste adequado: unitário para regra isolada; integração para entrada HTTP, persistência e segurança (níveis do perfil) | 25010 manutenibilidade/testabilidade | R |
| TES-08 | Testes independentes da ordem de execução e sem dependência de relógio, rede ou dados externos não controlados | 25010 confiabilidade | R |
| TES-09 | Nenhum teste desativado sem justificativa ligada a uma issue | 25010 manutenibilidade/testabilidade | R |

## 5. Segurança (ASVS 5.0.0 L2)

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| SEG-01 | Todo endpoint e operação sensível tem checagem de autorização | ASVS V8; CWE-862; A01:2025 | B |
| SEG-02 | Acesso a recurso por id verifica se o usuário tem direito àquele recurso (sem IDOR) | ASVS V8; CWE-639; A01:2025 | B |
| SEG-03 | Funções críticas exigem autenticação | ASVS V6; CWE-306; A07:2025 | B |
| SEG-04 | Consultas parametrizadas; nenhuma consulta montada por concatenação com entrada externa | ASVS V1; CWE-89; A05:2025 | B |
| SEG-05 | Sem execução de comando de sistema ou de linguagem de expressão com entrada externa | ASVS V1; CWE-78; CWE-917; A05:2025 | B |
| SEG-06 | Entrada validada na fronteira e codificada na saída | ASVS V2; CWE-20; A05:2025 | B |
| SEG-07 | Caminhos de arquivo canonizados e restritos ao diretório permitido | ASVS V5; CWE-22 | B |
| SEG-08 | Upload valida tipo, tamanho e destino | ASVS V5; CWE-434 | B |
| SEG-09 | Sem desserialização de dados não confiáveis (serialização nativa da plataforma; tipagem polimórfica aberta) | ASVS V1; CWE-502; A08:2025 | B |
| SEG-10 | Nenhum segredo, senha, token ou chave no código ou em configuração versionada | ASVS V13; CWE-798 | B |
| SEG-11 | Senhas com hash adaptativo (BCrypt, Argon2 ou PBKDF2) | ASVS V6; CWE-916; A04:2025 | B |
| SEG-12 | Algoritmos e modos criptográficos atuais; sem MD5/SHA-1 para segurança, sem ECB | ASVS V11; CWE-327; A04:2025 | B |
| SEG-13 | Tokens JWT: assinatura e algoritmo verificados, expiração curta, claims validadas | ASVS V9; CWE-347 | B |
| SEG-14 | Fluxos OAuth/OIDC seguem o ASVS V10 (PKCE, state, validação de redirect) | ASVS V10 | B |
| SEG-15 | Proteção CSRF ativa, salvo API stateless com token em header (decisão registrada em ADR) | ASVS V3; CWE-352 | B |
| SEG-16 | Requisição a URL externa a partir de entrada do usuário passa por lista de permissão | ASVS V1; CWE-918; A01:2025 | B |
| SEG-17 | Resposta de erro não expõe stack trace, SQL ou dados internos | ASVS V16; CWE-209; A02:2025 | B |
| SEG-18 | Eventos de segurança são registrados (login, falha de autorização, mudança de permissão) | ASVS V16; CWE-778; A09:2025 | R |
| SEG-19 | Logs não contêm senhas, tokens nem dados pessoais; entrada do usuário neutralizada antes de logar | ASVS V16; CWE-532; CWE-117 | B |
| SEG-20 | Objeto de persistência não é exposto diretamente na API nem preenchido em massa a partir da requisição | ASVS V2; CWE-915 | B |
| SEG-21 | Dependências sem vulnerabilidade conhecida alta ou crítica; versões fixas; bibliotecas mantidas | CWE-1395; CWE-1104; A03:2025 | B |
| SEG-22 | Limites de tamanho e taxa em operações caras ou públicas | ASVS V2; CWE-770 | R |

## 6. Desempenho

Avaliar apenas quando houver risco plausível.

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| DSP-01 | Sem consultas N+1 (carregamento sob demanda dentro de laço) | 25010 eficiência de desempenho/utilização de recursos | R |
| DSP-02 | Listagens paginadas; nenhuma consulta sem limite em tabela que cresce | CWE-770; 25010 eficiência/capacidade | R |
| DSP-03 | Complexidade algorítmica adequada ao volume esperado | CWE-407; 5055 | R |
| DSP-04 | Sem chamada remota ou consulta ao banco dentro de laço quando evitável | 25010 eficiência/comportamento no tempo | R |
| DSP-05 | Índices previstos na migração para colunas usadas em filtros novos | 25010 eficiência/comportamento no tempo | R |

## 7. Idiomas da stack

Definidos pelo perfil de stack (`qualidade.md`, seção "Itens específicos da stack"). No parecer, use o pilar `idiomas_da_stack`.

## 8. Configuração e infraestrutura

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| CFG-01 | Segredos vêm de variáveis de ambiente ou cofre, nunca de arquivo de configuração versionado | ASVS V13; CWE-798; A02:2025 | B |
| CFG-02 | Perfis de ambiente separados; configuração de desenvolvimento não vaza para produção (debug, consoles de banco, logs verbosos) | ASVS V13; CWE-489; A02:2025 | B |
| CFG-03 | Endpoints de administração e monitoramento expostos só o necessário e protegidos | ASVS V13; CWE-200; A02:2025 | B |
| CFG-04 | CORS restrito às origens previstas em ADR; sem `*` com credenciais | ASVS V3; CWE-942; A02:2025 | B |
| CFG-05 | Geração automática de esquema não altera produção; migrações versionadas | ADR; 25010 confiabilidade | B |
| CFG-06 | Dockerfile: imagem base com versão fixa, usuário não root, sem segredos em camadas | CWE-250; A03:2025; A08:2025 | B |
| CFG-07 | Pipeline de CI executa as ferramentas exigidas pelo perfil | ADR; 25010 manutenibilidade | R |
| CFG-08 | Versões de dependências e plugins fixas no build | A03:2025; CWE-1395 | R |

## 9. Documentação

| ID | Verificar | Referência | Sev. |
| --- | --- | --- | --- |
| DOC-01 | Mudança de contrato de API refletida na especificação (OpenAPI ou equivalente) | DES-05; 25010 compatibilidade | B |
| DOC-02 | README e instruções de execução atualizados quando a mudança altera configuração, variáveis de ambiente ou comandos | Google eng-practices (documentação); 25010 manutenibilidade | R |
| DOC-03 | Documentação não contradiz o código | 25010 manutenibilidade/analisabilidade | R |
| DOC-04 | Nenhum segredo, credencial real ou dado pessoal em documentação ou exemplos | CWE-798; CWE-200 | B |

---

## Histórico

| Versão | Data | Mudança | Aprovado por |
| --- | --- | --- | --- |
| 1.0.0 | 2026-11-10 | Versão inicial (Java/Spring) | — |
| 2.0.0 | 2026-11-11 | Núcleo independente de stack: seções 0 e 7, regras CERT Java e construções da stack passaram para o perfil `perfil-java-spring` (`qualidade.md`) | usuário (TASK-002, A-1) |
