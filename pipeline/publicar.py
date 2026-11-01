"""Etapa 9: prepara a publicação no app atual (artefato do Claude com banco de dados).

  preparar   -> trabalho/publicacao/figuras-para-enviar.txt  (figuras novas ou alteradas)
                trabalho/publicacao/lote-NN.json             (até 50 documentos por lote)
  registrar  -> grava o assetId devolvido pelo upload de uma figura em data/figuras-publicadas.json

Só questões com status "revisado" ou "publicado" entram nos lotes. Depois de gravar os
lotes no banco do app, rode 'publicar marcar' para mudar "revisado" -> "publicado".

O formato do documento no app é o da coleção "questoes" (ver docs/MODELO-DE-DADOS.md).
Quando o projeto virar SaaS, só esta etapa muda: os dados em data/ continuam iguais.
"""
import hashlib
import json

from .comum import DADOS, FIGURAS, TRABALHO, carregar_questoes, salvar_questao

REG = DADOS / "figuras-publicadas.json"


def _registro():
    return json.loads(REG.read_text()) if REG.exists() else {}


def _sha(nome):
    return hashlib.sha256((FIGURAS / nome).read_bytes()).hexdigest()


def documento_app(q: dict, reg: dict) -> dict:
    d = {k: q[k] for k in ("banca", "ano", "numero", "fase", "enunciado", "gabarito", "resolucao", "topicos", "criadoEm", "atualizadoEm") if k in q}
    if q.get("versao"): d["versao"] = q["versao"]
    d["origem"] = q["fonte"]["descricao"]
    d["figuras"] = [reg[f]["assetId"] for f in q["figuras"]]
    return d


def preparar(filtro: str | None = None):
    reg = _registro(); out = TRABALHO / "publicacao"; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("lote-*.json"): f.unlink()
    qs = [q for _, q in carregar_questoes(filtro) if q["status"] in ("revisado", "publicado")]
    enviar = sorted({f for q in qs for f in q["figuras"] if f not in reg or reg[f]["sha256"] != _sha(f)})
    (out / "figuras-para-enviar.txt").write_text("\n".join(str(FIGURAS / f) for f in enviar))
    if enviar:
        print(f"{len(enviar)} figura(s) precisam ser enviadas antes (lista em {out/'figuras-para-enviar.txt'}).")
        print("Depois de cada upload: python -m pipeline publicar registrar <arquivo.png> <assetId>")
        return
    escritas = [{"op": "set", "collection": "questoes", "doc_id": q["id"], "data": documento_app(q, reg)} for q in qs]
    for i in range(0, len(escritas), 50):
        (out / f"lote-{i // 50 + 1:02d}.json").write_text(json.dumps(escritas[i:i + 50], ensure_ascii=False))
    print(f"{len(escritas)} documento(s) em {(len(escritas) + 49) // 50} lote(s) em {out}.")


def registrar(arquivo: str, asset_id: str):
    reg = _registro(); nome = arquivo.split("/")[-1]
    reg[nome] = {"assetId": asset_id, "sha256": _sha(nome)}
    REG.write_text(json.dumps(reg, indent=1, sort_keys=True))
    print(f"{nome} -> {asset_id}")


def marcar(filtro: str | None = None):
    n = 0
    for _, q in carregar_questoes(filtro):
        if q["status"] == "revisado":
            q["status"] = "publicado"; salvar_questao(q); n += 1
    print(f"{n} questão(ões) marcadas como publicadas.")
