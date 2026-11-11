"""Etapa 8: verificações automáticas (rodar antes de marcar 'revisado' e antes de publicar).

Estrutura (sempre): campos obrigatórios, status válido, gabarito, tópicos existentes na
taxonomia, número de [[figura N]] == número de arquivos e arquivos presentes.
Fidelidade (quando o PDF da prova está em fontes/; se a prova estiver marcada com
camadaTexto = "ocr" no manifesto, compara com fontes/<arquivo>.ocr.txt): toda palavra (3+ letras) e todo
número do enunciado precisam existir no texto do PDF. Divergências comuns e legítimas:
quebras de linha com hífen, subscritos colados ("max", "eia"), URLs quebradas. Cada uma
precisa ser olhada; quando legítima, registre-a na própria questão em
revisao.divergenciasAceitas (com o motivo em revisao.notas) para não reaparecer.
"""
import re
import subprocess
from functools import lru_cache

from .comum import FIG_RE, FIGURAS, RAIZ, STATUS, TIPOS, carregar_questoes, chave_prova, fonte_da_prova, ids_topicos, tipo_questao

OBRIG = ["id", "banca", "ano", "numero", "fonte", "enunciado", "figuras", "gabarito", "resolucao", "topicos", "status"]


@lru_cache(maxsize=None)
def _texto_pdf(chave: str):
    try:
        pdf = RAIZ / fonte_da_prova(chave)["arquivoLocal"]
    except SystemExit:
        return None
    if not pdf.exists():
        return None
    if fonte_da_prova(chave).get("camadaTexto") == "ocr":
        ocr = pdf.with_suffix(".ocr.txt")   # gerado por: python -m pipeline ocr <prova>
        if not ocr.exists():
            return None
        t = ocr.read_text(encoding="utf-8")
    else:
        t = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    t = re.sub(r"­\s*\n", "", t); t = re.sub(r"-\n", "-", t)
    palavras = set(re.findall(r"[A-Za-zÀ-ÿ']+", t))
    palavras |= {p for w in re.findall(r"[A-Za-zÀ-ÿ']+(?:-[A-Za-zÀ-ÿ']+)+", t) for p in w.split("-")}
    return palavras, re.sub(r"\s+", "", t)


def checar(q: dict, topicos: set) -> tuple[list, list]:
    erros, avisos = [], []
    for c in OBRIG:
        if c not in q: erros.append(f"campo ausente: {c}")
    if q.get("status") not in STATUS: erros.append(f"status inválido: {q.get('status')}")
    final = q.get("status") in ("revisado", "publicado")
    tipo = tipo_questao(q)
    if tipo not in TIPOS: erros.append(f"tipo inválido: {q.get('tipo')}")
    if tipo == "discursiva":
        resp = q.get("respostas", [])
        if q.get("gabarito"): erros.append("discursiva não tem gabarito A–E (use respostas)")
        itens = [r.get("item", "") for r in resp]
        if len(set(itens)) != len(itens): erros.append("respostas com item repetido")
        if any(not str(r.get("texto", "")).strip() for r in resp): erros.append("resposta vazia")
        for it in itens:
            if it and not re.search(rf"(?m)^{it}\)", q.get("enunciado", "")): erros.append(f"item {it}) das respostas não aparece no enunciado")
        if any(re.search(r"</?(?!(?:i|b|u|sub|sup)>)[a-z]+[^>]*>", r.get("texto", "")) for r in resp):
            erros.append("marcação HTML não permitida nas respostas")
    elif "respostas" in q:
        erros.append("questão objetiva não tem respostas (use gabarito)")
    if final:
        if tipo == "objetiva" and q.get("gabarito") not in list("ABCDE"): erros.append("gabarito deve ser A–E")
        if tipo == "discursiva" and not q.get("respostas"): erros.append("discursiva sem respostas")
        if not q.get("resolucao", "").strip(): erros.append("resolução vazia")
        if not q.get("topicos"): erros.append("sem tópicos")
        if "_notas" in q: avisos.append("campo _notas ainda presente (apague ao revisar)")
    for t in q.get("topicos", []):
        if t not in topicos: erros.append(f"tópico inexistente: {t}")
    marcas = sorted({int(m) for m in FIG_RE.findall(q.get("enunciado", ""))})
    if marcas != list(range(1, len(q.get("figuras", [])) + 1)):
        erros.append(f"marcas [[figura N]] {marcas} não batem com {len(q.get('figuras', []))} arquivo(s)")
    for f in q.get("figuras", []):
        if not (FIGURAS / f).exists(): erros.append(f"figura ausente: data/figuras/{f}")
    if re.search(r"</?(?!(?:i|b|u|sub|sup)>)[a-z]+[^>]*>", q.get("enunciado", "")):
        erros.append("marcação HTML não permitida no enunciado (use só i, b, u, sub, sup)")
    # fidelidade ao PDF
    pdf = _texto_pdf(chave_prova(q["banca"], q["ano"], q.get("versao", ""), q.get("edicao", "")))
    if pdf is None:
        avisos.append("PDF da prova ausente em fontes/: fidelidade não conferida")
    else:
        palavras, compacto = pdf
        limpo = re.sub(r"<[^>]+>|\[\[figura \d+\]\]", " ", q.get("enunciado", ""))
        aceitos = set(q.get("revisao", {}).get("divergenciasAceitas", []))
        faltam = sorted({w for w in re.findall(r"[A-Za-zÀ-ÿ']{3,}", limpo) if w not in palavras} - aceitos)
        nums = sorted({n for n in re.findall(r"\d+(?:[.,]\d+)*", limpo) if n not in compacto} - aceitos)
        if faltam: avisos.append(f"palavras não encontradas no PDF: {faltam}")
        if nums: avisos.append(f"números não encontrados no PDF: {nums}")
    return erros, avisos


def executar(filtro: str | None = None, estrito: bool = False):
    topicos = ids_topicos(); n_err = n_av = 0; total = 0
    for f, q in carregar_questoes(filtro):
        total += 1
        erros, avisos = checar(q, topicos)
        if erros or avisos:
            print(f"\n{f.relative_to(RAIZ)}  [{q.get('status')}]")
            for e in erros: print("  ERRO  ", e)
            for a in avisos: print("  aviso ", a)
        n_err += len(erros); n_av += len(avisos)
    print(f"\n{total} questões verificadas: {n_err} erro(s), {n_av} aviso(s).")
    if n_err or (estrito and n_av):
        raise SystemExit(1)
