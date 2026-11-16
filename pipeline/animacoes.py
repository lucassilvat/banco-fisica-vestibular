r"""Resoluções animadas (adicionais à resolução comentada; não a substituem).

  python -m pipeline animacoes verificar [filtro]
  python -m pipeline animacoes preparar  [filtro]   -> trabalho/publicacao/animacoes-lote-NN.json

Cada roteiro fica em data/animacoes/<id da questão>.json (esquema em
schemas/animacao.schema.json e explicação em docs/ANIMACOES.md). O roteiro escolhe um
modelo de cena (desenhado pelo player do app) e descreve os passos: conceito físico,
texto, equações e o que a cena mostra. Sem perguntas ao aluno e sem controles para ele
mudar valores (decisão do Lucas).

Os nomes de elementos e de estado aceitos por modelo (MODELOS) precisam bater com os
modelos de cena de app/index.html (CENAS).
"""
import json
from pathlib import Path
import re

from .comum import DADOS, TRABALHO, carregar_questoes
from .verificar import checar_latex

ANIMACOES = DADOS / "animacoes"

MODELOS = {
    "plano-inclinado": {
        "parametros": {"senTheta", "cosTheta", "mu", "g"},
        "elementos": {"rampa", "angulo", "caixa", "peso", "normal", "atrito", "eixos", "componentes",
                      "angulo-peso", "aceleracao", "balanco"},
        "estado": {"movimento": {"repouso", "acelerando"}},
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
    "mhs-sombra": {
        "parametros": {"amplitude", "periodo", "t1", "t2"},
        "elementos": {"pendulo", "sombra", "vetor-v", "grafico", "ponto-1", "ponto-2", "secante"},
        "estado": {"t": None, "cursor": {True, False}},
    },
    "rotacao-latitude": {
        "parametros": {"latitude"},
        "elementos": {"terra", "eixo", "equador", "paralelo", "latitude", "morador", "gravidade", "centripeta", "angulo", "alternos"},
        "estado": {"girar": {True, False}},
    },
    "cadeia-energia": {
        "parametros": {"etapas", "altura"},
        "elementos": {f"etapa-{k}" for k in range(1, 9)} | {"subida"},
        "estado": {"subir": {True, False}},
    },
    "espelho-convexo": {
        "parametros": {"f", "d0", "d1", "t1"},
        "elementos": {"eixo", "muro", "espelho", "foco", "imagem", "cotas"},
        "estado": {"d": None, "mover": {True, False}},
    },
    "espectro-fototropismo": {
        "parametros": {"azul"},
        "elementos": {"espectro", "azul", "setas", "luz", "planta", "lados", "auxina"},
        "estado": {"curvar": {True, False}},
    },
    "campo-uniforme": {
        "parametros": {"U", "dTexto"},
        "elementos": {"placas", "tensao", "cota-d", "campo", "ion", "forca"},
        "estado": {"mover": {True, False}},
    },
    "rotas-velocidade-media": {"parametros": {"rotas"}, "elementos": {"rotas", "tempos", "totais", "veiculos"}, "estado": {"percorrer": {True, False}}},
    "engrenagens-internas": {"parametros": {"razao"}, "elementos": {"roda", "engrenagem-a", "engrenagem-b", "manivela", "contato", "raios"}, "estado": {"girar": {True, False}}},
    "lancamento-obliquo": {"parametros": {"coef", "xC", "tB", "tC", "vx", "vy"}, "elementos": {"terreno", "eixos", "trajetoria", "pontos", "vertice", "componentes", "velocidade-b", "bola"}, "estado": {"lancar": {True, False}, "t": None}},
    "manometro-gas": {"parametros": set(), "elementos": {"recipiente", "gas", "mercurio", "patm", "desnivel", "pressoes"}, "estado": {}},
    "aumento-linear": {"parametros": {"i1", "A1", "A2"}, "elementos": {"imagem-1", "objeto", "imagem-2"}, "estado": {}},
    "onda-corda": {"parametros": {"lambda", "f", "dist"}, "elementos": {"pino", "corda", "frente", "cotas"}, "estado": {"propagar": {True, False}}},
    "soma-potencias": {"parametros": {"U", "imax", "limite", "base", "alternativas"}, "elementos": {"limite", "base", "alt-a", "alt-b", "alt-c", "alt-d", "alt-e"}, "estado": {}},
    "grafico-modulo": {"parametros": {"zero", "coef", "xs", "ys", "marcasX", "rotX", "rotY", "rotReta", "rotModulo", "rotPonto0"}, "elementos": {"eixos", "reta", "modulo", "ponto-zero", "ponto-0"}, "estado": {"dobrar": {True, False}}},
    "triangulo-pg": {"parametros": set(), "elementos": {"triangulo", "particula", "tempos", "soma"}, "estado": {"percorrer": {True, False}}},
    "indicador-combustivel": {
        "parametros": set(),
        "elementos": {"tanque", "reostato", "circuito", "corrente", "lamina", "mostrador", "zoom"},
        "estado": {"nivel": None},
    },
}
OBRIG = ["id", "titulo", "conceitos", "cena", "passos", "status"]
# Revisão do Lucas, feita no app do Claude (coleção "revisoes"). Só as aprovadas vão para o site público.
REV_ESTADOS = ("nao-revisada", "comentada", "aprovada")


def estado_revisao(a: dict) -> str:
    return (a.get("revisao") or {}).get("estado", "nao-revisada")
TAGS_OK = re.compile(r"</?(i|b|u|sub|sup)>")


def carregar(filtro: str | None = None) -> list[dict]:
    out = []
    for f in sorted(ANIMACOES.glob("*.json")):
        if filtro and filtro not in f.name:
            continue
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


FORMAS = {"ret": {"x", "y", "w", "h"}, "circ": {"x", "y", "r"}, "linha": {"pontos"}, "caminho": {"d"}, "seta": {"de", "para"},
          "vetor": {"x", "y", "letra"}, "texto": {"x", "y", "txt"}, "rotulo": {"x", "y", "txt"}, "angulo": {"centro", "de", "ate"},
          "cota": {"de", "para"}}


def checar_diagrama(par: dict) -> list[str]:
    """Modelo genérico: formas conhecidas, com os campos obrigatórios; animações com alvo existente."""
    e = []
    els = par.get("elementos", {})
    if not els: e.append("diagrama sem elementos")
    for id_, formas in els.items():
        for f in formas:
            req = FORMAS.get(f.get("t"))
            if req is None: e.append(f"elemento {id_}: forma desconhecida {f.get('t')}"); continue
            falta = req - set(f)
            if falta: e.append(f"elemento {id_}: forma {f['t']} sem {', '.join(sorted(falta))}")
    for n, an in par.get("animacoes", {}).items():
        if an.get("alvo") not in els: e.append(f"animação {n}: alvo inexistente {an.get('alvo')}")
        if an.get("tipo") not in ("trajeto", "girar", "oscilar", "aparecer", "escalar", "esticar"): e.append(f"animação {n}: tipo desconhecido {an.get('tipo')}")
        for f in an.get("fases", []):
            if not f.get("duracao"): e.append(f"animação {n}: fase sem duracao")
            if an.get("tipo") == "trajeto" and len(f.get("pontos", [])) < 2: e.append(f"animação {n}: fase sem pontos")
            if an.get("tipo") == "esticar" and ("de" not in f or "ate" not in f or not (f.get("centro") or an.get("centro"))): e.append(f"animação {n}: fase de esticar sem de/ate/centro")
            v = f.get("velocidades")
            if v is not None and (len(v) != 2 or min(v) < 0): e.append(f"animação {n}: velocidades inválidas {v}")
    return e


def checar_aula(a: dict, q: dict) -> list[str]:
    """Formato "aula" (v2.15.0): abertura e métodos em telas; blocos texto / eq / gabarito / fim."""
    e = [f"falta o campo {k}" for k in ("id", "titulo", "conceitos", "metodos", "status") if k not in a]
    if e: return e
    for k in a:
        if k not in ("id", "formato", "titulo", "conceitos", "cena", "abertura", "metodos", "status", "revisao", "criadoEm", "atualizadoEm"):
            e.append(f"campo não aceito: {k}")
    if a["status"] not in ("rascunho", "revisado", "publicado"): e.append(f"status inválido {a['status']}")
    elementos, anims, estados = set(), set(), {}
    if "cena" in a:
        modelo = a["cena"].get("modelo")
        par = a["cena"].get("parametros", {})
        if modelo == "diagrama":
            e += checar_diagrama(par); elementos = set(par.get("elementos", {})); anims = set(par.get("animacoes", {}))
        elif modelo in MODELOS:  # modelo pronto do app (ex.: indicador-combustivel), com estado por tela
            m = MODELOS[modelo]; elementos = set(m["elementos"]); estados = m["estado"]
            for k in par:
                if k not in m["parametros"]: e.append(f"parâmetro desconhecido no modelo: {k}")
        else: e.append(f"modelo de cena desconhecido: {modelo}")
    def telas(lista, nome):
        for i, t in enumerate(lista, 1):
            onde = f"{nome}, tela {i}"
            for k in t:
                if k not in ("titulo", "cena", "blocos"): e.append(f"{onde}: campo não aceito: {k}")
            for x in t.get("cena", {}).get("mostrar", []):
                if x not in elementos: e.append(f"{onde}: elemento desconhecido: {x}")
            for x in t.get("cena", {}).get("animar", []):
                if x not in anims: e.append(f"{onde}: animação desconhecida: {x}")
            for k in t.get("cena", {}):
                if k not in ("mostrar", "animar", "estado", "destacar"): e.append(f"{onde}: campo de cena não aceito: {k}")
            for x in t.get("cena", {}).get("destacar", []):
                if x not in t.get("cena", {}).get("mostrar", []): e.append(f"{onde}: destacar só vale para elemento mostrado: {x}")
            for k, v in t.get("cena", {}).get("estado", {}).items():
                if k not in estados: e.append(f"{onde}: estado desconhecido: {k}"); continue
                if estados[k] is not None and v not in estados[k]: e.append(f"{onde}: valor inválido para {k}: {v}")
            if not t.get("blocos"): e.append(f"{onde}: sem blocos")
            ultima = None
            for j, b in enumerate(t.get("blocos", []), 1):
                ob = f"{onde}, bloco {j}"
                tipo = b.get("t")
                if tipo == "texto":
                    e.extend(checar_latex(b.get("html", ""), ob))
                    resto = TAGS_OK.sub("", re.sub(r"\\\(.+?\\\)", "", b.get("html", "")))
                    if re.search(r"<[a-zA-Z/]", resto): e.append(f"{ob}: marcação HTML não aceita")
                elif tipo == "eq":
                    tex = b.get("tex", "")
                    e.extend(checar_latex("\\(" + tex + "\\)", ob))
                    marcas = set(re.findall(r"\\marca\{([^}]+)\}", tex))
                    for id_ in b.get("cancelar", []):
                        if ultima is None or id_ not in ultima: e.append(f"{ob}: cancelar {id_}: a equação anterior não tem essa marca")
                    for id_ in b.get("mover", []):
                        if ultima is None or id_ not in ultima or id_ not in marcas: e.append(f"{ob}: mover {id_}: a marca precisa estar nas duas equações")
                    ultima = marcas
                elif tipo == "gabarito":
                    if q.get("gabarito") and b.get("letra", "").upper() != q["gabarito"].upper(): e.append(f"{ob}: gabarito {b.get('letra')} ≠ {q['gabarito']}")
                elif tipo != "fim":
                    e.append(f"{ob}: tipo de bloco desconhecido: {tipo}")
    telas(a.get("abertura", []), "abertura")
    if not a["metodos"]: e.append("sem métodos")
    for m in a["metodos"]:
        if not m.get("nome"): e.append("método sem nome")
        telas(m.get("telas", []), f"método {m.get('nome')}")
        blocos = [b for t in m.get("telas", []) for b in t.get("blocos", [])]
        if q.get("gabarito") and not any(b.get("t") == "gabarito" for b in blocos[-3:]):
            e.append(f"método {m.get('nome')}: termina sem o gabarito")
    return e


def checar(a: dict, questoes: dict) -> list[str]:
    if a.get("formato") == "aula":
        q = questoes.get(a.get("id"))
        if not q: return [f"não existe questão {a.get('id')}"]
        e = checar_aula(a, q)
        if "revisao" in a and (not isinstance(a["revisao"], dict) or a["revisao"].get("estado") not in REV_ESTADOS): e.append("revisao inválida")
        return e
    e = [f"falta o campo {k}" for k in OBRIG if k not in a]
    if e: return e
    q = questoes.get(a["id"])
    if not q: return [f"não existe questão {a['id']}"]
    if a["status"] not in ("rascunho", "revisado", "publicado"): e.append(f"status inválido {a['status']}")
    if "revisao" in a:
        r = a["revisao"]
        if not isinstance(r, dict) or r.get("estado") not in REV_ESTADOS: e.append(f"revisao inválida: {r}")
    m = MODELOS.get(a["cena"].get("modelo"))
    if a["cena"].get("modelo") == "diagrama":
        e += checar_diagrama(a["cena"].get("parametros", {}))
        par = a["cena"].get("parametros", {})
        m = {"parametros": {"largura", "altura", "elementos", "animacoes"}, "elementos": set(par.get("elementos", {})),
             "estado": {"animar": None}}
        for p in a["passos"]:
            for n in p.get("cena", {}).get("estado", {}).get("animar", []):
                if n not in par.get("animacoes", {}): e.append(f"animação desconhecida: {n}")
    if not m: return e + [f"modelo de cena desconhecido: {a['cena'].get('modelo')}"]
    for k in a["cena"].get("parametros", {}):
        if k not in m["parametros"]: e.append(f"parâmetro desconhecido no modelo: {k}")
    if not a["passos"]: e.append("roteiro sem passos")
    for i, p in enumerate(a["passos"], 1):
        onde = f"passo {i}"
        for k in ("titulo", "texto"):
            if not p.get(k): e.append(f"{onde}: falta {k}")
        textos = [("texto", p.get("texto", ""))] + [(f"equação {j}", "\\(" + x + "\\)") for j, x in enumerate(p.get("equacoes", []), 1)]
        for k in p:
            if k not in ("titulo", "conceito", "texto", "equacoes", "cena"): e.append(f"{onde}: campo não aceito: {k}")
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
        if f"({q['gabarito'].upper()})" not in ultimo.upper():
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
    if a.get("formato") == "aula":
        return {k: a[k] for k in ("formato", "titulo", "conceitos", "cena", "abertura", "metodos") if k in a}
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


def importar_revisoes(arquivo: str):
    """Grava nos roteiros as revisões exportadas da coleção "revisoes" do app.

    Aceita uma lista de documentos ({"id", "data"}, como sai do banco) ou um objeto {id: dados}."""
    bruto = json.loads(Path(arquivo).read_text(encoding="utf-8"))
    docs = {d["id"]: d.get("data", {}) for d in bruto} if isinstance(bruto, list) else bruto
    n = 0
    for id_, r in docs.items():
        f = ANIMACOES / f"{id_}.json"
        if not f.exists():
            print(f"aviso: não há roteiro para {id_}"); continue
        if r.get("estado") not in REV_ESTADOS:
            print(f"aviso: estado inválido em {id_}: {r.get('estado')}"); continue
        a = json.loads(f.read_text(encoding="utf-8"))
        novo = {"estado": r["estado"], "comentario": r.get("comentario", ""), "atualizadoEm": r.get("atualizadoEm", "")}
        if a.get("revisao") != novo:
            a["revisao"] = novo
            f.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); n += 1
    print(f"{n} roteiro(s) atualizado(s).")
    resumo()


def resumo():
    cont = {k: 0 for k in REV_ESTADOS}
    for a in carregar(): cont[estado_revisao(a)] += 1
    print("Revisão: " + ", ".join(f"{v} {k}" for k, v in cont.items()) + " (só as aprovadas vão para o site público).")


def executar(acao: str, filtro: str | None = None):
    if acao == "revisoes":
        if not filtro: raise SystemExit("Uso: python -m pipeline animacoes revisoes <arquivo.json>")
        importar_revisoes(filtro); return
    if acao == "resumo":
        resumo(); return
    if acao == "verificar":
        n = verificar(filtro)
        if n: raise SystemExit(f"{n} erro(s).")
    else:
        preparar(filtro)
