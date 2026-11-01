# Modelo de dados

A fonte da verdade são os arquivos em `data/`. O banco do app é uma cópia gerada pela
etapa `publicar`. Assim, trocar o app (por exemplo, ao virar SaaS) não mexe nos dados.

## Questão: `data/questoes/<banca>/<ano><versao>/<id>.json`

Esquema formal: `schemas/questao.schema.json`.

| Campo | Tipo | Exemplo / observação |
|---|---|---|
| `id` | texto | `unicamp-2021a-q35` = banca-ano+versão-qNN |
| `banca`, `ano`, `versao` | texto, número, texto | `Unicamp`, `2021`, `A` (versão só quando a banca aplicou provas diferentes no mesmo ano) |
| `numero` | texto | número da questão no caderno |
| `fase` | texto | `1ª fase · Prova Q` |
| `fonte.descricao` | texto | caderno de onde o texto foi transcrito (casa com `data/fontes/manifesto.json`) |
| `enunciado` | texto | literal, com `<i> <b> <u> <sub> <sup>` e `[[figura N]]` |
| `figuras` | lista | arquivos em `data/figuras/`, na ordem de `[[figura 1]]`, `[[figura 2]]`... |
| `gabarito` | `A`–`E` | |
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
como lista de `assetId`, sem `status`, `gabaritoFonte`, `revisao`.
