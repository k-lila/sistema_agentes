"""Hook PreToolUse (Edit|Write|NotebookEdit|Bash): protege escritas.

Roda de dois jeitos:

1. Pelo settings.json do projeto, sem argumentos (conversa principal e subagentes):
   - Subagente (agent_id presente) escrevendo em .claude/memoria/ -> deny.
     No Bash: comando que cita .claude/memoria e parece escrita.
   - Com tarefa ativa: alvo no projeto, fora da memória, não coberto por
     task.json > autorizacoes[].caminhos -> ask. Sem tarefa ativa: sem decisão.

2. Pelo frontmatter de um agente, com `--papel <nome do agente>`:
   - Alvo em caminho que pertence a outro papel (tabela PROPRIEDADE) -> deny.
   - Só essa checagem roda; as do item 1 ficam com a invocação do projeto,
     que acontece na mesma chamada de ferramenta.

Worktree: um alvo em .claude/worktrees/<nome>/ (cópia isolada criada pelo Claude Code)
é julgado, na propriedade e no status de ADR, pelo caminho dentro da cópia; sem isso a
linha `.claude/` da tabela negaria todo o experimento do /spike. A checagem de
autorizações continua usando o caminho real, relativo à raiz do projeto.

Nos dois: gravar em docs/adr/ uma linha de status `Aceito` ou `Substituído por`
-> deny. Essas linhas são gravadas só pelo usuário, à mão (skill nova-adr).

- Demais casos -> sem decisão (fluxo normal de permissões).
- Falha do próprio hook -> ask (nunca libera em silêncio).

Limite conhecido: escrita via Bash fora de .claude/memoria/ não passa por aqui, e a
separação entre código de produção e código de teste depende do perfil de stack;
as duas continuam na conferência por git do orquestrador e do gerente-de-qualidade.
"""
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2]).resolve()
MEMORIA = RAIZ / ".claude" / "memoria"
# Heurística de escrita em comandos Bash (redirecionamento ou programa que grava).
RE_ESCRITA_BASH = re.compile(
    r">|\b(tee|sed\s+-i|cp|mv|rm|touch|truncate|install|ln|dd|python3?|perl|ruby|node)\b")

# Dono de cada caminho, relativo à raiz; vale a primeira linha que casar.
# "orquestrador" e "usuario" não são agentes: nenhum --papel escreve ali.
PROPRIEDADE = [
    (re.compile(r"docs/produto/"), "gerente-de-produto"),
    (re.compile(r"docs/adr/"), "arquiteto"),
    (re.compile(r"docs/contracts/"), "arquiteto"),
    (re.compile(r"docs/testes/[^/]+/especificacao\.md\Z"), "arquiteto"),
    (re.compile(r"docs/testes/"), "orquestrador"),
    (re.compile(r"docs/senso-critico/"), "senso-critico"),
    (re.compile(r"docs/execucoes/"), "orquestrador"),
    (re.compile(r"docs/referencias/"), "orquestrador"),
    (re.compile(r"\.claude/memoria/"), "orquestrador"),
    (re.compile(r"\.claude/"), "usuario"),
]
# Worktree do Claude Code: o grupo 1 é o caminho dentro da cópia.
RE_WORKTREE = re.compile(r"\.claude/worktrees/[^/]+/(.+)\Z")
# Linha de status na ADR ("- Aceito — data") ou célula de status no índice ("| Aceito |").
RE_STATUS_DO_USUARIO = re.compile(
    r"^\s*-\s*(Aceito|Substituído por)\b|\|\s*(Aceito|Substituído por[^|]*?)\s*\|")


def glob_para_regex(glob):
    """Converte glob relativo à raiz em regex: ** atravessa pastas, * e ? não."""
    partes, i = [], 0
    while i < len(glob):
        c = glob[i]
        if glob.startswith("**/", i):
            partes.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            partes.append(".*")
            i += 2
        elif c == "*":
            partes.append("[^/]*")
            i += 1
        elif c == "?":
            partes.append("[^/]")
            i += 1
        else:
            partes.append(re.escape(c))
            i += 1
    return re.compile("".join(partes) + r"\Z")


def ler_task():
    try:
        with open(MEMORIA / "task.json", encoding="utf-8") as f:
            task = json.load(f)
    except Exception:
        return {}
    return task if isinstance(task, dict) else {}


def caminhos_autorizados(task):
    globs = []
    for a in task.get("autorizacoes") or []:
        if isinstance(a, dict) and isinstance(a.get("caminhos"), list):
            globs.extend(c.removeprefix("./").removeprefix("/") for c in a["caminhos"] if isinstance(c, str))
    return globs


def papel_informado():
    """Valor de --papel, ou None quando o hook roda pelo settings.json do projeto."""
    if "--papel" not in sys.argv:
        return None
    i = sys.argv.index("--papel")
    return sys.argv[i + 1] if i + 1 < len(sys.argv) else ""


def dono_de(relativo):
    for regex, dono in PROPRIEDADE:
        if regex.match(relativo):
            return dono
    return None


def linhas_de_status(texto):
    return Counter(l.strip() for l in (texto or "").splitlines() if RE_STATUS_DO_USUARIO.search(l))


def status_novos(ferramenta, ti, alvo):
    """Linhas de status reservadas ao usuário que a escrita acrescentaria ao arquivo."""
    if ferramenta == "Edit":
        antes, depois = ti.get("old_string"), ti.get("new_string")
    elif ferramenta == "Write":
        antes = alvo.read_text(encoding="utf-8") if alvo.is_file() else ""
        depois = ti.get("content")
    else:
        return []
    return sorted((linhas_de_status(depois) - linhas_de_status(antes)).elements())


def decidir(decisao, motivo):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decisao,
            "permissionDecisionReason": motivo,
        }
    }, ensure_ascii=False))
    sys.exit(0)


NEGAR_SUBAGENTE = ("Subagentes não escrevem em .claude/memoria/ (protocolo de memória). "
                   "Devolva a informação ao orquestrador.")


def main():
    entrada = json.load(sys.stdin)
    ti = entrada.get("tool_input") or {}
    subagente = bool(entrada.get("agent_id"))
    papel = papel_informado()
    ferramenta = entrada.get("tool_name")

    if ferramenta == "Bash":
        cmd = ti.get("command") or ""
        if papel is None and subagente and ".claude/memoria" in cmd and RE_ESCRITA_BASH.search(cmd):
            decidir("deny", NEGAR_SUBAGENTE)
        return

    alvo = ti.get("file_path") or ti.get("notebook_path")
    if not alvo:
        return
    alvo = Path(alvo)
    if not alvo.is_absolute():
        alvo = Path(entrada.get("cwd") or RAIZ) / alvo
    alvo = alvo.resolve()

    if not alvo.is_relative_to(RAIZ):
        return  # fora do projeto (ex.: ~/.claude/plans): fluxo normal
    relativo = alvo.relative_to(RAIZ).as_posix()
    em_worktree = RE_WORKTREE.match(relativo)
    na_copia = em_worktree.group(1) if em_worktree else relativo

    if na_copia.startswith("docs/adr/"):
        novos = status_novos(ferramenta, ti, alvo)
        if novos:
            decidir("deny", "As linhas de status 'Aceito' e 'Substituído por' de uma ADR são gravadas só pelo "
                            "usuário, à mão, na ADR e no índice (skill nova-adr). Não grave: mostre ao usuário "
                            f"a linha exata e o arquivo. Linha recusada: {novos[0]!r}")

    if papel is not None:  # invocação pelo frontmatter do agente: só a propriedade do papel
        dono = dono_de(na_copia)
        if dono and dono != papel:
            decidir("deny", f"'{na_copia}' pertence a '{dono}', não ao papel '{papel}'. Ninguém altera artefato "
                            "de outro papel: relate o que precisa mudar no seu relatório ao orquestrador.")
        return

    if alvo.is_relative_to(MEMORIA):
        if subagente:
            decidir("deny", NEGAR_SUBAGENTE)
        return

    task = ler_task()
    if not (task.get("tarefa") or {}).get("id"):
        return  # sem tarefa ativa: fluxo normal de permissões
    if any(glob_para_regex(g).match(relativo) for g in caminhos_autorizados(task)):
        return
    decidir("ask", f"'{relativo}' está fora das autorizações da tarefa ativa (task.json > autorizacoes). "
                   "Confirme a edição; se fizer parte da tarefa, registre a autorização.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # falha do hook não pode liberar a escrita em silêncio
        decidir("ask", f"Hook proteger_escrita falhou ({type(e).__name__}: {e}); confirme a operação manualmente.")
