"""Caminhos, leitura de dados e utilidades compartilhadas pelo pipeline."""
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "data"
QUESTOES = DADOS / "questoes"
FIGURAS = DADOS / "figuras"
FONTES = RAIZ / "fontes"          # PDFs oficiais (fora do git)
TRABALHO = RAIZ / "trabalho"      # área de trabalho por prova (fora do git)

STATUS = ("rascunho", "revisado", "publicado")
TIPOS = ("objetiva", "discursiva")   # ausência de "tipo" = objetiva
FIG_RE = re.compile(r"\[\[figura (\d+)\]\]")


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", t))[:80]


def taxonomia() -> dict:
    return json.loads((DADOS / "taxonomia.json").read_text(encoding="utf-8"))


def ids_topicos() -> set:
    return {t["id"] for a in taxonomia()["areas"] for t in a["topicos"]}


def manifesto() -> list:
    return json.loads((DADOS / "fontes" / "manifesto.json").read_text(encoding="utf-8"))["provas"]


def chave_prova(banca: str, ano: int, versao: str = "", edicao: str = "") -> str:
    """Identificador de uma prova: unicamp-2021A, fuvest-2024, acafe-2025-inverno, einstein-2025-prova-i...

    `edicao` separa provas da mesma banca e ano sem virar rótulo de ano no app (Acafe:
    Verão/Inverno; Einstein: Prova I/Prova II); o ano fica limpo e a edição aparece na fase."""
    return f"{banca.lower()}-{ano}{versao or ''}" + (f"-{slug(edicao)}" if edicao else "")


def fonte_da_prova(chave: str, tipo: str = "caderno") -> dict:
    for p in manifesto():
        if chave_prova(p["banca"], p["ano"], p.get("versao", ""), p.get("edicao", "")) == chave and p["tipo"] == tipo:
            return p
    raise SystemExit(f"Prova '{chave}' ({tipo}) não está em data/fontes/manifesto.json. Registre-a com: python -m pipeline registrar-prova")


def pdf_da_prova(chave: str, tipo: str = "caderno") -> Path:
    p = RAIZ / fonte_da_prova(chave, tipo)["arquivoLocal"]
    if not p.exists():
        raise SystemExit(f"PDF não encontrado em {p}. Copie o arquivo oficial para esse caminho.")
    return p


def pasta_trabalho(chave: str) -> Path:
    d = TRABALHO / chave
    d.mkdir(parents=True, exist_ok=True)
    return d


def id_questao(banca: str, ano: int, versao: str, numero, edicao: str = "") -> str:
    return f"{banca.lower()}-{ano}{(versao or '').lower()}" + (f"-{slug(edicao)}" if edicao else "") + f"-q{int(numero):02d}"


def caminho_questao(q: dict) -> Path:
    pasta = f"{q['ano']}{q.get('versao', '')}" + (f"-{slug(q['edicao'])}" if q.get("edicao") else "")
    return QUESTOES / q["banca"].lower() / pasta / f"{q['id']}.json"


def carregar_questoes(filtro: str | None = None) -> list[tuple[Path, dict]]:
    out = []
    for f in sorted(QUESTOES.rglob("*.json")):
        if filtro and filtro not in str(f):
            continue
        out.append((f, json.loads(f.read_text(encoding="utf-8"))))
    return out


def salvar_questao(q: dict) -> Path:
    p = caminho_questao(q)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def tipo_questao(q: dict) -> str:
    return q.get("tipo") or "objetiva"
