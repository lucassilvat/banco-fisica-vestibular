"""Etapa 2: divide o caderno em questões a partir dos títulos "QUESTÃO N" (Fuvest: só "NN").

Gera trabalho/<prova>/segmentos.json  {numero: [[pagina, x0, y0, x1, y1], ...]}
e   trabalho/<prova>/segmentos.txt    (início de cada questão, para conferência rápida)

Supõe layout em duas colunas (padrão Comvest/Fuvest/Vunesp). A coluna de cada título
é decidida pelo CENTRO da linha, não pela borda esquerda (títulos deslocados existem,
ex.: Unicamp 2019, questão 36).
"""
import json
import re

import pymupdf

from .comum import pasta_trabalho, pdf_da_prova

TITULO = re.compile(r"QUEST[ÃA]O\s+(\d+)", re.I)
# Fuvest: o título é só o número ("01", ou "{ 01}" a partir de 2025), em corpo >= 12 pt
TITULO_NUMERO = re.compile(r"\{?\s*(\d{2})\s*\}?")


def titulos(doc, so_numero=False):
    achados = {}
    for pi, pg in enumerate(doc):
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if so_numero:
                    m = TITULO_NUMERO.fullmatch(t)
                    if m and max(s["size"] for s in l["spans"]) < 12: m = None
                else:
                    m = TITULO.fullmatch(t)
                if m and int(m.group(1)) not in achados:
                    achados[int(m.group(1))] = (pi, l["bbox"])
    return achados


def segmentos(doc, margem_inferior=30, topo=40, so_numero=False):
    W, H = doc[0].rect.width, doc[0].rect.height
    t = titulos(doc, so_numero)
    itens = sorted((pi, 0 if (bb[0] + bb[2]) / 2 < W / 2 else 1, bb[1], n) for n, (pi, bb) in t.items())
    seg = {}
    for i, (pi, col, y, n) in enumerate(itens):
        prox = itens[i + 1] if i + 1 < len(itens) else None
        regs, cp, cc, cy = [], pi, col, y - 2
        while True:
            x0, x1 = (0, W / 2) if cc == 0 else (W / 2 - 25, W)
            if prox and (prox[0], prox[1]) == (cp, cc):
                regs.append([cp + 1, x0, cy, x1, prox[2] - 2]); break
            regs.append([cp + 1, x0, cy, x1, H - margem_inferior])
            if prox is None or len(regs) > 4: break
            cp, cc, cy = (cp, 1, topo) if cc == 0 else (cp + 1, 0, topo)
        seg[n] = regs
    return seg


def executar(chave: str):
    doc = pymupdf.open(pdf_da_prova(chave))
    seg = segmentos(doc, so_numero=chave.startswith("fuvest"))
    d = pasta_trabalho(chave)
    (d / "segmentos.json").write_text(json.dumps(seg, indent=1))
    linhas = []
    for n in sorted(seg):
        txt = " ".join(doc[r[0] - 1].get_text("text", clip=pymupdf.Rect(*r[1:])) for r in seg[n])
        linhas.append(f"{n:03d} | {re.sub(r'\s+', ' ', txt)[:220]}")
    (d / "segmentos.txt").write_text("\n".join(linhas), encoding="utf-8")
    print(f"{len(seg)} questões encontradas em {chave}. Arquivos: {d/'segmentos.json'}, {d/'segmentos.txt'}")
    faltando = [n for n in range(1, max(seg) + 1) if n not in seg] if seg else []
    if faltando:
        print("ATENÇÃO: números de questão ausentes:", faltando)
