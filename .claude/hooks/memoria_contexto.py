"""Hook SessionStart: injeta no contexto um resumo do estado da memória.

task.json e roadmap.json são estado local (fora do Git): num clone novo eles não
existem, e este hook os recria a partir dos modelos da skill nova-memoria.

Nunca falha: qualquer erro de leitura vira um aviso de uma linha.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
MEMORIA = RAIZ / ".claude" / "memoria"
MODELOS = RAIZ / ".claude" / "skills" / "nova-memoria" / "assets"


def recriar_estado_ausente():
    """Copia o modelo vazio para cada arquivo de estado que faltar; devolve os nomes recriados."""
    recriados = []
    for nome in ("task", "roadmap"):
        destino = MEMORIA / f"{nome}.json"
        if not destino.exists():
            shutil.copyfile(MODELOS / f"{nome}.vazio.json", destino)
            recriados.append(destino.name)
    return recriados


def carregar(nome):
    with open(MEMORIA / nome, encoding="utf-8") as f:
        return json.load(f)


def impedimentos_abertos():
    texto = (MEMORIA / "impedimentos.md").read_text(encoding="utf-8")
    m = re.search(r"^## Abertos\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    if not m:
        return []
    return re.findall(r"^### (I-\d+ — .+)$", m.group(1), re.M)


def main():
    try:
        print(resumo())
    except Exception as e:  # leitura ou formato falhou: avisa e segue
        print(f"[memória] Aviso: não foi possível resumir a memória ({type(e).__name__}: {e}). "
              "Leia .claude/memoria/ manualmente e rode: python3 -I .claude/hooks/validar_memoria.py --tudo")


def resumo():
    linhas = ["[memória] Resumo do estado (protocolo em .claude/regras/memoria.md):"]
    recriados = recriar_estado_ausente()
    if recriados:
        linhas.append(f"- Estado local recriado dos modelos ({', '.join(recriados)}): cópia de trabalho nova. "
                      "Se havia fluxo em andamento, reconstrua a tarefa a partir de docs/execucoes/<slug>.md.")
    roadmap = carregar("roadmap.json")
    task = carregar("task.json")
    abertos = impedimentos_abertos()

    r = roadmap.get("roadmap") or {}
    t = task.get("tarefa") or {}
    if not r.get("titulo") and not t.get("id"):
        linhas.append("- Sem roadmap nem tarefa ativa.")
    else:
        if r.get("titulo"):
            linhas.append(f"- Roadmap: {r['titulo']} ({r.get('status')}); tarefa_atual: {roadmap.get('tarefa_atual')}")
        if t.get("id"):
            linhas.append(f"- Tarefa {t['id']} — {t.get('titulo')} ({t.get('status')}); aguardando: {task.get('aguardando')}")
            linhas.append(f"- Próximo passo: {task.get('proximo_passo')}")
            for e in task.get("plano", []):
                if e.get("status") != "feita":
                    linhas.append(f"  - etapa {e.get('n')}: {e.get('etapa')} [{e.get('status')}]")
    if abertos:
        linhas.append("- Impedimentos abertos: " + "; ".join(abertos))
    linhas.append("- Antes de retomar, leia .claude/memoria/roadmap.json, task.json e os impedimentos abertos.")
    linhas.append("- Para escrever na memória, siga a skill nova-memoria.")
    return "\n".join(linhas)


if __name__ == "__main__":
    main()
    sys.exit(0)
