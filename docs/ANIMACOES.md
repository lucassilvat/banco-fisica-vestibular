# Resoluções animadas

> **Em revisão (v2.14.0).** No app do Claude (só o Lucas acessa), cada animação tem a seleção
> Não revisada / Comentada / Aprovada e um comentário, gravados na coleção `revisoes`. O site
> público (GitHub Pages) só recebe as **aprovadas**: `python -m pipeline site` filtra pelo campo
> `revisao.estado` do roteiro; `python -m pipeline site <pasta> --revisao` gera a versão com todas,
> que é a publicada no app do Claude. Antes de cada pull request, exportar a coleção `revisoes`
> e gravar com `python -m pipeline animacoes revisoes <arquivo.json>`. Não produzir animações novas
> sem novo pedido.

Adicional à resolução comentada (que continua igual): um passo a passo animado, feito para
o aluno, com os conceitos físicos explícitos. No app, aparece o botão **Resolução animada**
ao lado de **Ver resolução** nas questões que têm roteiro.

Piloto (v2.8.0): Unesp 2025 Q78 (plano inclinado), ENEM 2023 Q98 (circuito) e Unicamp 2017
Q58 (gráfico v × t). Desde a v2.9.0 o trabalho segue por vestibular, ano a ano, começando pela
Unesp: 2026 completa (Q76–Q82) e 2025 completa (Q48, Q76–Q82, Q84, Q90).


## Formato "aula" (v2.15.0) — o estilo pedido pelo Lucas

As diretrizes de conteúdo e de desenho que vieram das revisões do Lucas estão na seção
"Diretrizes das revisões do Lucas", abaixo; ler antes de cada lote.

A resolução é dada como um professor faria na lousa:

- **Abertura** (opcional): quando há mais de um caminho, uma tela que os apresenta ("Há dois
  métodos..."). Os métodos ficam em **abas**; o aluno escolhe qual vê.
- **Telas** de cada método, com **blocos** que aparecem um a um, com pausa proporcional ao
  tamanho: `{"t": "texto", "html": "..."}` (negrito com `<b>` onde importa; LaTeX entre `\(` e
  `\)`), `{"t": "eq", "tex": "..."}` (uma equação por bloco), `{"t": "gabarito", "letra": "A"}` e
  `{"t": "fim"}`.
- **Álgebra animada**: marque trechos com `\marca{id}{...}`. No bloco seguinte,
  `"cancelar": ["id", ...]` risca esses trechos da equação anterior antes de mostrar a nova;
  `"mover": ["id"]` leva o trecho (com a mesma marca nas duas equações) da posição antiga para a
  nova, como em "passar para o outro lado".
- **Preferir cancelamentos a contas intermediárias** (ex.: escrever 70 = 7 · 10 e cancelar o 7).
- **Cena** (modelo `diagrama`) só quando agrega: simulação se ajuda a entender o fenômeno,
  desenho estático se basta, nenhuma se o texto resolve. Cada tela diz o que mostrar
  (`cena.mostrar`) e quais animações rodam (`cena.animar`); `cena.destacar` faz piscar um
  elemento mostrado.
  Também vale um **modelo pronto** do app (ex.: `indicador-combustivel`, Unesp 2026 Q82); aí a
  tela usa `cena.estado` com os estados do modelo (em `MODELOS`, `pipeline/animacoes.py`).
- **Imagens em espelhos e lentes**: desenhar imagem virtual do lado virtual (atrás do espelho),
  com o tamanho dado pelo aumento (revisão do Lucas na Unesp 2026 Q79).
- Cada método termina com o gabarito e "Fim da resolução.".
- **Cancelamento**: o traço é um fundo diagonal no próprio termo marcado (canto inferior esquerdo ao
  superior direito, como o `\cancel`), sem medir a tela: assim acompanha o termo em qualquer escala
  (o painel do artefato reduz a página, e um traço posicionado por medida saía deslocado).
- **Movimento com aceleração uniforme**: no `trajeto`, `velocidades: [v0, v]` faz o corpo ir de v0
  a v uniformemente (`acelerado: true` é o caso que parte do repouso). Para sequências no mesmo
  ciclo (cai, depois desce junto com o prato), `fases: [{pontos, duracao, ...}, ...]`; o tipo
  `esticar` (mola) usa `fases` com `de`/`ate` (fator vertical) e `centro`.
- **Resolução aprovada não se altera direto**: sugerir ao Lucas e esperar o aval; depois da mudança,
  ela volta à revisão.
- Exemplo completo: `data/animacoes/unesp-2026-q81.json` (dois métodos, cancelamento e mover).

## Diretrizes das revisões do Lucas

O que o Lucas pediu nos comentários de revisão (Unesp 2019 a 2026, nov/2026), com a questão de
origem. Vale para toda resolução animada nova ou refeita: ler antes de produzir um lote e conferir
cada item antes de publicar no app para revisão.

### 1. Como o aluno resolveria

- **Resolver do jeito que o aluno vai fazer na prova**, seguindo o caminho que a questão sugere.
  Ex.: meia-vida térmica (Unesp 2019 Q80): meia-vida por meia-vida, com a temperatura inicial e a
  final de cada uma, e depois Q = m c ΔT.
- **Não assumir o que o problema não garante.** Um gráfico ou desenho que sugere uma informação
  não dada (ex.: meias-vidas de mesma duração) induz o aluno ao erro; nesse caso, sem gráfico.
- **Enunciar a fórmula antes de usá-la**: primeiro E<sub>p</sub> = m g h, depois os valores
  (2019 Q85); primeiro T<sub>y</sub> = T sen θ, mostrando o ângulo e o seno (ou cosseno) no
  triângulo retângulo, depois a conta (2022 Q77). Na segunda vez, o mesmo raciocínio mais rápido.
- **Ordem lógica das grandezas**: calcular primeiro o que se conserva e usá-lo depois. Ex.: na
  refração de ondas, a frequência primeiro; mantendo a frequência, o novo comprimento de onda
  (2022 Q81).
- **Áreas sob gráficos por partes simples**: figuras abaixo da curva (dois triângulos, não um
  triângulo "acima" que se subtrai) e cada parte com a sua conta antes da soma (2020 Q76).
- **Contas longas em etapas que o aluno reconhece**: em misturas, tomar 1 000 g, isolar o volume
  na fórmula da densidade antes de calcular, somar os volumes ("a cada 1 kg temos esse volume") e
  fechar com regra de três (2020 Q87).
- **Versão aproximada quando os valores são "feios"**: depois da resolução completa, refazer com
  valores arredondados (ex.: densidades 20 e 6; 528/170 ≈ 3), dizendo que na hora da prova
  aproximar é boa estratégia, e mostrar que o gabarito é o mesmo (2020 Q87, 2019 Q73).

### 2. Álgebra na lousa

- **Sinais corretos, sem módulo**: o aluno precisa se apropriar das fórmulas com o sinal. Ex.:
  imagem real, portanto invertida: p' > 0 e A < 0; A = −p'/p, os sinais de menos se cancelam
  (2020 Q80). Calor cedido: Q negativo, e o texto explica o sinal.
- **Demonstrar visualmente as passagens**: cancelamentos animados e termos que "passam para o
  outro lado" (ex.: de A = −p'/p até p = 5 000 p'). Na passagem de logaritmos, a **regra do
  tombamento** animada (2021 Q81): muitos alunos têm dificuldade com ela. "Tombar" vale só para o
  logaritmo de uma potência; na definição de logaritmo, dizer apenas que o número é o expoente da
  base (log I/I<sub>0</sub> = 6 ⇒ I/I<sub>0</sub> = 10<sup>6</sup>: o 6 é o expoente de 10; 2018 Q81).
- **Desenvolvimento vertical**: uma passagem por linha, uma embaixo da outra; nada de encadear
  várias passagens na mesma linha com "⇒" (2016 Q79).
- **Sem produto vetorial**: alunos de ensino médio não o conhecem. Força magnética pela **regra da mão
  direita**, mostrada com o desenho de uma mão (polegar na corrente, dedos no campo, a força sai da
  palma); em questões de alternativas, testar cada uma por eliminação, na ordem em que o aluno faria:
  polaridade da pilha, polo do ímã, mão, força e efeito (2017 Q83).
- **Cancelamento só onde é algébrico** (fator comum, termo que aparece dos dois lados). Igualar
  membros de uma cadeia de igualdades não é cancelar.
- **O traço do cancelamento fica sobre o termo**, em qualquer tamanho de tela (2025 Q79 e Q81).
- **Entidades HTML** (`&lt;`) nunca: usar os caracteres `<`, `>` e `&` (2021 Q78, enunciado).

### 3. Fidelidade do desenho

- **O desenho segue a figura da prova** e a física: nada fundido ou omitido que mude o sentido
  (o baço estava junto com os intestinos; na prova, baço e intestinos estão em paralelo e em série
  com o fígado: 2019 Q66).
- **Conferir o gabarito e as grandezas contra a figura** antes de animar: na 2019 Q81, α é o
  ângulo de incidência na interface A/B (na camada A), e o gabarito gravado estava errado.
- **Escala real quando o desenho é cinemático**: o ponto mais alto da parábola tem de estar no
  vértice, e o vetor velocidade no ponto que ele descreve, mesmo que a figura da prova não esteja
  em escala (2022 Q78). Órbitas desenhadas contêm os planetas (2020 Q77).
- **Óptica**: imagem virtual do lado virtual do espelho, com o tamanho dado pelo aumento
  (2026 Q79). Raios pelo centro óptico; objeto e imagem com setas opostas quando a imagem é
  invertida (2020 Q80). Marcar o **olho** do observador quando importa a orientação, e **todas
  as distâncias** envolvidas na formação das imagens (2021 Q80). Refração no prisma calculada pela
  lei de Snell nas duas faces: o feixe entra pela face, separa-se dentro do vidro e cada cor sai
  desviada para a base, o violeta mais; se o desvio entre as cores for exagerado para ser visto,
  dizer isso no desenho (2018 Q80).
- **Circuitos fechados e legíveis**: cada componente ligado ao fio pelos dois terminais (resistor
  entre os pontos indicados, lâmpada no caminho da corrente), nós marcados onde os fios se dividem
  e aparelhos de medida identificados (2018 Q82).
- **Grandeza usada na conta aparece no desenho**: se a resolução usa h ou λ, marcar h ou λ na
  figura (cota) e mostrar a relação que se lê dela, como os 3 m = λ + λ/2 = 1,5λ (2016 Q82, 2017 Q80).
- **Forças com ponto de aplicação**: as forças sobre um corpo (ou sobre um conjunto tratado como um
  só corpo) saem de um ponto marcado nele, não soltas no desenho (2016 Q78).
- **Ângulos bem marcados**: setor entre as duas retas certas, rótulo legível (2023 Q80).
- **Correntes e campos com sentido certo em todo o ciclo**, inclusive quando a animação recomeça
  (2026 Q82).
- **Representar o fenômeno com o modelo que o professor usaria**: a Terra com um ímã de barra
  dentro (S magnético perto do N geográfico), linhas de campo grandes, saindo do N e entrando no S,
  com setas de orientação. Nada de vetores pequenos ou confusos (2019 Q82).

### 4. Movimento nas simulações

- **Colisões**: os corpos se movem juntos depois do contato (quando é o caso), com a velocidade
  indicada perto do corpo. Mostrar duas "fotografias": imediatamente antes e imediatamente depois
  da colisão. A animação serve para o aluno entender o que aconteceu (2023 Q78).
- **Aceleração uniforme de verdade**: o corpo ganha velocidade uniformemente enquanto anda
  (2023 Q87).
- Simulação só quando agrega; contas simples ficam só na lousa.

### 5. Legibilidade

- **Linhas importantes em preto (#111111) e grossas**, com bom contraste também no tema escuro
  (2021 Q76: segmentos do triângulo).
- **Cor citada no texto = cor do desenho**: se o texto fala da seta vermelha, a seta é vermelha
  (2021 Q80).
- Desenho grande o suficiente para ver os detalhes no painel do app; rótulos sem sobreposição.

### 6. Processo

- Uma resolução já **Aprovada** não se altera direto: sugerir a mudança ao Lucas e esperar o aval;
  depois ela volta à revisão (vale também para mudanças no player que alterem o que ela mostra).
- Ao corrigir um comentário, conferir a captura de **todas** as telas da questão.

## Como funciona

Um **roteiro** por questão em `data/animacoes/<id>.json` (esquema em
`schemas/animacao.schema.json`). O roteiro não desenha nada: escolhe um **modelo de cena**
e diz, passo a passo, o que mostrar. O **player do app** (`app/index.html`, `CENAS` e
`openPlayer`) desenha a cena em SVG à esquerda e o passo à direita, com avançar/voltar e
equações que aparecem uma a uma.

Decisão do Lucas (v2.8.2): só o player do app, sem vídeo (o Manim foi testado e descartado).

Cada passo tem:

| Campo | Para quê |
|---|---|
| `conceito` | o conceito físico do passo (aparece acima do título e acende o chip correspondente em `conceitos`) |
| `titulo`, `texto` | mesma marcação da resolução (`<i>`, `<b>`, `<sub>`, LaTeX entre `\(` e `\)`) |
| `equacoes` | LaTeX sem delimitadores, mostradas uma de cada vez |
| `cena.mostrar` / `cena.ocultar` | elementos do modelo que entram/saem (acumulam de um passo para o outro) |
| `cena.destacar` | elementos que piscam só neste passo |
| `cena.estado` | animações do modelo (valem deste passo em diante) |

## Modelos de cena

| Modelo | Parâmetros | Elementos | Estado |
|---|---|---|---|
| `plano-inclinado` | `senTheta`, `cosTheta`, `mu`, `g` | `rampa`, `angulo`, `caixa`, `peso`, `normal`, `atrito`, `eixos`, `componentes`, `angulo-peso`, `aceleracao`, `balanco` | `movimento`: `repouso`/`acelerando` |
| `circuito-conjuntos-serie` | `conjuntos` (até 3 nomes), `rSobreR` (r/R do exemplo numérico) | `circuito`, `conjuntos`, `corrente`, `equivalentes`, `brilho` | `queimada`: nome da lâmpada queimada |
| `grafico-vt` | `pontos` [[t, v]...], `tMax`, `vMax`, `passoT`, `passoV`, `trechos` (2 intervalos de área), `paradas` | `eixos`, `curva`, `estrada`, `paradas`, `faixa`, `area-1`, `area-2`, `cotas-1`, `cotas-2` | `percorrer`: carro e área acumulando com o tempo |
| `mhs-sombra` | `amplitude` (m), `periodo` (s), `t1`, `t2` | `pendulo`, `sombra`, `vetor-v`, `grafico`, `ponto-1`, `ponto-2`, `secante` | `t`: instante parado (sem `t`, oscila); `cursor`: linha do tempo no gráfico |
| `rotacao-latitude` | `latitude` (graus) | `terra`, `eixo`, `equador`, `paralelo`, `latitude`, `morador`, `gravidade`, `centripeta`, `angulo`, `alternos` | `girar` |
| `cadeia-energia` | `etapas` [{`rotulo`, `valor`, `operacao`}] (até 8; `^{}` e `_{}` nos textos), `altura` | `etapa-1`…`etapa-8`, `subida` | `subir` |
| `espelho-convexo` | `f` (negativo), `d0`, `d1`, `t1` | `eixo`, `muro`, `espelho`, `foco`, `imagem`, `cotas` | `d` (distância fixa) ou `mover` (de `d0` a `d1` em `t1`) |
| `espectro-fototropismo` | `azul` [λ mín, λ máx] em nm | `espectro`, `azul`, `setas`, `luz`, `planta`, `lados`, `auxina` | `curvar` |
| `campo-uniforme` | `U` (V), `dTexto` | `placas`, `tensao`, `cota-d`, `campo`, `ion`, `forca` | `mover` |
| `indicador-combustivel` | — | `tanque`, `reostato`, `circuito`, `corrente`, `lamina`, `mostrador`, `zoom` | `nivel`: 0 a 1 ou `esvaziar` |
| `rotas-velocidade-media` | `rotas` [{`nome`, `trechos` [{`modal`, `ds`, `v`}]}] | `rotas`, `tempos`, `totais`, `veiculos` | `percorrer` |
| `engrenagens-internas` | `razao` (R<sub>A</sub>/R<sub>B</sub>) | `roda`, `engrenagem-a`, `engrenagem-b`, `manivela`, `contato`, `raios` | `girar` |
| `lancamento-obliquo` | `coef` [a, b, c] de y(x), `xC`, `tB`, `tC`, `vx`, `vy` | `terreno`, `eixos`, `trajetoria`, `pontos`, `vertice`, `componentes`, `velocidade-b`, `bola` | `lancar`; `t` (instante parado) |
| `manometro-gas` | — | `recipiente`, `gas`, `mercurio`, `patm`, `desnivel`, `pressoes` | — |
| `aumento-linear` | `i1`, `A1`, `A2` | `imagem-1`, `objeto`, `imagem-2` | — |
| `onda-corda` | `lambda`, `f`, `dist` | `pino`, `corda`, `frente`, `cotas` | `propagar` |
| `soma-potencias` | `U`, `imax`, `limite`, `base`, `alternativas` | `limite`, `base`, `alt-a`…`alt-e` | — |
| `grafico-modulo` | `zero`, `coef`, `xs`, `ys`, `marcasX`, rótulos | `eixos`, `reta`, `modulo`, `ponto-zero`, `ponto-0` | `dobrar` |
| `triangulo-pg` | — | `triangulo`, `particula`, `tempos`, `soma` | `percorrer` |

| `diagrama` | `largura`, `altura`, `elementos` {nome: [formas]}, `animacoes` {nome: {`alvo`, `tipo`, ...}} | os nomes definidos em `elementos` | `animar`: lista de animações |

**`diagrama`** é o modelo genérico, usado a partir da Unesp 2024: a cena inteira vai no
roteiro. Formas: `ret`, `circ`, `linha`, `caminho`, `seta` (com `rotulo`, `sub`, `vetor`,
`rot_em`, `ancora`, `tracejado`), `vetor`, `texto`, `rotulo` (texto em caixa), `angulo`
(setor + rótulo em caixa) e `cota`. Cores por nome (`peso`, `normal`, `atrito`, `acel`,
`tinta`, `mudo`, `suave`, `papel`, `perigo`, `luz`, `linha`) ou CSS. Animações: `trajeto`
(`pontos`, `duracao`, `pausa`), `girar`, `oscilar`, `aparecer` e `escalar` (`centro`,
`fator`). Para cálculos encadeados, um diagrama de caixas ligadas por setas (`etapa-1`…)
substitui o `cadeia-energia`. `python -m pipeline animacoes verificar` confere os campos
obrigatórios de cada forma e os alvos das animações.

Os nomes aceitos ficam em `MODELOS` (`pipeline/animacoes.py`) e precisam bater com `CENAS`
no app.

Para escalar, a ideia é ter poucos modelos reaproveitáveis (lançamentos, blocos e polias,
lentes e espelhos, ondas, gráficos p × V...) e escrever só o roteiro de cada questão.
Os modelos foram feitos para as questões do piloto; generalizá-los (mais conjuntos no
circuito, ângulos diferentes etc.) é o próximo passo.

## Regras

- **Sem perguntas ao aluno** ("Pense antes de avançar" e semelhantes): o que seria a resposta
  vai no próprio texto do passo.
- **Sem simuladores em que o aluno muda valores** (controles deslizantes, campos para
  digitar). As animações rodam sozinhas; o aluno só avança e volta os passos.
- **Forças: letra maiúscula e notação de vetor** (seta em cima) na cena e no texto: \(\vec{P}\),
  \(\vec{N}\), \(\vec{F}_{\text{at}}\), \(\vec{F}_{g}\)... Atrito é \(\vec{F}_{\text{at}}\), não *f*. Exceção só
  se a questão usar outra notação. Nas equações de intensidade (módulos) a letra fica sem seta.
  Na cena, rótulo de grandeza vetorial usa `sVec`.
- **Só o essencial.** Cada informação do roteiro precisa ser usada na resolução. Mostrar o que
  acontece é bem-vindo, mas sem números ou grandezas que a resolução não usa (ex.: na Unesp
  2026 Q76, nada de pulsação nem período; no ENEM 2023 Q98, nada de porcentagem de um exemplo
  numérico).
- **Revisão visual de cada passo** antes de publicar: abrir o player, olhar todos os passos e
  conferir (1) legibilidade — nada de texto ou ângulo sobre fundo que atrapalhe; rótulos de
  ângulo em caixa (`sPill`) e setores preenchidos (`sWedge`); nada sobreposto; (2) fidelidade —
  o desenho corresponde à física e à figura da prova (ex.: o circuito é um caminho fechado, sem
  fio solto nem corrente indo para onde não há fio; sentidos de forças, campos e correntes).
- O roteiro **não altera** enunciado, gabarito nem resolução da questão. A física tem de
  bater com a resolução comentada; o último passo cita a alternativa correta, como "(A)".
- Exemplo numérico que a questão não dá (ex.: `r = R` no circuito do ENEM) é dito como
  exemplo no texto, e a conclusão geral vem junto.
- `python -m pipeline animacoes verificar` confere: questão existe, modelo e elementos
  válidos, só os campos aceitos em cada passo, LaTeX no subconjunto do app, marcação
  aceita, último passo com o gabarito.

## Publicar

```
python -m pipeline animacoes verificar
python -m pipeline animacoes preparar        # trabalho/publicacao/animacoes-lote-NN.json
```

Desde a v2.11.0 os roteiros vão num arquivo do próprio artefato: `python -m pipeline site
<pasta> --revisao` gera `animacoes.json` (todas as animações, para o app de revisão), publicado
junto com `index.html`. O app junta esse arquivo à
coleção `animacoes` do banco (o arquivo prevalece), então os lotes de `preparar` só são
necessários para corrigir um roteiro sem republicar o app.
