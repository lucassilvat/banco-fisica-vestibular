"""Etapa 6: recorta as figuras de cada questão.

  detectar <prova> <numeros>  -> trabalho/<prova>/figuras/caixas.json + recortes + folha-contato.png
  Ajustes manuais: trabalho/<prova>/figuras/ajustes.json  {"36": [[pagina, x0, y0, x1, y1], ...]}
  (coordenadas em pontos PDF; use a imagem de grade da etapa renderizar). Caixas
  ajustadas não passam pelo corte automático de texto.

As caixas saem ordenadas por coluna e depois de cima para baixo, que é a ordem de
leitura; em alternativas-figura isso dá a), b), c), d).
Depois de conferir a folha de contato, copie para a questão com:
  python -m pipeline figuras aplicar <prova> <numero>
"""
import json
import re
import shutil

import pymupdf
from PIL import Image, ImageDraw

from .comum import FIGURAS, carregar_questoes, id_questao, fonte_da_prova, pasta_trabalho, pdf_da_prova, salvar_questao

ALT = re.compile(r"^[a-e]\)")


def _agrupar(caixas, folga):
    caixas = [pymupdf.Rect(b) for b in caixas]
    mudou = True
    while mudou:
        mudou = False; out = []
        for r in caixas:
            for i, o in enumerate(out):
                if (o + (-folga, -folga, folga, folga)).intersects(r):
                    out[i] = o | r; mudou = True; break
            else:
                out.append(pymupdf.Rect(r))
        caixas = out
    return caixas


def _detectar(doc, regioes):
    figs = []
    for p, x0, y0, x1, y1 in regioes:
        pg = doc[p - 1]; R = pymupdf.Rect(x0, y0, x1, y1); partes = []
        for d in pg.get_drawings():
            r = d["rect"]
            if not R.intersects(r) or r.y0 < 60: continue
            if r.width < 3 and r.height > 120: continue      # fios de coluna
            if r.height < 18 and r.width > 180: continue     # tarjas de título
            if r.get_area() > 0 and (r & R).get_area() < 0.5 * r.get_area(): continue
            partes.append(r)
        for im in pg.get_image_info():
            r = pymupdf.Rect(im["bbox"])
            if r.y0 > 60 and R.intersects(r) and (r & R).get_area() > 0.5 * r.get_area(): partes.append(r & R)
        cl = [c for c in _agrupar(partes, 10) if c.width > 20 and c.height > 15]
        linhas = []
        for b in pg.get_text("dict", clip=R)["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if t: linhas.append((pymupdf.Rect(l["bbox"]), t))
        for _ in range(3):  # absorve rótulos curtos (eixos, nomes de componentes)
            for lb, t in linhas:
                if len(t) > 32 or ALT.match(t) or t.startswith(("QUEST", "(")): continue
                if (26 <= lb.x0 <= 36 or 304 <= lb.x0 <= 318) and lb.width > 40: continue
                for i, c in enumerate(cl):
                    if (c + (-16, -16, 16, 16)).intersects(lb): cl[i] = c | lb
            cl = _agrupar(cl, 6)
        cl.sort(key=lambda c: (0 if (c.x0 + c.x1) / 2 < pg.rect.width / 2 else 1, c.y0))
        figs += [[p] + [round(v, 1) for v in ((c + (-4, -4, 4, 4)) & pg.rect)] for c in cl]
    return figs


def _aparar(pg, R):
    """Remove linhas de parágrafo e alternativas grudadas no topo/rodapé da caixa."""
    for _ in range(6):
        mudou = False
        for b in pg.get_text("dict", clip=R)["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip(); lb = pymupdf.Rect(l["bbox"])
                if not t: continue
                paragrafo = lb.width > 90 or 26 <= lb.x0 <= 36 or 304 <= lb.x0 <= 318 or ALT.match(t) or t.startswith(("(", "Dado"))
                if not paragrafo: continue
                if lb.y0 < R.y0 + 24 and lb.y1 < R.y0 + 30 and lb.y1 < R.y1:
                    R.y0 = lb.y1 + 1; mudou = True
                elif lb.y1 >= R.y1 - 24 and lb.y0 > R.y0:
                    R.y1 = lb.y0 - 1; mudou = True
        if not mudou: break
    return R


def detectar(chave: str, numeros: list[int]):
    d = pasta_trabalho(chave); out = d / "figuras"; out.mkdir(exist_ok=True)
    seg = json.loads((d / "segmentos.json").read_text())
    ajustes = json.loads((out / "ajustes.json").read_text()) if (out / "ajustes.json").exists() else {}
    doc = pymupdf.open(pdf_da_prova(chave)); caixas = {}; tiles = []
    for n in numeros:
        manual = str(n) in ajustes
        bxs = ajustes[str(n)] if manual else _detectar(doc, seg[str(n)])
        res = []
        for velho in out.glob(f"q{n:03d}-*.png"): velho.unlink()   # recortes de uma rodada anterior
        for k, (p, a, b, c, e) in enumerate(bxs, 1):
            pg = doc[p - 1]; R = pymupdf.Rect(a, b, c, e)
            if not manual: R = _aparar(pg, R)
            res.append([p, round(R.x0, 1), round(R.y0, 1), round(R.x1, 1), round(R.y1, 1)])
            pg.get_pixmap(dpi=200, clip=R).save(out / f"q{n:03d}-{k}.png")
            pix = pg.get_pixmap(dpi=40, clip=R); im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            t = Image.new("RGB", (max(im.width, 70), im.height + 12), "white"); t.paste(im, (0, 12))
            ImageDraw.Draw(t).text((1, 0), f"Q{n}.{k}{' (manual)' if manual else ''}", fill=(220, 0, 0)); tiles.append(t)
        caixas[str(n)] = res
    (out / "caixas.json").write_text(json.dumps(caixas, indent=1))
    if tiles:
        W = 900; x = y = rh = 0; pos = []
        for t in tiles:
            if x + t.width > W: x = 0; y += rh + 6; rh = 0
            pos.append((x, y)); x += t.width + 8; rh = max(rh, t.height)
        s = Image.new("RGB", (W, y + rh + 2), "white")
        for t, q in zip(tiles, pos): s.paste(t, q)
        s.save(out / "folha-contato.png")
    print(f"{sum(map(len, caixas.values()))} figuras. Confira {out/'folha-contato.png'}; corrija em {out/'ajustes.json'} e rode de novo.")


def aplicar(chave: str, numero: int):
    """Copia os recortes aprovados para data/figuras e preenche o campo 'figuras' da questão."""
    fonte = fonte_da_prova(chave); out = pasta_trabalho(chave) / "figuras"
    qid = id_questao(fonte["banca"], fonte["ano"], fonte.get("versao", ""), numero, fonte.get("edicao", ""))
    alvo = [q for _, q in carregar_questoes(qid) if q["id"] == qid]
    if not alvo: raise SystemExit(f"Questão {qid} não existe. Rode 'rascunho' antes.")
    q = alvo[0]; nomes = []
    for src in sorted(out.glob(f"q{numero:03d}-*.png"), key=lambda p: int(p.stem.split("-")[1])):
        nome = f"{qid}-{src.stem.split('-')[1]}.png"; shutil.copy(src, FIGURAS / nome); nomes.append(nome)
    q["figuras"] = nomes; salvar_questao(q)
    print(f"{qid}: {len(nomes)} figura(s) aplicadas. Posicione cada uma no enunciado com [[figura N]].")
