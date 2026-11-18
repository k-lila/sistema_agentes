"""Validador da memória (.claude/memoria/).

Uso como hook PostToolUse (Edit|Write|Bash): lê o evento do stdin e só age se o
alvo estiver em .claude/memoria/ (ou, no Bash, se o comando citar .claude/memoria).
  - erro estrutural ou falha do próprio validador -> stderr + exit 2
    (volta ao Claude para corrigir);
  - divergência entre arquivos -> aviso via additionalContext, sem bloquear
    (pode ser transitória durante um fechamento).
Uso manual: python3 -I .claude/hooks/validar_memoria.py --tudo
"""
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2]).resolve()
MEMORIA = RAIZ / ".claude" / "memoria"
MODELOS = RAIZ / ".claude" / "skills" / "nova-memoria" / "assets"

ST_TAREFA_TASK = {None, "em_andamento", "bloqueada"}
ST_ETAPA = {"pendente", "em_andamento", "feita", "bloqueada"}
ST_ROADMAP = {None, "planejamento", "em_andamento", "concluido", "suspenso"}
ST_TAREFA_ROADMAP = {"planejada", "proxima", "em_andamento", "bloqueada", "concluida", "cancelada"}
ACOES = {"criar", "modificar", "excluir"}
RE_DATAHORA = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}\Z")
RE_DATA = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
RE_I = re.compile(r"I-\d{3,}\Z")
RE_D = re.compile(r"D-\d{3,}\Z")
RE_TASK = re.compile(r"TASK-\d{3,}\Z")

erros, avisos = [], []


def carregar(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        erros.append(f"{caminho.relative_to(RAIZ)}: arquivo ausente")
    except json.JSONDecodeError as e:
        erros.append(f"{caminho.relative_to(RAIZ)}: JSON inválido ({e})")
    return None


def chaves_iguais(onde, atual, modelo):
    if not isinstance(atual, dict):
        erros.append(f"{onde}: deveria ser objeto")
        return False
    faltam, sobram = set(modelo) - set(atual), set(atual) - set(modelo)
    if faltam:
        erros.append(f"{onde}: chaves ausentes {sorted(faltam)}")
    if sobram:
        erros.append(f"{onde}: chaves desconhecidas {sorted(sobram)}")
    return not faltam and not sobram


def fixas_iguais(nome, atual, modelo):
    """Chaves _* (instruções e modelos de item) devem ser idênticas às do modelo."""
    for k in sorted(c for c in modelo if c.startswith("_")):
        if atual[k] != modelo[k]:
            erros.append(f"{nome}: '{k}' difere do modelo; chaves _* não se editam no arquivo vivo "
                         f"(o modelo fica em .claude/skills/nova-memoria/assets/)")


def itens(onde, lista, chaves):
    """Valida que lista é lista de objetos com exatamente as chaves dadas; devolve os válidos."""
    if not isinstance(lista, list):
        erros.append(f"{onde}: deveria ser lista")
        return []
    ok = []
    for i, it in enumerate(lista):
        if chaves_iguais(f"{onde}[{i}]", it, chaves):
            ok.append(it)
    return ok


def lista_de(onde, valor, regex=None, formato=""):
    """Valida que valor é lista de strings (no formato de regex, se dado)."""
    if not isinstance(valor, list):
        erros.append(f"{onde}: deveria ser lista (recebido {valor!r})")
        return
    for v in valor:
        if not isinstance(v, str) or (regex and not regex.match(v)):
            erros.append(f"{onde}: item inválido {v!r}" + (f"; use {formato}" if formato else "; use texto"))


def data_hora(onde, valor):
    if valor is not None and not (isinstance(valor, str) and RE_DATAHORA.match(valor)):
        erros.append(f"{onde}: use AAAA-MM-DDTHH:MM ou null (recebido {valor!r})")


def data(onde, valor):
    if valor is not None and not (isinstance(valor, str) and RE_DATA.match(valor)):
        erros.append(f"{onde}: use AAAA-MM-DD ou null (recebido {valor!r})")


def validar_task(task, modelo):
    if not chaves_iguais("task.json", task, modelo):
        return
    fixas_iguais("task.json", task, modelo)
    data_hora("task.json atualizado_em", task["atualizado_em"])
    t = task["tarefa"]
    if chaves_iguais("task.json tarefa", t, modelo["tarefa"]):
        if t["status"] not in ST_TAREFA_TASK:
            erros.append(f"task.json tarefa.status inválido: {t['status']!r} (aguardar usuário vai em 'aguardando')")
        if t["id"] is not None and not RE_TASK.match(str(t["id"])):
            erros.append(f"task.json tarefa.id inválido: {t['id']!r}")
        data("task.json tarefa.iniciada_em", t["iniciada_em"])
        for c in itens("task.json criterios_de_aceite", t["criterios_de_aceite"], modelo["_modelo_de_criterio"]):
            if not isinstance(c["verificado"], bool):
                erros.append("task.json criterios_de_aceite: 'verificado' deve ser true/false")
            elif c["verificado"] and not c["evidencia"]:
                erros.append(f"task.json critério verificado sem evidência: {c['criterio']!r}")
        lista_de("task.json tarefa.fora_do_escopo", t["fora_do_escopo"])
    ag = task["aguardando"]
    if ag is not None and ag != "usuario" and not (isinstance(ag, str) and re.match(r"agente:\S+\Z", ag)):
        erros.append(f"task.json aguardando inválido: {ag!r}")
    for e in itens("task.json plano", task["plano"], modelo["_modelo_de_etapa"]):
        if e["status"] not in ST_ETAPA:
            erros.append(f"task.json etapa {e['n']}: status inválido {e['status']!r}")
        if e["status"] == "bloqueada" and not (isinstance(e["impedimento"], str) and RE_I.match(e["impedimento"])):
            erros.append(f"task.json etapa {e['n']}: bloqueada exige impedimento I-XXX")
        elif e["impedimento"] is not None and not (isinstance(e["impedimento"], str) and RE_I.match(e["impedimento"])):
            erros.append(f"task.json etapa {e['n']}: impedimento deve ser I-XXX ou null")
    for a in itens("task.json arquivos", task["arquivos"], modelo["_modelo_de_arquivo"]):
        if a["acao"] not in ACOES:
            erros.append(f"task.json arquivo {a['caminho']}: acao inválida {a['acao']!r}")
    for a in itens("task.json autorizacoes", task["autorizacoes"], modelo["_modelo_de_autorizacao"]):
        data(f"task.json autorização {a['id']} data", a["data"])
        if isinstance(a["caminhos"], list) and not a["caminhos"]:
            erros.append(f"task.json autorização {a['id']}: 'caminhos' deve ser lista não vazia")
        else:
            lista_de(f"task.json autorização {a['id']} caminhos", a["caminhos"])
    lista_de("task.json decisoes_registradas", task["decisoes_registradas"], RE_D, "D-XXX")
    pend = task["pendencias_de_fechamento"]
    if chaves_iguais("task.json pendencias_de_fechamento", pend, modelo["pendencias_de_fechamento"]):
        lista_de("task.json pendencias.apontamentos_sem_disposicao", pend["apontamentos_sem_disposicao"])
        lista_de("task.json pendencias.adrs_pendentes", pend["adrs_pendentes"])
    itens("task.json arquivos_apoio", task["arquivos_apoio"], modelo["_modelo_de_arquivo_apoio"])
    lista_de("task.json notas_de_retomada", task["notas_de_retomada"])


def validar_roadmap(rm, modelo):
    if not chaves_iguais("roadmap.json", rm, modelo):
        return
    fixas_iguais("roadmap.json", rm, modelo)
    data_hora("roadmap.json atualizado_em", rm["atualizado_em"])
    if chaves_iguais("roadmap.json roadmap", rm["roadmap"], modelo["roadmap"]):
        if rm["roadmap"]["status"] not in ST_ROADMAP:
            erros.append(f"roadmap.json status inválido: {rm['roadmap']['status']!r}")
        data("roadmap.json iniciado_em", rm["roadmap"]["iniciado_em"])
    ta = rm["tarefa_atual"]
    if ta is not None and not (isinstance(ta, str) and RE_TASK.match(ta)):
        erros.append(f"roadmap.json tarefa_atual: use TASK-NNN ou null (recebido {ta!r})")
    tarefas = itens("roadmap.json tarefas", rm["tarefas"], modelo["_modelo_de_tarefa"])
    for t in tarefas:
        if not (isinstance(t["id"], str) and RE_TASK.match(t["id"])):
            erros.append(f"roadmap.json tarefa com id inválido: {t['id']!r}")
        if t["status"] not in ST_TAREFA_ROADMAP:
            erros.append(f"roadmap.json {t['id']}: status inválido {t['status']!r}")
        lista_de(f"roadmap.json {t['id']} depende_de", t["depende_de"], RE_TASK, "TASK-NNN")
        data(f"roadmap.json {t['id']} concluida_em", t["concluida_em"])
    proximas = [t["id"] for t in tarefas if t["status"] == "proxima"]
    if len(proximas) > 1:
        erros.append(f"roadmap.json: mais de uma tarefa 'proxima' {proximas}")
    itens("roadmap.json arquivos_apoio", rm["arquivos_apoio"], modelo["_modelo_de_arquivo_apoio"])


def ids_em(nome, prefixo):
    try:
        texto = (MEMORIA / nome).read_text(encoding="utf-8")
    except FileNotFoundError:
        erros.append(f"{nome}: arquivo ausente")
        return set()
    return set(re.findall(rf"^### ({prefixo}-\d+)", texto, re.M))


def cruzar(task, rm):
    """Divergências entre arquivos. Só roda com a estrutura já válida (sem erros)."""
    ids_i, ids_d = ids_em("impedimentos.md", "I"), ids_em("decisoes.md", "D")
    tid, ta = task["tarefa"]["id"], rm["tarefa_atual"]
    tarefas = {t["id"]: t for t in rm["tarefas"]}
    if rm["roadmap"]["titulo"] is None:  # sem roadmap: tarefa, se houver, é avulsa
        if ta is not None:
            avisos.append(f"roadmap.tarefa_atual ({ta}) preenchido sem roadmap; tarefa avulsa vive só em task.json")
    else:
        if ta != tid:
            avisos.append(f"roadmap.tarefa_atual ({ta}) ≠ task.tarefa.id ({tid})")
        if ta is not None and ta not in tarefas:
            avisos.append(f"roadmap.tarefa_atual ({ta}) não está em roadmap.tarefas")
    refs_i = [e["impedimento"] for e in task["plano"] if e["impedimento"]]
    for i in sorted(set(refs_i) - ids_i):
        avisos.append(f"{i} citado mas ausente em impedimentos.md")
    for d in sorted(set(task["decisoes_registradas"]) - ids_d):
        avisos.append(f"{d} citado mas ausente em decisoes.md")
    ids_aut = {a["id"] for a in task["autorizacoes"]}
    for a in task["arquivos"]:
        if a["autorizacao"] not in ids_aut:
            avisos.append(f"arquivo {a['caminho']}: autorização {a['autorizacao']!r} inexistente")
    for t in tarefas.values():
        for dep in t["depende_de"]:
            if dep not in tarefas:
                avisos.append(f"{t['id']} depende de {dep}, que não existe")
            elif t["status"] == "proxima" and tarefas[dep]["status"] != "concluida":
                avisos.append(f"{t['id']} está 'proxima' mas {dep} não está concluida")


def validar():
    m_task, m_rm = carregar(MODELOS / "task.vazio.json"), carregar(MODELOS / "roadmap.vazio.json")
    task, rm = carregar(MEMORIA / "task.json"), carregar(MEMORIA / "roadmap.json")
    if m_task and task is not None:
        validar_task(task, m_task)
    if m_rm and rm is not None:
        validar_roadmap(rm, m_rm)
    if not erros:
        cruzar(task, rm)


def alvo_na_memoria(entrada):
    """True se a ferramenta do evento escreveu (ou pode ter escrito) na memória."""
    ti = entrada.get("tool_input") or {}
    if entrada.get("tool_name") == "Bash":
        return ".claude/memoria" in (ti.get("command") or "")
    alvo = ti.get("file_path")
    if not alvo:
        return False
    alvo = Path(alvo)
    if not alvo.is_absolute():
        alvo = Path(entrada.get("cwd") or RAIZ) / alvo
    return alvo.resolve().is_relative_to(MEMORIA)


def main():
    if "--tudo" in sys.argv:
        validar()
        for e in erros:
            print(f"ERRO: {e}")
        for a in avisos:
            print(f"AVISO: {a}")
        if not erros and not avisos:
            print("Memória válida.")
        sys.exit(1 if erros else 0)

    if not alvo_na_memoria(json.load(sys.stdin)):
        sys.exit(0)
    validar()
    if erros:
        print("Memória inválida após a edição; corrija agora:\n- " + "\n- ".join(erros), file=sys.stderr)
        sys.exit(2)
    if avisos:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "Divergências na memória (podem ser transitórias):\n- " + "\n- ".join(avisos),
        }}, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # falha do validador não pode passar em silêncio
        print(f"Validador da memória falhou ({type(e).__name__}: {e}); "
              f"confira .claude/memoria/ com: python3 -I .claude/hooks/validar_memoria.py --tudo", file=sys.stderr)
        sys.exit(2)
