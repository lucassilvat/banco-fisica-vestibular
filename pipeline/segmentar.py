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

from .comum import fonte_da_prova, pasta_trabalho, pdf_da_prova

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
                    grande = max(s["size"] for s in l["spans"]) >= 12
                    negrito = all("Bold" in s["font"] or s["flags"] & 16 for s in l["spans"] if s["text"].strip())
                    if m and not (grande or (negrito and max(s["size"] for s in l["spans"]) >= 8.5)): m = None
                else:
                    m = TITULO.fullmatch(t)
                if m and int(m.group(1)) not in achados:
                    achados[int(m.group(1))] = (pi, l["bbox"])
    return achados


# Acafe: coluna única; título "NN)" (ou só "NN", Verão 2021) em negrito no início da linha. As
# versões divulgadas trazem depois de cada questão o gabarito e a justificativa ("Dados da
# questão", "Informações da questão", "Alternativa correta letra: X"...), que ficam fora.
TITULO_ACAFE = re.compile(r"\{?(\d{2})\}?\s*(\)|$)")
FIM_ACAFE = re.compile(r"(Dados da questão|Informações da questão|Alternativa correta|Gabarito\b|Justificativa)")


def segmentos_coluna_unica(doc, margem_inferior=30, topo=20):
    W, H = doc[0].rect.width, doc[0].rect.height
    marcos = []   # (pagina, y, numero ou None para fim de questão)
    for pi, pg in enumerate(doc):
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp: continue
                t = "".join(s["text"] for s in l["spans"]).strip()
                m = TITULO_ACAFE.match(sp[0]["text"].strip()) or TITULO_ACAFE.match(t[:4])
                negrito = "Bold" in sp[0]["font"] or sp[0]["flags"] & 16
                if m and negrito and l["bbox"][0] < 120 and 1 <= int(m.group(1)) <= 90:
                    marcos.append((pi, l["bbox"][1], int(m.group(1))))
                elif FIM_ACAFE.match(t):
                    marcos.append((pi, l["bbox"][1], None))
    marcos.sort()
    # um número pode aparecer como falso título (instruções, tabelas): fica a 1ª ocorrência
    # depois da questão anterior
    escolhidos, pos = set(), (-1, -1)
    for n in sorted({m[2] for m in marcos if m[2] is not None}):
        cand = [m for m in marcos if m[2] == n and (m[0], m[1]) > pos]
        if cand: escolhidos.add(cand[0]); pos = (cand[0][0], cand[0][1])
    marcos = [m for m in marcos if m[2] is None or m in escolhidos]
    seg = {}
    for i, (pi, y, n) in enumerate(marcos):
        if n is None or n in seg: continue
        prox = marcos[i + 1] if i + 1 < len(marcos) else None
        regs, cp, cy = [], pi, y - 2
        while True:
            if prox and prox[0] == cp:
                regs.append([cp + 1, 0, cy, W, prox[1] - 2]); break
            regs.append([cp + 1, 0, cy, W, H - margem_inferior])
            if prox is None or len(regs) > 3: break
            cp, cy = cp + 1, topo
        seg[n] = [r for r in regs if r[4] - r[2] > 5]   # descarta faixa vazia quando a questão termina no fim da página
    return seg


def titulos_ocr(doc, extra=None):
    """Títulos desenhados como vetor (sem texto no PDF, ex.: Fuvest 2018): acha "NN" por OCR."""
    import subprocess, tempfile
    achados = {}; z = 150 / 72
    with tempfile.TemporaryDirectory() as tmp:
        for pi, pg in enumerate(doc):
            img = f"{tmp}/p.png"; pg.get_pixmap(dpi=150).save(img)
            tsv = subprocess.run(["tesseract", img, "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout
            for linha in tsv.splitlines()[1:]:
                c = linha.split("\t")
                if len(c) < 12 or not re.fullmatch(r"\d{2}", c[11].strip()): continue
                x, y, w, h = (int(v) / z for v in c[6:10])
                if pi == 0 or not (9 <= h <= 15 and w <= 20) or not (25 <= x <= 45 or 300 <= x <= 320): continue   # número na margem da coluna
                n = int(c[11])
                if n not in achados: achados[n] = (pi, (x, y, x + w, y + h))
    for n, (pi, bb) in json.loads(open(ajuste).read()).items() if (ajuste := extra) else []:
        achados[int(n)] = (pi, bb)
    return achados


def segmentos(doc, margem_inferior=30, topo=40, so_numero=False, extra=None):
    W, H = doc[0].rect.width, doc[0].rect.height
    t = titulos(doc, so_numero)
    if so_numero and len(t) < 10:
        t = titulos_ocr(doc, extra)
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


# Largura total (Einstein, Prova II discursiva): uma questão por página, em coluna única; a
# questão termina no quadro "RESOLUÇÃO E RESPOSTA" (espaço do candidato), que fica fora.
# O texto "RASCUNHO" em marca d'água no meio da página é ignorado.
FIM_LARGURA_TOTAL = re.compile(r"RESOLU[ÇC][ÃA]O E RESPOSTA", re.I)


def segmentos_largura_total(doc, margem_inferior=30):
    W, H = doc[0].rect.width, doc[0].rect.height
    t = titulos(doc); seg = {}
    for n, (pi, bb) in sorted(t.items()):
        fim = None
        for b in doc[pi].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                s = "".join(x["text"] for x in l["spans"]).strip()
                if FIM_LARGURA_TOTAL.search(s) and l["bbox"][1] > bb[1]:
                    fim = min(fim or 1e9, l["bbox"][1])
        seg[n] = [[pi + 1, 0, bb[1] - 2, W, (fim or H - margem_inferior) - 2]]
    return seg


def executar(chave: str):
    doc = pymupdf.open(pdf_da_prova(chave))
    extra = pasta_trabalho(chave) / "titulos-ajustes.json"   # {"11": [pagina0, [x0,y0,x1,y1]]} para títulos que o OCR não achou
    if chave.startswith("acafe"):
        seg = segmentos_coluna_unica(doc)
    elif fonte_da_prova(chave).get("layout") == "largura-total":
        seg = segmentos_largura_total(doc)
    else:
        seg = segmentos(doc, so_numero=chave.startswith("fuvest"), extra=str(extra) if extra.exists() else None)
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
