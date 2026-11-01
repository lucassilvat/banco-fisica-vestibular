"""Etapa 4: gera imagens para leitura humana (ou do Claude).

  questao  -> trabalho/<prova>/imagens/qNNN.png  (a questão inteira, colunas empilhadas)
  grade    -> trabalho/<prova>/imagens/pagina-NN-grade.png (página com grade em pontos PDF,
              para escolher caixas de figura à mão)
"""
import json

import pymupdf
from PIL import Image, ImageDraw

from .comum import pasta_trabalho, pdf_da_prova


def questoes(chave: str, numeros: list[int], dpi: int = 110):
    d = pasta_trabalho(chave); out = d / "imagens"; out.mkdir(exist_ok=True)
    seg = json.loads((d / "segmentos.json").read_text())
    doc = pymupdf.open(pdf_da_prova(chave))
    for n in numeros:
        ims = []
        for p, x0, y0, x1, y1 in seg[str(n)]:
            pg = doc[p - 1]; r = pymupdf.Rect(x0, y0, x1, y1)
            blocos = [pymupdf.Rect(b[:4]) for b in pg.get_text("blocks", clip=r)]
            if blocos:
                u = blocos[0]
                for b in blocos: u |= b
                r = (u & r) + (-2, -2, 2, 2)
            pix = pg.get_pixmap(dpi=dpi, clip=r)
            ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        W = max(i.width for i in ims); H = sum(i.height + 6 for i in ims)
        m = Image.new("RGB", (W, H), "white"); y = 0
        for i in ims: m.paste(i, (0, y)); y += i.height + 6
        m.save(out / f"q{n:03d}.png")
    print(f"{len(numeros)} imagens em {out}")


def grade(chave: str, paginas: list[int]):
    d = pasta_trabalho(chave); out = d / "imagens"; out.mkdir(exist_ok=True)
    doc = pymupdf.open(pdf_da_prova(chave)); z = 0.9
    for p in paginas:
        pix = doc[p - 1].get_pixmap(matrix=pymupdf.Matrix(z, z))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im)
        for v in range(0, 850, 25):
            c = (255, 0, 0) if v % 100 == 0 else (255, 190, 190)
            if v <= 600: dr.line([(v * z, 0), (v * z, im.height)], fill=c)
            dr.line([(0, v * z), (im.width, v * z)], fill=c)
            if v % 100 == 0:
                dr.text((v * z + 2, 2), str(v), fill=(255, 0, 0)); dr.text((2, v * z + 2), str(v), fill=(255, 0, 0))
        im.save(out / f"pagina-{p:02d}-grade.png")
    print(f"Grades em {out} (coordenadas em pontos PDF)")
