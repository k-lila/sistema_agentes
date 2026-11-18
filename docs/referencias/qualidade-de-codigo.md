# Referências sobre qualidade de código — relatório para o agente revisor

Nov 10, 2026 · @klila

Oito referências cobrem o que um agente revisor de código precisa: duas normas ISO definem o vocabulário de qualidade, cinco fontes abertas (três da OWASP, o CWE da MITRE e o SEI CERT) dão requisitos verificáveis de segurança e confiabilidade, e o guia do Google define o procedimento e o critério de aprovação.

As fontes abertas foram lidas nas páginas oficiais. As normas ISO/IEC 25010 e 5055 são pagas: delas foram consultados apenas prévias oficiais, o sumário de mudanças e resumos públicos. Tudo aqui é paráfrase; para citar trechos literais no prompt do agente, consulte o original.

## 1. ISO/IEC 25010:2023 — modelo de qualidade de produto

Define o vocabulário: nove características de qualidade, cada uma dividida em subcaracterísticas. Não traz métricas nem limites; é uma taxonomia para especificar requisitos, critérios de aceite e avaliação.

| Característica | Subcaracterísticas | Avaliável na revisão de código? |
| --- | --- | --- |
| Adequação funcional | completude, correção, pertinência | Em parte, com testes executados |
| Eficiência de desempenho | comportamento no tempo, uso de recursos, capacidade | Só riscos (N+1, algoritmo); medir exige execução |
| Compatibilidade | coexistência, interoperabilidade | Pouco; contratos de API sim |
| Capacidade de interação | reconhecimento de adequação, aprendizado, operabilidade, proteção contra erro do usuário, engajamento, inclusividade, assistência, autodescrição | Pouco; exige usuários |
| Confiabilidade | ausência de falhas, disponibilidade, tolerância a falhas, recuperabilidade | Sim: tratamento de erro, recursos, concorrência |
| Segurança (security) | confidencialidade, integridade, não repúdio, responsabilização, autenticidade, resistência | Sim, em grande parte |
| Manutenibilidade | modularidade, reusabilidade, analisabilidade, modificabilidade, testabilidade | Sim: território natural da revisão |
| Flexibilidade | adaptabilidade, escalabilidade, instalabilidade, substituibilidade | Em parte (configuração, acoplamento) |
| Segurança (safety) | restrição operacional, identificação de risco, falha segura, alerta de perigo, integração segura | Raramente, fora de sistemas críticos |

O que mudou de 2011 para 2023, segundo o próprio prefácio da norma:

- Safety entrou como nona característica.
- Usabilidade virou capacidade de interação; portabilidade virou flexibilidade.
- Entraram inclusividade, autodescrição, resistência e escalabilidade; maturidade virou ausência de falhas.
- O modelo de qualidade em uso saiu para a ISO/IEC 25019, e a visão geral de uso dos modelos para a ISO/IEC 25002.

Para o agente: use as características como rótulos dos achados e declare, em cada uma, se foi verificada, inferida ou não é avaliável no nível do código. Ao citar, nomeie a edição ("25010:2023"); muito material online ainda descreve o modelo de 2011, com oito características.

Fontes: [prévia oficial da norma (VDE)](https://www.vde-verlag.de/iec-normen/preview-pdf/info_isoiec25010{ed2.0}en.pdf), [arc42 — lista de subcaracterísticas](https://quality.arc42.org/articles/q42-for-iso-users/), [arc42 — mudanças de 2023](https://quality.arc42.org/articles/iso-25010-update-2023).

## 2. ISO/IEC 5055:2021 — medidas automatizadas de qualidade de código

É a ponte entre o modelo da 25010 e o código: mede quatro características (segurança, confiabilidade, eficiência de desempenho, manutenibilidade) contando, no código-fonte, ocorrências de fraquezas graves. Nasceu no consórcio CISQ, passou pela OMG como especificação ASCQM e virou norma ISO em 2021.

O que importa:

- **Medida estrutural, não comportamental.** A 25023 mede o software rodando; a 5055 mede o código antes de rodar. É a norma que mais se parece com o trabalho de um revisor.
- **Cada medida é uma lista de CWEs.** Exemplos do sumário da norma: código morto (CWE-561), duplicação por copiar e colar (CWE-1041), dependências circulares entre módulos (CWE-1047), arquivo grande demais (CWE-1080), literais fixos em excesso (CWE-1052), código comentado em excesso (CWE-1085), complexidade algorítmica (CWE-407), condição de corrida (CWE-366), divisão por zero (CWE-369).
- **Independente de linguagem.** As ferramentas que a implementam trazem regras específicas por linguagem e agregam os resultados por característica.
- **Pensada para contrato e aceite.** Serve para fixar metas de qualidade interna e acompanhar a evolução entre versões.

Para o agente: a 5055 dá identificadores precisos (CWE-xxx) para achados de manutenibilidade e confiabilidade, onde a 25010 só dá o nome da característica. Boa parte dessas regras é mecânica e cabe a uma ferramenta de análise estática; o agente confere e interpreta o relatório.

Fontes: [arc42 — ISO/IEC 5055](https://quality.arc42.org/standards/iso-5055), [CISQ — anúncio da norma](https://it-cisq.org/?p=1055), [prévia oficial com o sumário (ANSI)](https://webstore.ansi.org/preview-pages/ISO/preview_ISO+IEC+5055-2021.pdf).

## 3. OWASP Top 10:2025 — riscos de segurança mais críticos

É um documento de conscientização, não um padrão verificável: ordena dez categorias de risco em aplicações web. Esta é a 8ª edição; cada categoria agrupa várias CWEs (de 5 a 40), totalizando 248.

| # | Categoria | O que o revisor procura no código |
| --- | --- | --- |
| A01 | Controle de acesso quebrado (agora inclui SSRF) | Endpoint sem checagem de autorização, acesso a recurso por id sem verificar dono, URL externa aceita sem lista de permissão |
| A02 | Configuração insegura | Padrões inseguros, CORS aberto, mensagens de erro detalhadas em produção, recursos de debug ligados |
| A03 | Falhas na cadeia de suprimentos de software (nova, ampliou "componentes vulneráveis") | Dependências sem versão fixa, bibliotecas desatualizadas ou abandonadas, build e distribuição sem verificação |
| A04 | Falhas criptográficas | Algoritmo fraco, segredo no código, senha sem hash adequado, dado sensível em texto puro |
| A05 | Injeção (inclui XSS e SQL injection) | Consulta montada por concatenação, entrada sem validação ou codificação na saída |
| A06 | Design inseguro | Ausência de modelagem de ameaças, regra de negócio que pode ser contornada, falta de limite de uso |
| A07 | Falhas de autenticação | Gestão de sessão e de credenciais feita à mão em vez de usar o framework |
| A08 | Falhas de integridade de software e dados | Desserialização de dado não confiável, artefato ou dado aceito sem verificar integridade |
| A09 | Falhas de registro e alerta | Eventos de segurança sem log, log sem alerta, dado sensível vazando no log |
| A10 | Tratamento incorreto de condições excepcionais (nova) | Exceção engolida, erro que deixa o sistema aberto (fail open), estado inconsistente após falha |

O que importa:

- **Foco em causa raiz.** A edição de 2025 prefere categorias que apontam a causa (falha criptográfica) em vez do sintoma (exposição de dados), porque isso orienta a correção.
- **Oito categorias vêm de dados, duas da comunidade.** Os dados olham para trás e só mostram o que ferramentas já testam; a pesquisa com profissionais cobre riscos que os testes automatizados ainda não pegam.
- **A10 interessa muito à revisão de código.** Tratamento de erro é algo que se vê lendo o código, e agora conta como risco de segurança, não só de confiabilidade.

Para o agente: use o Top 10 para priorizar onde olhar, e o ASVS (seção 4) para checar requisitos concretos. A própria OWASP apresenta o Top 10 como documento de conscientização, não como padrão de verificação.

Fontes: [OWASP Top 10:2025 (pt-BR)](https://owasp.org/Top10/2025/pt-BR/), [Introdução e mudanças de 2025](https://top10.owasp.org/2025/pt-BR/0x00_2025-Introduction/).

## 4. OWASP ASVS 5.0 — padrão de verificação de segurança

É o complemento verificável do Top 10: um catálogo aberto (CC BY-SA 4.0) de cerca de 350 requisitos de segurança para aplicações web e APIs, pensado para uso direto em revisão de código, testes e contratos. A versão 5.0.0 saiu em maio de 2025, a primeira grande revisão desde 2021.

**Três níveis cumulativos** (cada um inclui o anterior):

| Nível | Parcela dos requisitos | Para quê |
| --- | --- | --- |
| L1 — Básico | \~20% | Defesas mínimas contra as vulnerabilidades mais exploradas; base para qualquer aplicação |
| L2 — Padrão | \~50% | Ataques menos comuns ou mais complexos; recomendado para aplicações de negócio com dados sensíveis |
| L3 — Avançado | \~30% | Defesa em profundidade para contextos de alta exigência (financeiro, saúde, infraestrutura crítica) |

**17 capítulos:** V1 codificação e sanitização · V2 validação e lógica de negócio · V3 segurança do frontend · V4 APIs e serviços web · V5 manipulação de arquivos · V6 autenticação · V7 gestão de sessão · V8 autorização · V9 tokens autocontidos (JWT) · V10 OAuth e OIDC · V11 criptografia · V12 comunicação segura · V13 configuração · V14 proteção de dados · V15 codificação segura e arquitetura · V16 registro de segurança e tratamento de erros · V17 WebRTC.

O que importa:

- **Cada requisito tem um identificador estável** no formato capítulo.seção.requisito, e a recomendação é citá-lo com a versão (por exemplo, v5.0.0-6.2.1). Isso dá ao revisor a rastreabilidade que o Top 10 não dá.
- **Os requisitos foram escritos para serem verificáveis:** a versão 5.0 removeu duplicações e reformulou itens para terem um objetivo testável.
- **O L1 ficou mais enxuto** que na versão 4, justamente para baixar a barreira de adoção.
- **Cobertura ampliada de OAuth/OIDC e tokens (V9, V10)**, relevante para qualquer projeto de identidade.

Para o agente: escolha o nível conforme o risco do projeto (L1 como piso; L2 para dados sensíveis) e use os capítulos aplicáveis como checklist. Todo achado de segurança deve citar o requisito com a versão.

Fontes: [arc42 — OWASP ASVS](https://quality.arc42.org/standards/owasp-asvs), [página do projeto](https://owasp.org/www-project-application-security-verification-standard/), [repositório no GitHub](https://github.com/OWASP/ASVS).

## 5. OWASP Code Review Guide — revisão de código com foco em segurança

É o único material desta lista escrito especificamente para quem faz revisão de código, mas está datado: a versão atual (2.0) é de julho de 2017, e seus capítulos de vulnerabilidades seguem o Top 10 de 2013. Use-o pelo método, não pela lista de riscos.

O livro tem três partes:

- **O porquê e o como da revisão:** preparação, lugar da revisão no ciclo de desenvolvimento seguro, cobertura, modelagem de ameaças da aplicação e métricas de revisão.
- **Tipos de vulnerabilidade e como identificá-los,** com exemplos do que não fazer e do que fazer, organizados por controle técnico (autenticação, autorização, sessão, validação de entrada, tratamento de erro, criptografia) e por vulnerabilidade (injeção SQL e de SO, XSS, CSRF, condições de corrida, logging).
- **Apêndices,** incluindo um checklist do revisor.

O que importa:

- **Ferramenta não substitui leitura.** O guia defende que scanners melhoram, mas a revisão manual continua necessária no ciclo de desenvolvimento seguro.
- **Exemplos são sinais de alerta, não receitas.** Os autores escolheram mostrar padrões suspeitos em vez de impor um jeito único de escrever, porque há muitas formas corretas de resolver o mesmo problema.
- **Revisão guiada por risco e por modelagem de ameaças:** decidir primeiro onde o código lida com dados sensíveis e entradas externas, e concentrar a atenção ali.

Para o agente: aproveite a estrutura (controle técnico → padrão vulnerável → correção) e o checklist do apêndice, mas atualize as categorias com o Top 10:2025 e o ASVS 5.0. Só a página do projeto e o sumário foram lidos aqui, não o PDF completo.

Fontes: [página do projeto](https://owasp.org/www-project-code-review-guide/), [sumário da versão anterior (wiki arquivada)](https://wiki.owasp.org/index.php/OWASP_Code_Review_Guide_Table_of_Contents).

## 6. CWE e CWE Top 25 (MITRE) — o vocabulário comum das fraquezas

O CWE (Common Weakness Enumeration) é um dicionário aberto de tipos de fraqueza de software, cada um com um identificador estável (CWE-79, CWE-89…). É a língua franca entre normas e ferramentas: a ISO 5055 é definida em CWEs, o OWASP Top 10 agrupa CWEs em categorias e os analisadores estáticos rotulam achados com CWEs.

A lista **CWE Top 25 de 2025** saiu em dezembro de 2025, com MITRE e CISA. Ela ranqueia fraquezas pela combinação de frequência e gravidade (CVSS) em cerca de 39 mil CVEs publicadas entre junho de 2024 e junho de 2025.

As entradas mais relevantes para uma aplicação web em Java/Spring (as fraquezas de memória, como estouro de buffer e use-after-free, pouco se aplicam a linguagens com memória gerenciada):

| Posição | CWE | Fraqueza |
| --- | --- | --- |
| 1 | [CWE-79](https://cwe.mitre.org/data/definitions/79.html) | Cross-site scripting (XSS) |
| 2 | [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | Injeção de SQL |
| 3 | [CWE-352](https://cwe.mitre.org/data/definitions/352.html) | Cross-site request forgery (CSRF) |
| 4 | [CWE-862](https://cwe.mitre.org/data/definitions/862.html) | Autorização ausente (subiu 5 posições) |
| 6 | [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | Path traversal |
| 12 | [CWE-434](https://cwe.mitre.org/data/definitions/434.html) | Upload irrestrito de arquivo perigoso |
| 13 | [CWE-476](https://cwe.mitre.org/data/definitions/476.html) | Desreferência de ponteiro nulo (subiu 8) |
| 15 | [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Desserialização de dados não confiáveis |
| 17 | [CWE-863](https://cwe.mitre.org/data/definitions/863.html) | Autorização incorreta |
| 18 | [CWE-20](https://cwe.mitre.org/data/definitions/20.html) | Validação de entrada inadequada |
| 20 | [CWE-200](https://cwe.mitre.org/data/definitions/200.html) | Exposição de informação sensível |
| 21 | [CWE-306](https://cwe.mitre.org/data/definitions/306.html) | Autenticação ausente em função crítica |
| 22 | [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-side request forgery (SSRF) |
| 24 | [CWE-639](https://cwe.mitre.org/data/definitions/639.html) | Bypass de autorização por chave controlada pelo usuário (IDOR) |
| 25 | [CWE-770](https://cwe.mitre.org/data/definitions/770.html) | Alocação de recursos sem limite |

O que importa:

- **Autorização é o padrão em ascensão.** CWE-862, 863, 639 e 306 somadas mostram que falhar em checar quem pode fazer o quê é hoje um dos problemas centrais, o que bate com o A01 do OWASP.
- **A lista é anual.** Use a edição do ano e cite-a com o ano.
- **Cada página de CWE traz descrição, exemplos de código vulnerável e mitigações**, material útil para o agente justificar um achado.

Para o agente: rotule todo achado de segurança ou confiabilidade com o CWE mais específico possível, não com a categoria genérica.

Fontes: [CWE Top 25 de 2025 (MITRE)](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html), [alerta da CISA](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/3ff772a).

## 7. SEI CERT Oracle Coding Standard for Java — regras de codificação segura

É o padrão de codificação segura específico de Java, mantido pelo SEI da Carnegie Mellon e aberto num wiki. O objetivo declarado é eliminar práticas de codificação que levam a vulnerabilidades exploráveis, e o próprio padrão diz que pode servir de métrica para avaliar código, por revisão manual ou automática.

Como é organizado:

- **Regras agrupadas por área,** cada uma com sigla de três letras: declarações e inicialização (DCL), expressões (EXP), números (NUM), objetos (OBJ), métodos (MET), exceções (ERR), concorrência e locks (VNA, LCK, THI, TPS, TSM), entrada e saída (FIO), serialização (SER), validação de entrada (IDS), segurança da plataforma (SEC), entre outras.
- **Identificador estável por regra,** como LCK07-J (adquirir e liberar locks sempre na mesma ordem, para evitar deadlock) ou SEC02-J (não basear checagens de segurança em fontes não confiáveis).
- **Regras e recomendações separadas:** regras (00–49) são obrigatórias para conformidade; recomendações (50 em diante), como DCL51-J (não sombrear identificadores em escopos internos), são boas práticas.
- **Prioridade por nível (L1 a L3),** calculada a partir de gravidade, probabilidade e custo de correção. L1 é o que corrigir primeiro.
- **Cada regra traz exemplo de código não conforme e solução conforme,** além do mapeamento para ferramentas de análise estática.

O que importa:

- **Cobre o que é idiomático de Java** e que normas gerais não alcançam: publicação segura de objetos entre threads, armadilhas de `equals`/`hashCode`, exceções engolidas, desserialização.
- **Atenção à data:** a base do padrão foi escrita para versões antigas do Java (SE 6/7). Parte das regras de segurança da plataforma (SecurityManager, applets) perdeu relevância no Java moderno; as de concorrência, exceções e objetos continuam valendo.

Para o agente: use as regras L1 e L2 de ERR, OBJ, MET, LCK/VNA, IDS e SER como checklist de Java, citando o identificador (ex.: ERR00-J) no achado.

Fontes: [introdução do padrão (SEI wiki)](https://wiki.sei.cmu.edu/confluence/x/8kpMBQ), [exportação estruturada das regras](https://huggingface.co/datasets/safebuffer/sei-cert-java-rules/viewer/default/train).

## 8. Google Engineering Practices — guia de code review

É a referência mais direta sobre *como* revisar, não sobre *o que* é qualidade. Descreve o processo de revisão do Google em dois manuais: o do revisor e o do autor da mudança. O repositório foi arquivado em novembro de 2025, mas o site continua no ar e a licença (CC-BY 3.0) permite reutilizar o texto com atribuição.

**O critério de aprovação.** O objetivo da revisão é que a saúde geral do código melhore com o tempo. Daí a regra principal: aprovar a mudança quando ela certamente melhora o sistema, mesmo que não esteja perfeita. Não existe código perfeito, só código melhor. Mas nada justifica aprovar algo que piora o código, exceto numa emergência.

**O que o revisor examina:** design (é adequado ao sistema?), funcionalidade (faz o que o autor pretendia, e isso é bom para o usuário?), complexidade (dá para simplificar? outra pessoa entenderia?), testes (existem, estão corretos e bem desenhados?), nomes, comentários (claros e úteis?), estilo (segue o guia?) e documentação (foi atualizada?). O design é o item mais importante.

**Princípios para decidir divergências:**

1. Fatos técnicos e dados valem mais que opinião e gosto pessoal.
2. Em estilo, o guia de estilo é a autoridade; o que não está nele é preferência, e vale a consistência com o código existente.
3. Design quase nunca é questão de gosto: decide-se por princípios de engenharia. Se o autor demonstra que duas soluções são igualmente válidas, prevalece a dele.
4. Sem outra regra aplicável, peça consistência com o código atual, desde que isso não piore o sistema.

**Severidade explícita.** Comentários de polimento ou puramente educativos levam o prefixo "Nit:", sinalizando que o autor pode ignorá-los. Isso separa o que bloqueia do que é sugestão.

**Conflitos não podem travar a mudança.** Primeiro busca-se consenso com base no guia; se não houver, escala-se para quem decide (líder técnico, mantenedor).

O manual do revisor também cobre: como navegar numa mudança, velocidade de resposta, como escrever comentários e como lidar com resistência do autor.

Para o agente: adote o critério "melhora a saúde do código" como regra de aprovação, o prefixo de severidade (bloqueante / recomendado / nit), a hierarquia fatos > guia > princípios > consistência, e o roteamento de impasses para o Arquiteto ou o Gerente de Produto em vez de ciclos infinitos com o Escritor.

Fontes: [visão geral do processo](https://google.github.io/eng-practices/review/), [manual do revisor](https://google.github.io/eng-practices/review/reviewer/), [o padrão de code review](https://google.github.io/eng-practices/review/reviewer/standard.html).

## Síntese: o papel de cada referência no agente revisor

Nenhuma referência sozinha basta: cada uma responde a uma pergunta diferente do revisor.

| Referência | Pergunta que responde | Uso no agente | Como citar no achado |
| --- | --- | --- | --- |
| ISO/IEC 25010:2023 | O que é qualidade? | Taxonomia para classificar cada achado | Característica/subcaracterística (ex.: manutenibilidade/testabilidade) |
| ISO/IEC 5055:2021 | Como medir qualidade no código? | Base para as regras estruturais da análise estática | CWE da medida |
| OWASP Top 10:2025 | Onde estão os maiores riscos? | Priorizar onde olhar primeiro | A01:2025 … A10:2025 |
| OWASP ASVS 5.0 | Que requisito de segurança deve ser cumprido? | Checklist de segurança, no nível L1 ou L2 | v5.0.0-capítulo.seção.requisito |
| OWASP Code Review Guide | Como revisar com foco em segurança? | Método: controle técnico, padrão vulnerável, correção | Não usado como identificador |
| CWE / Top 25 de 2025 | Qual é exatamente a fraqueza? | Rótulo preciso de cada achado de segurança e confiabilidade | CWE-xxx |
| SEI CERT Java | Qual é a regra idiomática em Java? | Checklist da stack | ERR00-J, LCK07-J… |
| Google eng-practices | Quando aprovar e como comentar? | Critério de aprovação, severidade, resolução de impasses | Não usado como identificador |

Um achado bem formado combina três delas: a característica da 25010 (o que foi afetado), o identificador específico (CWE, ASVS ou CERT) e a severidade no estilo do Google (bloqueante, recomendado ou nit).
