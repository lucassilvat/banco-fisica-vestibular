r"""Resoluções animadas (adicionais à resolução comentada; não a substituem).

  python -m pipeline animacoes verificar [filtro]
  python -m pipeline animacoes preparar  [filtro]   -> trabalho/publicacao/animacoes-lote-NN.json

Cada roteiro fica em data/animacoes/<id da questão>.json (esquema em
schemas/animacao.schema.json e explicação em docs/ANIMACOES.md). O roteiro escolhe um
modelo de cena (desenhado pelo player do app e, opcionalmente, pelo Manim em videos/) e
descreve os passos: conceito físico, texto, equações, pergunta e o que a cena mostra.

Os nomes de elementos e de estado aceitos por modelo (MODELOS) precisam bater com os
modelos de cena de app/index.html (CENAS) e de videos/manim_roteiro.py.
"""
import json
import re

from .comum import DADOS, TRABALHO, carregar_questoes
from .verificar import checar_latex

ANIMACOES = DADOS / "animacoes"

MODELOS = {
    "plano-inclinado": {
        "parametros": {"senTheta", "cosTheta", "mu", "g"},
        "elementos": {"rampa", "angulo", "caixa", "peso", "normal", "atrito", "eixos", "componentes",
                      "angulo-peso", "aceleracao", "balanco"},
        "estado": {"movimento": {"repouso", "acelerando"}, "controle": {"aceleracao", None}},
    },
    "circuito-conjuntos-serie": {
        "parametros": {"conjuntos", "rSobreR"},
        "elementos": {"circuito", "conjuntos", "corrente", "equivalentes", "brilho"},
        "estado": {"queimada": None},   # None: qualquer valor (nome de um conjunto ou null)
    },
    "grafico-vt": {
        "parametros": {"pontos", "tMax", "vMax", "passoT", "passoV", "trechos", "paradas"},
        "elementos": {"eixos", "curva", "estrada", "paradas", "faixa", "area-1", "area-2", "cotas-1", "cotas-2"},
        "estado": {"percorrer": {True, False}},
    },
}
OBRIG = ["id", "titulo", "conceitos", "cena", "passos", "status"]
TAGS_OK = re.compile(r"</?(i|b|u|sub|sup)>")


def carregar(filtro: str | None = None) -> list[dict]:
    out = []
    for f in sorted(ANIMACOES.glob("*.json")):
        if filtro and filtro not in f.name:
            continue
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


def checar(a: dict, questoes: dict) -> list[str]:
    e = [f"falta o campo {k}" for k in OBRIG if k not in a]
    if e: return e
    q = questoes.get(a["id"])
    if not q: return [f"não existe questão {a['id']}"]
    if a["status"] not in ("rascunho", "revisado", "publicado"): e.append(f"status inválido {a['status']}")
    m = MODELOS.get(a["cena"].get("modelo"))
    if not m: return e + [f"modelo de cena desconhecido: {a['cena'].get('modelo')}"]
    for k in a["cena"].get("parametros", {}):
        if k not in m["parametros"]: e.append(f"parâmetro desconhecido no modelo: {k}")
    if not a["passos"]: e.append("roteiro sem passos")
    for i, p in enumerate(a["passos"], 1):
        onde = f"passo {i}"
        for k in ("titulo", "texto"):
            if not p.get(k): e.append(f"{onde}: falta {k}")
        textos = [("texto", p.get("texto", ""))] + [(f"equação {j}", "\\(" + x + "\\)") for j, x in enumerate(p.get("equacoes", []), 1)]
        if p.get("pergunta"):
            textos += [("pergunta", p["pergunta"].get("texto", "")), ("resposta", p["pergunta"].get("resposta", ""))]
            if not p["pergunta"].get("texto") or not p["pergunta"].get("resposta"): e.append(f"{onde}: pergunta sem texto ou resposta")
        for campo, t in textos:
            e += checar_latex(t, f"{onde}, {campo}")
            resto = TAGS_OK.sub("", re.sub(r"\\\(.+?\\\)", "", t))
            if re.search(r"<[a-zA-Z/]", resto): e.append(f"{onde}, {campo}: marcação HTML não aceita")
        c = p.get("cena", {})
        for k in ("mostrar", "ocultar", "destacar"):
            for x in c.get(k, []):
                if x not in m["elementos"]: e.append(f"{onde}: elemento desconhecido em {k}: {x}")
        for k, v in c.get("estado", {}).items():
            if k not in m["estado"]: e.append(f"{onde}: estado desconhecido: {k}"); continue
            ok = m["estado"][k]
            if ok is not None and v not in ok: e.append(f"{onde}: valor inválido para {k}: {v}")
    if q.get("gabarito") and a["status"] != "rascunho":
        ultimo = a["passos"][-1]["texto"]
        if f"({q['gabarito']})" not in ultimo.upper():
            e.append(f"o último passo não cita a alternativa do gabarito ({q['gabarito']})")
    return e


def verificar(filtro: str | None = None) -> int:
    questoes = {q["id"]: q for _, q in carregar_questoes()}
    n_err = 0
    for a in carregar(filtro):
        erros = checar(a, questoes)
        n_err += len(erros)
        print(("ERRO " if erros else "ok   ") + a.get("id", "?"))
        for x in erros: print("     -", x)
    return n_err


def documento_app(a: dict) -> dict:
    return {k: a[k] for k in ("titulo", "conceitos", "cena", "passos")}


def preparar(filtro: str | None = None):
    if verificar(filtro):
        raise SystemExit("Há erros: corrija antes de preparar os lotes.")
    out = TRABALHO / "publicacao"; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("animacoes-lote-*.json"): f.unlink()
    escritas = [{"op": "set", "collection": "animacoes", "doc_id": a["id"], "data": documento_app(a)}
                for a in carregar(filtro) if a["status"] in ("revisado", "publicado")]
    for i in range(0, len(escritas), 50):
        (out / f"animacoes-lote-{i // 50 + 1:02d}.json").write_text(json.dumps(escritas[i:i + 50], ensure_ascii=False))
    print(f"{len(escritas)} roteiro(s) em {(len(escritas) + 49) // 50} lote(s) em {out}.")


def executar(acao: str, filtro: str | None = None):
    if acao == "verificar":
        n = verificar(filtro)
        if n: raise SystemExit(f"{n} erro(s).")
    else:
        preparar(filtro)
