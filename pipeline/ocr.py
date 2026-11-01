"""Texto de referência por OCR, para cadernos cuja camada de texto é ilegível.

Alguns PDFs oficiais (ex.: Fuvest 2021, "Caderno Reserva") têm fontes com codificação
própria: o pdftotext devolve símbolos sem sentido. Nesses casos:

  python -m pipeline ocr fuvest-2021

renderiza cada página a 300 dpi, roda o Tesseract (português) e grava
fontes/<arquivo>.ocr.txt (fora do git, como o PDF). Também marca a prova no manifesto
com "camadaTexto": "ocr"; a etapa verificar passa a conferir a fidelidade contra esse
texto. O OCR erra letras isoladas, então os avisos de fidelidade dessas provas precisam
de conferência visual na imagem antes de virarem divergências aceitas.
"""
import json
import subprocess
import tempfile
from pathlib import Path

import pymupdf

from .comum import DADOS, RAIZ, chave_prova, fonte_da_prova, pdf_da_prova


def arquivo_ocr(chave: str) -> Path:
    pdf = RAIZ / fonte_da_prova(chave)["arquivoLocal"]
    return pdf.with_suffix(".ocr.txt")


def executar(chave: str, dpi: int = 300):
    doc = pymupdf.open(pdf_da_prova(chave)); partes = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, pg in enumerate(doc, 1):
            img = Path(tmp) / f"p{i:02d}.png"; pg.get_pixmap(dpi=dpi).save(img)
            txt = subprocess.run(["tesseract", str(img), "-", "-l", "por", "--psm", "1"], capture_output=True, text=True).stdout
            partes.append(f"=== página {i}\n{txt}")
    out = arquivo_ocr(chave); out.write_text("\n".join(partes), encoding="utf-8")
    man_p = DADOS / "fontes" / "manifesto.json"; man = json.loads(man_p.read_text(encoding="utf-8"))
    for p in man["provas"]:
        if chave_prova(p["banca"], p["ano"], p.get("versao", "")) == chave and p["tipo"] == "caderno":
            p["camadaTexto"] = "ocr"
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OCR de {len(doc)} páginas em {out}; manifesto marcado com camadaTexto = ocr.")
