"""Etapa 3: pontua cada questão pela presença de vocabulário de Física.

Gera trabalho/<prova>/triagem.csv, ordenado da maior para a menor pontuação.
É um FILTRO, não uma decisão: a lista final de questões de Física é decidida
olhando as imagens das candidatas (critério em docs/CRITERIOS.md).
"""
import csv
import json
import re

import pymupdf

from .comum import pasta_trabalho, pdf_da_prova

# termo -> peso. Unidades e grandezas pesam mais que palavras genéricas.
TERMOS = {
    r"\bm/s\b": 3, r"m/s2|m/s²": 3, r"\bkm/h\b": 2, r"\bjoules?\b|\b\d+\s?J\b": 3, r"\bwatts?\b|\b\d+\s?W\b": 3,
    r"\bnewtons?\b|\b\d+\s?N\b": 3, r"\bvolts?\b|\b\d+\s?V\b": 3, r"\bohms?\b|Ω": 3, r"\bhertz\b|\bHz\b": 3,
    r"\bpascal\b|\bPa\b": 2, r"velocidade": 2, r"aceleraç": 3, r"\bforça": 2, r"energia (cinética|potencial|elétrica|mecânica)": 3,
    r"potência": 2, r"corrente elétrica": 3, r"diferença de potencial|tensão elétrica": 3, r"resist[eê]ncia (elétrica|equivalente)|resistor": 3,
    r"\blente": 2, r"espelho (plano|côncavo|convexo|esférico)": 3, r"refração|índice de refração|reflexão": 3, r"comprimento de onda": 3,
    r"frequência": 1, r"\bcalor\b|calor específico|capacidade térmica": 2, r"temperatura": 1, r"dilatação": 3, r"pressão": 1,
    r"campo (elétrico|magnético)": 3, r"carga elétrica": 3, r"empuxo|densidade": 2, r"órbita|gravitacional|kepler": 2,
    r"quantidade de movimento|momento linear|impulso": 3, r"colisão": 2, r"torque|alavanca": 2, r"gás (ideal|perfeito)": 3,
    r"fóton|efeito fotoelétrico|nuclear|radioativ": 2, r"\bonda": 1, r"trajetória|movimento (retilíneo|circular|uniforme)": 2,
}


def executar(chave: str, limite: int = 4):
    d = pasta_trabalho(chave)
    seg = json.loads((d / "segmentos.json").read_text())
    doc = pymupdf.open(pdf_da_prova(chave))
    linhas = []
    for n, regs in seg.items():
        txt = " ".join(doc[r[0] - 1].get_text("text", clip=pymupdf.Rect(*r[1:])) for r in regs)
        txt = re.sub(r"\s+", " ", txt)
        achados, pts = [], 0
        for padrao, peso in TERMOS.items():
            k = len(re.findall(padrao, txt, flags=re.I))
            if k:
                pts += peso * min(k, 3); achados.append(re.sub(r"[\\()|?:]", "", padrao)[:18])
        linhas.append({"numero": int(n), "pontos": pts, "candidata": "sim" if pts >= limite else "",
                       "termos": "; ".join(achados[:8]), "inicio": txt[:160]})
    linhas.sort(key=lambda r: (-r["pontos"], r["numero"]))
    with open(d / "triagem.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader(); w.writerows(linhas)
    cand = sorted(r["numero"] for r in linhas if r["candidata"])
    print(f"{len(cand)} candidatas (pontos >= {limite}): {cand}")
    print(f"Detalhes em {d/'triagem.csv'}. Confira também as vizinhas de cada bloco: blocos de Física costumam ser contíguos.")
