# Resoluções animadas

Adicional à resolução comentada (que continua igual): um passo a passo animado, feito para
o aluno, com os conceitos físicos explícitos. No app, aparece o botão **Resolução animada**
ao lado de **Ver resolução** nas questões que têm roteiro.

Piloto (v2.8.0): Unesp 2025 Q78 (plano inclinado), ENEM 2023 Q98 (circuito) e Unicamp 2017
Q58 (gráfico v × t).

## Como funciona

Um **roteiro** por questão em `data/animacoes/<id>.json` (esquema em
`schemas/animacao.schema.json`). O roteiro não desenha nada: escolhe um **modelo de cena**
e diz, passo a passo, o que mostrar. O mesmo roteiro serve para:

1. **Player do app** (`app/index.html`, `CENAS` e `openPlayer`): cena em SVG à esquerda,
   passo à direita, com avançar/voltar, equações que aparecem uma a uma, pergunta
   "Pense antes de avançar" e, em alguns modelos, controles interativos.
2. **Vídeo em Manim** (`videos/manim_roteiro.py`), opcional:
   `ROTEIRO=<id> manim -qh videos/manim_roteiro.py Roteiro`. Requer `pip install manim`,
   LaTeX com `babel` (português), `dvisvgm` e `ffmpeg`. Os vídeos não vão para o git.

Cada passo tem:

| Campo | Para quê |
|---|---|
| `conceito` | o conceito físico do passo (aparece acima do título e acende o chip correspondente em `conceitos`) |
| `titulo`, `texto` | mesma marcação da resolução (`<i>`, `<b>`, `<sub>`, LaTeX entre `\(` e `\)`) |
| `equacoes` | LaTeX sem delimitadores, mostradas uma de cada vez |
| `pergunta` | `{texto, resposta}`: o aluno pensa e só depois abre a resposta |
| `cena.mostrar` / `cena.ocultar` | elementos do modelo que entram/saem (acumulam de um passo para o outro) |
| `cena.destacar` | elementos que piscam só neste passo |
| `cena.estado` | animações do modelo (valem deste passo em diante) |

## Modelos de cena

| Modelo | Parâmetros | Elementos | Estado |
|---|---|---|---|
| `plano-inclinado` | `senTheta`, `cosTheta`, `mu`, `g` | `rampa`, `angulo`, `caixa`, `peso`, `normal`, `atrito`, `eixos`, `componentes`, `angulo-peso`, `aceleracao`, `balanco` | `movimento`: `repouso`/`acelerando`; `controle`: `aceleracao` (controle deslizante da aceleração da esteira) |
| `circuito-conjuntos-serie` | `conjuntos` (até 3 nomes), `rSobreR` (r/R do exemplo numérico) | `circuito`, `conjuntos`, `corrente`, `equivalentes`, `brilho` | `queimada`: nome da lâmpada queimada |
| `grafico-vt` | `pontos` [[t, v]...], `tMax`, `vMax`, `passoT`, `passoV`, `trechos` (2 intervalos de área), `paradas` | `eixos`, `curva`, `estrada`, `paradas`, `faixa`, `area-1`, `area-2`, `cotas-1`, `cotas-2` | `percorrer`: carro e área acumulando com o tempo |

Os nomes aceitos ficam em `MODELOS` (`pipeline/animacoes.py`) e precisam bater com `CENAS`
no app e com `MODELOS` no Manim (por enquanto, só `plano-inclinado` tem versão em vídeo).

Para escalar, a ideia é ter poucos modelos reaproveitáveis (lançamentos, blocos e polias,
lentes e espelhos, ondas, gráficos p × V...) e escrever só o roteiro de cada questão.
Os modelos foram feitos para as questões do piloto; generalizá-los (mais conjuntos no
circuito, ângulos diferentes etc.) é o próximo passo.

## Regras

- O roteiro **não altera** enunciado, gabarito nem resolução da questão. A física tem de
  bater com a resolução comentada; o último passo cita a alternativa correta, como "(A)".
- Exemplo numérico que a questão não dá (ex.: `r = R` no circuito do ENEM) é dito como
  exemplo no texto, e a conclusão geral vem junto.
- `python -m pipeline animacoes verificar` confere: questão existe, modelo e elementos
  válidos, LaTeX no subconjunto do app, marcação aceita, último passo com o gabarito.

## Publicar

```
python -m pipeline animacoes verificar
python -m pipeline animacoes preparar        # trabalho/publicacao/animacoes-lote-NN.json
```

Grave os lotes na coleção `animacoes` do banco do app (documento = id da questão). O site
estático (`python -m pipeline site`) leva os roteiros em `animacoes.json`.
