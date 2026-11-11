# Modelo de dados

A fonte da verdade são os arquivos em `data/`. O banco do app é uma cópia gerada pela
etapa `publicar`. Assim, trocar o app (por exemplo, ao virar SaaS) não mexe nos dados.

## Questão: `data/questoes/<banca>/<ano><versao>[-<edicao>]/<id>.json`

Esquema formal: `schemas/questao.schema.json`.

| Campo | Tipo | Exemplo / observação |
|---|---|---|
| `id` | texto | `fuvest-2024-q12` = banca-ano-qNN; com edição: `acafe-2025-verao-q29`, `unicamp-2021-biologicas-e-saude-q49` |
| `banca`, `ano` | texto, número | `Unicamp`, `2021` |
| `versao` | texto | **obsoleto**: não usar (marcava a prova no ano, como "2021 A"); nenhuma questão o usa desde a v2.0.0 |
| `edicao` | texto | opcional: `Verão`, `Inverno` (Acafe, dois vestibulares por ano); `Prova I`, `Prova II` (Einstein, dois cadernos do mesmo vestibular); `Exatas e Humanas`, `Biológicas e Saúde` (Unicamp 2021, provas por área). Entra no id (`einstein-2025-prova-ii-q03`), na pasta e na chave da prova; o app mostra só o ano, e a edição aparece na `fase` |
| `tipo` | texto | opcional: `objetiva` (padrão, quando ausente) ou `discursiva` |
| `numero` | texto | número da questão no caderno |
| `fase` | texto | `1ª fase · Prova Q` |
| `fonte.descricao` | texto | caderno de onde o texto foi transcrito (casa com `data/fontes/manifesto.json`) |
| `enunciado` | texto | literal, com `<i> <b> <u> <sub> <sup>` e `[[figura N]]` |
| `figuras` | lista | arquivos em `data/figuras/`, na ordem de `[[figura 1]]`, `[[figura 2]]`... |
| `gabarito` | `A`–`E` | vazio nas discursivas |
| `respostas` | lista | só nas discursivas: `[{"item": "a", "texto": "..."}]`, resposta final de cada item, na ordem do enunciado (`item` vazio se a questão não tem itens); mesma marcação do enunciado |
| `gabaritoFonte` | texto | `oficial`, `prova-comentada-oficial`, `resolucao-propria` |
| `resolucao` | texto | passo a passo, mesma marcação do enunciado |
| `topicos` | lista | ids de `data/taxonomia.json` |
| `status` | texto | `rascunho` → `revisado` → `publicado` |
| `revisao` | objeto | opcional: `divergenciasAceitas` (lista), `notas` (texto) |
| `criadoEm`, `atualizadoEm` | ISO 8601 | |
| `_notas` | objeto | só em rascunho, apagado na revisão |

## Outros arquivos

- `data/taxonomia.json`: 15 áreas, 151 tópicos (`id` = slug do nome).
- `data/fontes/manifesto.json`: cada PDF oficial usado, com banca, ano, versão, tipo,
  descrição, URL, nº de páginas e sha256. Os PDFs ficam em `fontes/`, fora do git.
- `data/figuras-publicadas.json`: arquivo de figura → `assetId` no app + sha256 (para
  saber o que precisa ser reenviado).

## Documento no app atual (coleção `questoes`)

Gerado por `publicar`: mesmos campos, exceto `fonte.descricao` → `origem`, `figuras`
como lista de `assetId`, sem `status`, `gabaritoFonte`, `revisao`. As discursivas levam
também `tipo` e `respostas`; o app mostra o selo "Discursiva", as respostas por item na
resolução e no gabarito da lista .docx, e um filtro "Tipo de questão".
