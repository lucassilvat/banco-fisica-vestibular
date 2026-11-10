"""Linha de comando do pipeline. Use: python -m pipeline <comando> ...  (ajuda: -h)"""
import argparse
import hashlib
import json
from collections import Counter

from . import figuras, ocr, publicar, rascunho, renderizar, segmentar, site, triagem, verificar
from .comum import DADOS, RAIZ, carregar_questoes, chave_prova, taxonomia


def nums(s: str) -> list[int]:
    out = []
    for parte in s.split(","):
        a, _, b = parte.partition("-")
        out += list(range(int(a), int(b) + 1)) if b else [int(a)]
    return out


NOMES_BANCA = {"fuvest": "Fuvest", "unicamp": "Unicamp", "unesp": "Unesp", "enem": "ENEM", "acafe": "Acafe"}


def registrar_prova(a):
    a.banca = NOMES_BANCA.get(a.banca.lower(), a.banca)  # grafia única por banca (ex.: "fuvest" -> "Fuvest")
    pdf = RAIZ / "fontes" / f"{chave_prova(a.banca, a.ano, a.versao)}-{a.tipo}.pdf"
    if not pdf.exists():
        raise SystemExit(f"Copie o PDF oficial para {pdf} e rode de novo.")
    import pymupdf
    man_p = DADOS / "fontes" / "manifesto.json"; man = json.loads(man_p.read_text(encoding="utf-8"))
    reg = dict(banca=a.banca, ano=a.ano, versao=a.versao, tipo=a.tipo, descricao=a.descricao, fase=a.fase,
               arquivoLocal=str(pdf.relative_to(RAIZ)), url=a.url, sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
               paginas=len(pymupdf.open(pdf)))
    man["provas"] = [p for p in man["provas"] if p["arquivoLocal"] != reg["arquivoLocal"]] + [reg]
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Registrada: {reg['arquivoLocal']} ({reg['paginas']} páginas)")


def painel(_):
    qs = [q for _, q in carregar_questoes()]
    print(f"{len(qs)} questões | status: {dict(Counter(q['status'] for q in qs))}")
    print("por prova:", dict(sorted(Counter(f"{q['banca']} {q['ano']}{q.get('versao','')}" for q in qs).items())))
    uso = Counter(t for q in qs for t in q["topicos"])
    vazios = []
    for area in taxonomia()["areas"]:
        n = sum(uso[t["id"]] for t in area["topicos"])
        sem = [t["nome"] for t in area["topicos"] if not uso[t["id"]]]
        vazios += sem
        print(f"  {area['area']:<20} {n:>4} marcações | {len(sem)} tópico(s) sem questão")
    print(f"{len(vazios)} tópicos ainda sem nenhuma questão (bom alvo para as próximas provas).")


def main():
    p = argparse.ArgumentParser(prog="python -m pipeline", description=__doc__)
    s = p.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("registrar-prova", help="1. registra um PDF oficial em data/fontes/manifesto.json")
    r.add_argument("banca"); r.add_argument("ano", type=int); r.add_argument("--versao", default="")
    r.add_argument("--tipo", default="caderno", choices=["caderno", "gabarito", "prova-comentada"])
    r.add_argument("--descricao", required=True); r.add_argument("--fase", default="1ª fase"); r.add_argument("--url", default="")
    r.set_defaults(f=registrar_prova)
    x = s.add_parser("segmentar", help="2. divide o caderno em questões"); x.add_argument("prova")
    x.set_defaults(f=lambda a: segmentar.executar(a.prova))
    x = s.add_parser("ocr", help="2b. texto de referência por OCR (PDF com camada de texto ilegível)"); x.add_argument("prova")
    x.set_defaults(f=lambda a: ocr.executar(a.prova))
    x = s.add_parser("triagem", help="3. lista candidatas de Física"); x.add_argument("prova"); x.add_argument("--limite", type=int, default=4)
    x.set_defaults(f=lambda a: triagem.executar(a.prova, a.limite))
    x = s.add_parser("renderizar", help="4. imagens das questões (ou --grade para páginas)"); x.add_argument("prova"); x.add_argument("numeros")
    x.add_argument("--grade", action="store_true", help="interpreta 'numeros' como páginas e desenha grade")
    x.set_defaults(f=lambda a: (renderizar.grade if a.grade else renderizar.questoes)(a.prova, nums(a.numeros)))
    x = s.add_parser("rascunho", help="5. cria rascunhos das questões escolhidas"); x.add_argument("prova"); x.add_argument("numeros")
    x.set_defaults(f=lambda a: rascunho.executar(a.prova, nums(a.numeros)))
    x = s.add_parser("figuras", help="6. detectar/aplicar figuras"); x.add_argument("acao", choices=["detectar", "aplicar"])
    x.add_argument("prova"); x.add_argument("numeros")
    x.set_defaults(f=lambda a: figuras.detectar(a.prova, nums(a.numeros)) if a.acao == "detectar" else [figuras.aplicar(a.prova, n) for n in nums(a.numeros)])
    x = s.add_parser("verificar", help="8. checagens automáticas"); x.add_argument("filtro", nargs="?"); x.add_argument("--estrito", action="store_true")
    x.set_defaults(f=lambda a: verificar.executar(a.filtro, a.estrito))
    x = s.add_parser("publicar", help="9. preparar lotes / registrar figura / marcar publicadas")
    x.add_argument("acao", choices=["preparar", "registrar", "marcar"]); x.add_argument("args", nargs="*")
    x.set_defaults(f=lambda a: publicar.preparar(*(a.args[:1])) if a.acao == "preparar" else publicar.registrar(*a.args) if a.acao == "registrar" else publicar.marcar(*(a.args[:1])))
    x = s.add_parser("site", help="gera o site estático do app (GitHub Pages)"); x.add_argument("destino", nargs="?", default="site")
    x.set_defaults(f=lambda a: site.executar(a.destino))
    x = s.add_parser("painel", help="cobertura do banco por prova e por tópico"); x.set_defaults(f=painel)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
