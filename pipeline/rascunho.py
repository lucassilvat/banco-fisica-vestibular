"""Etapa 5: cria o RASCUNHO de cada questão a partir da camada de texto do PDF.

Para cada número pedido, grava data/questoes/<banca>/<ano><versao>/<id>.json com
status "rascunho", enunciado pré-extraído (com <i>, <b>, <u>, <sub>, <sup>) e campos
de resolução/tópicos vazios. Nunca sobrescreve uma questão que já exista.

O texto extraído é só um ponto de partida: fórmulas de editor de equações (MathType),
frações e textos em colunas costumam sair embaralhados. A transcrição final é feita
olhando a imagem da questão (trabalho/<prova>/imagens/qNNN.png) e conferida na
etapa "verificar".
"""
import json
from datetime import datetime, timezone

import pymupdf

from . import _extracao as ex
from .comum import caminho_questao, fonte_da_prova, id_questao, pasta_trabalho, pdf_da_prova


def executar(chave: str, numeros: list[int]):
    fonte = fonte_da_prova(chave)
    d = pasta_trabalho(chave); outdir = d / "extracao"; outdir.mkdir(exist_ok=True)
    seg = json.loads((d / "segmentos.json").read_text())
    doc = pymupdf.open(pdf_da_prova(chave))
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for n in numeros:
        body, alts, figs, compartilhado = ex.extract(doc, seg[str(n)], str(outdir), n)
        q = {"id": id_questao(fonte["banca"], fonte["ano"], fonte.get("versao", ""), n),
             "banca": fonte["banca"], "ano": fonte["ano"]}
        if fonte.get("versao"): q["versao"] = fonte["versao"]
        q.update(numero=str(n), fase=fonte.get("fase", "1ª fase"), fonte={"descricao": fonte["descricao"]},
                 enunciado="\n\n".join(body) + ("\n\n" + "\n".join(alts) if alts else ""),
                 figuras=[], gabarito="", gabaritoFonte="", resolucao="", topicos=[], status="rascunho",
                 criadoEm=agora, atualizadoEm=agora,
                 _notas={"figurasDetectadas": figs, "textoCompartilhadoDepois": compartilhado,
                         "aviso": "Rascunho automático: confira contra trabalho/<prova>/imagens antes de revisar."})
        p = caminho_questao(q)
        if p.exists():
            print(f"pulando {q['id']} (já existe em {p})"); continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"rascunho criado: {p}")
