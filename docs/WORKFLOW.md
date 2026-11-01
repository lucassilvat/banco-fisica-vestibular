# Fluxo de trabalho: importar uma prova

Uma prova entra no banco em 9 etapas. As etapas automáticas são comandos do pipeline;
as de julgamento (o que é Física, transcrição final, resolução, revisão) são feitas
por uma pessoa ou pelo Claude, e sempre conferidas pela etapa 8 antes de publicar.

```
 1 registrar-prova   PDF oficial -> fontes/ + manifesto (com sha256)
 2 segmentar         caderno -> uma região por questão
 3 triagem           pontua vocabulário de Física -> lista de candidatas
 4 renderizar        imagem de cada candidata (e grades de página para figuras)
   ── decisão: quais questões entram (docs/CRITERIOS.md)
 5 rascunho          texto pré-extraído -> data/questoes/... (status: rascunho)
 6 figuras           detecta, recorta, folha de contato; ajustes manuais se preciso
 7 transcrição final, gabarito, resolução e tópicos (julgamento)
 8 verificar         estrutura + fidelidade ao PDF -> status: revisado
 9 publicar          lotes para o banco do app -> status: publicado
```

Instalação (uma vez): `pip install -r requirements.txt` e `poppler-utils` (pdftotext).
Todos os comandos rodam na raiz do projeto: `python -m pipeline <comando> -h`.

---

## 1. Registrar a prova

Baixe do site da banca o **caderno de questões aplicado** (não a prova comentada nem
resoluções de cursinho) e, se houver, o **gabarito oficial**. Copie para `fontes/` com o
nome `<banca>-<ano><versao>-<tipo>.pdf` e registre:

```
python -m pipeline registrar-prova Unicamp 2015 --descricao "Vestibular Unicamp 2015, 1ª fase, caderno de questões" --fase "1ª fase · Prova Q" --url https://...
python -m pipeline registrar-prova Unicamp 2015 --tipo gabarito --descricao "Gabarito oficial 1ª fase 2015"
```

A chave da prova passa a ser `unicamp-2015` (com versão: `unicamp-2021A`). Os PDFs ficam
fora do git; o manifesto guarda o sha256 para saber exatamente de qual arquivo cada
questão foi transcrita.

## 2. Segmentar

```
python -m pipeline segmentar unicamp-2015
```

Confira `trabalho/unicamp-2015/segmentos.txt`: deve haver uma linha por questão, na
ordem, e o aviso de números ausentes não deve aparecer. Na primeira prova de uma banca
nova, abra algumas imagens (etapa 4) para confirmar que as regiões estão certas. O
segmentador assume títulos "QUESTÃO N" (Unicamp) ou só o número em corpo grande ("01",
"{ 01}": Fuvest, chaves `fuvest-*`) e duas colunas; outras diagramações pedem ajuste em
`pipeline/segmentar.py`. Na Fuvest, os textos comuns ("TEXTO PARA AS QUESTÕES...") ficam
no fim do segmento da questão anterior: confira-os na imagem.

### 2b. OCR (só quando a camada de texto do PDF é ilegível)

Se o `segmentos.txt` sair com símbolos sem sentido (ex.: Fuvest 2021, "Caderno Reserva"),
rode `python -m pipeline ocr <prova>`. Ele grava `fontes/<arquivo>.ocr.txt` e marca a prova
no manifesto (`camadaTexto: "ocr"`); a triagem precisa ser feita olhando as imagens, e o
`verificar` passa a conferir a fidelidade contra o texto do OCR.

## 3. Triagem

```
python -m pipeline triagem unicamp-2015
```

Gera `triagem.csv` ordenado por pontuação. Trate a lista como ponto de partida:
- olhe também as vizinhas de cada bloco de candidatas (blocos de Física são contíguos);
- questões interdisciplinares costumam pontuar pouco (2019 Q15, Q81 só citam Física de
  passagem no texto, mas a resolução depende dela).

## 4. Renderizar

```
python -m pipeline renderizar unicamp-2015 55-66
python -m pipeline renderizar unicamp-2015 21,22 --grade    # páginas, com grade
```

Com as imagens, decida a lista final seguindo `docs/CRITERIOS.md`.

## 5. Rascunho

```
python -m pipeline rascunho unicamp-2015 57-64
```

Cria um JSON por questão com `status: "rascunho"`. O texto vem da camada de texto do PDF
e já traz itálicos, sublinhados, sub/sobrescritos. Fórmulas de editor de equações e
frações saem embaralhadas: a transcrição é corrigida na etapa 7, olhando a imagem.

## 6. Figuras

```
python -m pipeline figuras detectar unicamp-2015 58,61,63
```

Abra `trabalho/unicamp-2015/figuras/folha-contato.png`. Se alguma caixa pegou texto
demais ou cortou a figura, escreva a caixa certa em `figuras/ajustes.json`
(`{"58": [[pagina, x0, y0, x1, y1]]}`, coordenadas lidas na imagem de grade) e rode de
novo. Quando estiverem certas:

```
python -m pipeline figuras aplicar unicamp-2015 58,61,63
```

Regras: a figura entra recortada do próprio caderno, sem retoques, exceto remover
destaques que não existiam na prova aplicada (ex.: marca-texto do gabarito em provas
comentadas). Alternativas que são figuras viram uma figura por alternativa.

## 7. Transcrição final, gabarito, resolução e tópicos

Para cada rascunho, comparando com a imagem da questão:

1. **Enunciado** literal (regras em `docs/CRITERIOS.md`), com `[[figura N]]` no ponto em
   que cada figura aparece e as alternativas no fim, uma por linha (`a) ...`).
2. **Textos comuns e instruções gerais** ("Texto comum às questões...", "use g = 10 m/s²")
   repetidos no início de cada questão a que se aplicam.
3. **Gabarito**: do gabarito oficial quando houver (`gabaritoFonte: "oficial"`); senão,
   da resolução (`"resolucao-propria"`), para ser conferido depois.
4. **Resolução** comentada, passo a passo, numerada; em questões interdisciplinares,
   explicar também a parte não física que elimina alternativas.
5. **Tópicos** da `data/taxonomia.json` (2 a 4, do mais central ao acessório).
6. Apagar o campo `_notas` e mudar `status` para `"revisado"`.

## 8. Verificar

```
python -m pipeline verificar unicamp-2015
python -m pipeline verificar --estrito      # o banco inteiro, avisos contam como erro
```

Erros bloqueiam a publicação. Avisos de fidelidade ("palavra não encontrada no PDF")
precisam ser olhados um a um: quando são legítimos (palavra hifenizada na quebra de
linha, subscrito colado, URL quebrada), registre em `revisao.divergenciasAceitas`
com o motivo em `revisao.notas`.

## 9. Publicar

```
python -m pipeline publicar preparar unicamp-2015
```

Se houver figuras novas, ele lista os arquivos: envie cada um ao armazenamento do app
e registre o id devolvido (`publicar registrar data/figuras/x.png <assetId>`). Rode
`preparar` de novo para gerar os lotes (`trabalho/publicacao/lote-NN.json`, até 50
documentos cada), grave-os no banco do app e finalize com:

```
python -m pipeline publicar marcar unicamp-2015
git add -A && git commit -m "Unicamp 2015: 8 questões de Física"
```

---

## Como pedir ao Claude

O arquivo `CLAUDE.md` na raiz descreve estas regras para o Claude. Um pedido típico:

> Importe a 1ª fase da Unicamp 2015 (PDF em fontes/unicamp-2015-caderno.pdf, gabarito
> em fontes/unicamp-2015-gabarito.pdf). Siga o docs/WORKFLOW.md até a etapa 8 e me
> mostre a lista de questões escolhidas antes de transcrever.

## Ritmo e priorização

- `python -m pipeline painel` mostra quantas questões há por prova e quais áreas e
  tópicos ainda estão vazios. Hoje, Eletromagnetismo, Física moderna e Ondulatória
  são as áreas mais pobres. Use isso para escolher as próximas provas.
- Um lote razoável é **uma prova por vez**, com revisão sua antes do commit. Provas
  da mesma banca reaproveitam ajustes de segmentação e de figuras.
- Antes de começar uma banca nova (Fuvest, Unesp, ENEM), importe uma prova só e
  ajuste o segmentador; depois o ritmo volta ao normal.
