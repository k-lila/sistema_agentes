## Regra das referências

`docs/referencias/` reúne as referências técnicas do projeto. Diante de uma dúvida técnica, elas são o primeiro caminho para a resposta ou para a melhor decisão. Vale para o orquestrador e para todos os agentes, principalmente os técnicos.

- **Dúvida técnica:** qualquer questão sobre como algo funciona ou como deve ser feito (ferramenta, técnica, padrão, norma) que os artefatos do projeto ainda não decidem. O que o produto deve fazer não é dúvida técnica: isso é da spec.
- **Consulte antes de responder:** leia o índice `docs/referencias/README.md`, escolha o documento pelo que ele responde e leia só a seção pertinente. Nunca leia uma referência inteira. Só depois recorra às outras fontes (código, documentação oficial, web, conhecimento geral).
- **Referência informa, não decide:** ADR aceita, contrato e spec continuam valendo. Se uma referência contradisser um deles, não escolha: relate a contradição a quem decide.
- **Quando a referência não cobre:** siga pelas outras fontes e diga que a referência não cobriu. Nem toda pergunta tem resposta ali, e isso não bloqueia o trabalho.
- **Deixe rastro:** quem usa uma referência cita o documento e a seção (`[ref: <documento> §<seção>]`). Quem procurou e não achou registra a lacuna e a devolve ao orquestrador, que avalia se ela pede uma referência nova.
- **Referência desatualizada ou errada:** se a fonte original ou o comportamento observado contradisser a referência, relate; não a corrija.
- **Dono da pasta:** o orquestrador. Subagentes não escrevem em `docs/referencias/` (o hook nega). Toda referência nova ou renomeada entra no índice no mesmo passo.
