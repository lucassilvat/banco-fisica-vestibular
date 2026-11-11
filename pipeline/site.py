"""Gera o site estático do app (para GitHub Pages ou qualquer hospedagem de arquivos).

  python -m pipeline site [pasta]     (padrão: site/)

Copia app/index.html, grava questoes.json (só questões revisadas/publicadas, no mesmo
formato do banco do app, com as figuras pelo nome do arquivo) e copia as figuras usadas
para figuras/. O app detecta que está fora do Claude e lê esses arquivos.
A pasta gerada fica fora do git; o GitHub Actions (.github/workflows/pages.yml) a
gera a cada envio ao ramo main e publica no GitHub Pages.
"""
import json
import shutil
from pathlib import Path

from .comum import FIGURAS, RAIZ, carregar_questoes


CABECALHO = (
    '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<meta name="description" content="Questões de Física de vestibulares, transcritas das provas oficiais, com resolução comentada.">'
    '<style>:root{box-sizing:border-box}body{margin:0;padding:0}img{max-width:100%}'
    '[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n'
)


def documento_site(q: dict) -> dict:
    d = {k: q[k] for k in ("id", "banca", "ano", "numero", "fase", "enunciado", "gabarito", "resolucao", "topicos") if k in q}
    if q.get("versao"): d["versao"] = q["versao"]
    if q.get("tipo") == "discursiva":
        d["tipo"] = "discursiva"; d["respostas"] = q.get("respostas", [])
    d["origem"] = q["fonte"]["descricao"]
    d["figuras"] = list(q["figuras"])
    return d


def executar(destino: str = "site"):
    out = RAIZ / destino
    if out.exists(): shutil.rmtree(out)
    (out / "figuras").mkdir(parents=True)
    qs = [q for _, q in carregar_questoes() if q["status"] in ("revisado", "publicado")]
    for q in qs:
        for f in q["figuras"]:
            shutil.copy(FIGURAS / f, out / "figuras" / f)
    (out / "questoes.json").write_text(json.dumps([documento_site(q) for q in qs], ensure_ascii=False), encoding="utf-8")
    app = (RAIZ / "app" / "index.html").read_text(encoding="utf-8")
    if not app.lstrip().lower().startswith("<!doctype"):
        # app/index.html é o corpo publicado no artefato (que acrescenta o esqueleto do documento);
        # fora do Claude ele precisa do esqueleto completo, com a codificação UTF-8 declarada.
        app = (CABECALHO + app + "\n</body></html>\n")
    (out / "index.html").write_text(app, encoding="utf-8")
    (out / ".nojekyll").write_text("")
    n_fig = len(list((out / "figuras").iterdir()))
    print(f"Site gerado em {out}: {len(qs)} questões, {n_fig} figuras. Teste local: python -m http.server -d {destino}")
