## Regras de método

- Atualizações de rotina da memória (`.claude/memoria/`) dispensam relatório; fechamentos, exclusões e resets trazem um resumo antes, conforme `.claude/regras/memoria.md`.
- Dentro dos fluxos `/feature` e `/fundacao`, o resumo confirmado na Etapa 0 e os portões 1 a 3 substituem o relatório abaixo; os subagentes desses fluxos não apresentam relatório prévio e escrevem só nos caminhos do próprio papel.
- Dentro do fluxo `/bugfix`, o enquadramento confirmado na Etapa 0 e o diagnóstico confirmado no Portão 1 substituem o relatório abaixo; os subagentes não apresentam relatório prévio e escrevem só nos caminhos do próprio papel, e o escritor só no escopo confirmado.
- Dentro do fluxo `/spike`, o enquadramento confirmado no Portão 1 substitui o relatório abaixo; o escritor não apresenta relatório prévio e escreve só na worktree do experimento.
- Antes de cada alteração em código ou documentação, apresente um relatório resumido que aponte claramente:
  1. razões dos novos códigos e/ou das modificações;
  2. arquivos a serem criados, se houver;
  3. arquivos a serem modificados, se houver;
- Ao elaborar perguntas e fornecer as opções de resposta, para cada resposta:
  1. Uma frase para a opção em si;
  2. Uma frase para a justificativa da opção;
  3. Ao menos 1 pró;
  4. Ao menos 1 contra;
