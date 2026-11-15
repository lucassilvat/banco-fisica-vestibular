# Histórico de versões

Cada versão corresponde a um lote de importação ou a uma mudança no app/pipeline.
Formato: `vMAIOR.MENOR.CORREÇÃO` — MENOR sobe a cada prova importada; MAIOR, em mudanças
de modelo de dados; CORREÇÃO, em correções de questões já publicadas.

## v2.15.0 — 2026-11-15

- **Novo formato de resolução animada, "aula"** (pedido do Lucas): cadência de professor. Cada
  tela mostra seus blocos um a um, com pausa proporcional ao tamanho (texto com negrito, equação,
  gabarito, "Fim da resolução."); equações aparecem uma de cada vez. Uma equação pode derivar da
  anterior **riscando** trechos (cancelamentos) ou **levando** um trecho para a nova posição
  (passar para o outro lado), com `\marca{id}{...}` no LaTeX e `cancelar`/`mover` no bloco.
  Vários métodos aparecem em **abas**; a tela de abertura apresenta os caminhos. Desenho ou
  simulação (modelo `diagrama`) só quando ajuda; sem cena, a lousa ocupa a largura toda.
  "Próxima tela" completa a tela em andamento antes de avançar.
- **Unesp 2026 refeita nesse formato** (Q76 a Q82), com preferência por cancelamentos em vez de
  contas intermediárias; a Q81 tem dois métodos (campo elétrico e trabalho). Simulações: sombra
  do pêndulo (Q76), espelho se aproximando do muro (Q79), íon migrando entre os eletrodos (Q81).
- Revisão do Lucas: na Q79 as imagens do muro passaram para trás do espelho (região virtual),
  reduzidas; na Q82 voltou o desenho animado do indicador (modelo `indicador-combustivel`), em que
  só a porção ativa do reostato entra no circuito; a bateria ganhou os polos + e −, e a corrente
  (sentido convencional) sai do polo positivo. As cargas desaceleram quando a corrente cai, mas
  não recuam mais ao longo do ciclo (o deslocamento passou a ser acumulado quadro a quadro). O formato aula agora aceita, além do
  `diagrama`, os modelos prontos do app, com `estado` por tela.
- `pipeline animacoes verificar` confere o formato aula (tipos de bloco, marcas usadas em
  `cancelar`/`mover`, gabarito ao fim de cada método); `\marca` entrou no subconjunto de LaTeX.

## v2.14.0 — 2026-11-15

- **Revisão das resoluções animadas no app do Claude** (que só o Lucas acessa). Cada questão com
  animação ganhou a seleção **Não revisada** (padrão) / **Comentada** / **Aprovada** e um campo de
  comentário; tudo fica na coleção `revisoes` do banco do app. Uma barra no topo mostra quantas
  estão em cada situação e filtra as questões por ela. Salvar um comentário numa animação ainda
  não revisada a marca como Comentada.
- **Site público (GitHub Pages) só com as aprovadas**: `python -m pipeline site` só põe em
  `animacoes.json` os roteiros com `revisao.estado = "aprovada"`; `--revisao` inclui todos (é o
  que vai para o app do Claude). Os roteiros não aprovados continuam no repositório.
- `python -m pipeline animacoes revisoes <arquivo.json>` grava nos roteiros as revisões exportadas
  do app; `python -m pipeline animacoes resumo` conta as revisões. Campo `revisao` no esquema.
- Substitui a ocultação da v2.13.1 (constante `MOSTRAR_ANIMACOES`, removida).

## v2.13.1 — 2026-11-15

- **Resoluções animadas ocultas no app** (decisão do Lucas, que quer seguir outro caminho no
  futuro). O botão "Resolução animada" não aparece mais; o app mostra só a resolução textual.
  Nada foi apagado: os 360 roteiros continuam em `data/animacoes/` e em `animacoes.json`, e o
  player continua no código. Para reativar, basta `MOSTRAR_ANIMACOES = true` em `app/index.html`.

## v2.13.0 — 2026-11-15

- **Resolução animada da Fuvest 2016 a 2027**: todas as 149 questões da Fuvest no banco.
- Questões de leitura e de várias alternativas a julgar ganharam uma tabela que marca cada
  alternativa (ou afirmativa) como verdadeira ou falsa, com o motivo em poucas palavras.
- Questões interdisciplinares (Química, Biologia, Geografia, Matemática): a animação trata a
  parte de Física e resume a outra disciplina em uma frase.
- Fuvest 2022 Q54 (anulada pela banca): a animação mostra o sentido pretendido e explica por
  que o módulo das alternativas está incorreto.
- Revisão visual e de fidelidade de todos os passos.

## v2.12.0 — 2026-11-15

- **Resolução animada da Unicamp 2016 a 2027**: 115 questões novas (a Unicamp 2017 Q58 já
  tinha). Com isso, todas as 116 questões da Unicamp no banco têm resolução animada.
- Questões interdisciplinares (Unicamp 2017 Q32, Q35, Q38; 2019 Q15, Q36, Q81): a animação
  trata a parte de Física e cita em uma frase a conclusão da outra disciplina.
- Notação da questão respeitada quando ela foge da regra geral das forças (ex.: Unicamp 2023
  Q33 usa \(\vec{f}_{at}\)).
- `pipeline animacoes verificar`: a conferência do gabarito no último passo passou a aceitar
  letra minúscula, como nas alternativas da Unicamp ("(a)").
- Revisão visual e de fidelidade de todos os passos.

## v2.11.0 — 2026-11-15

- **Resolução animada da Unesp 2016 a 2024**: 77 questões (2024: 8; 2023: 9; 2022: 7;
  2021: 8; 2020: 9; 2019: 12; 2018: 7; 2017: 8; 2016: 9). Com isso, todas as questões da
  Unesp no banco têm resolução animada.
- **Modelo de cena genérico `diagrama`**: a cena é descrita no próprio roteiro (retângulos,
  círculos, linhas, caminhos, setas e vetores, textos, rótulos em caixa, ângulos e cotas,
  agrupados em elementos) com animações `trajeto`, `girar`, `oscilar`, `aparecer` e `escalar`.
  Novas questões não exigem mais código no app, só o roteiro.
- **Publicação por arquivo**: o app lê os roteiros de `animacoes.json` (gerado por
  `python -m pipeline site`) e os junta aos da coleção `animacoes` do banco (o arquivo
  prevalece). Não é mais preciso gravar lotes no banco.
- Revisão visual e de fidelidade de todos os passos (sobreposições, legibilidade, sentidos de
  forças, campos e correntes, circuitos fechados).

## v2.10.0 — 2026-11-14

- **Resolução animada da Unesp 2025**: as 9 questões que faltavam (Q48, Q76, Q77, Q79, Q80,
  Q81, Q82, Q84, Q90; a Q78 já tinha). Nove modelos de cena novos: `rotas-velocidade-media`,
  `engrenagens-internas`, `lancamento-obliquo`, `manometro-gas`, `aumento-linear`, `onda-corda`,
  `soma-potencias`, `grafico-modulo` e `triangulo-pg`. Revisão visual de todos os passos.

## v2.9.1 — 2026-11-14

- **Revisão das resoluções animadas (pedidos do Lucas):**
  - Forças com letra maiúscula e notação de vetor, na cena e no texto: o atrito passou de
    *f* para \(\vec{F}_{\text{at}}\) (Unesp 2025 Q78); \(\vec{F}_{g}\) (Unesp 2026 Q77), \(\vec{F}\) e \(\vec{E}\)
    (Unesp 2026 Q81). Velocidade e acelerações também com seta.
  - Unesp 2026 Q77: ângulos com setor preenchido, arco escuro e rótulo em caixa; quadro dos
    ângulos alternos reescrito para caber.
  - Só o essencial: saíram a pulsação e o período (Unesp 2026 Q76), o exemplo numérico com
    porcentagens (ENEM 2023 Q98), a conferência por triângulos e o comentário das alternativas
    (Unicamp 2017 Q58), "direita e menor" e "a imagem ficou maior" (Unesp 2026 Q79).
  - Unesp 2026 Q82: o circuito agora é um caminho fechado (bateria → cursor do reostato →
    porção do reostato → bobina → bateria); antes um fio subia além da ligação e os pontos da
    corrente "vazavam" por ele. A lâmina não faz parte do circuito: só é aquecida pela bobina.
    A corrente aparece como "maior/menor", sem porcentagem.
  - Revisão visual de todos os passos das 10 resoluções (sobreposições e legibilidade).
- `docs/ANIMACOES.md`: regras de notação de forças, de só o essencial e de revisão visual.

## v2.9.0 — 2026-11-14

- **Resolução animada da Unesp 2026 (Q76–Q82)**, as 7 questões do ano. Sete modelos de cena
  novos: `mhs-sombra` (pêndulo, sombra em MHS e gráfico v × t com a secante), `rotacao-latitude`
  (Terra em corte, força gravitacional, aceleração centrípeta e latitude), `cadeia-energia`
  (da distância à altura, etapa por etapa), `espelho-convexo` (imagem pela equação de Gauss com o
  carro se aproximando do muro), `espectro-fototropismo` (λ e f no espectro; auxina no lado
  sombreado), `campo-uniforme` (placas, campo e íon) e `indicador-combustivel` (boia, reostato,
  corrente, lâmina bimetálica e ponteiro).
- **App:** textos das cenas com contorno da cor do fundo, para ficarem legíveis sobre linhas.

## v2.8.2 — 2026-11-14

- **Resolução animada, decisões do Lucas:** sem vídeo em Manim (`videos/manim_roteiro.py`
  removido); sem perguntas "Pense antes de avançar" (o conteúdo útil das respostas foi para
  o texto dos passos); sem controles para o aluno mudar valores (saiu o passo "Teste você
  mesmo" da Unesp 2025 Q78, e a resposta foi para o passo da segunda lei de Newton).
  O `animacoes verificar` recusa campos fora de `titulo`, `conceito`, `texto`, `equacoes` e
  `cena`.

## v2.8.1 — 2026-11-14

- **Correção do app:** na v2.8.0 o painel "Minha lista" ficava aberto e o botão "Fechar" não
  funcionava. O app dependia do esqueleto de documento que o artefato acrescentava (com a
  regra que esconde elementos com o atributo `hidden`), e a nova forma de publicar não o
  acrescenta. `app/index.html` agora é um documento completo (`<!DOCTYPE html>`, codificação,
  viewport e a regra do `hidden` no próprio CSS).

## v2.8.0 — 2026-11-14

- **Resolução animada (piloto).** Adicional à resolução comentada, que não muda: botão
  "Resolução animada" no app, com a cena desenhada à esquerda e o passo à direita (conceito
  físico, texto, equações uma a uma, pergunta "Pense antes de avançar"). Três questões:
  Unesp 2025 Q78 (plano inclinado, com controle da aceleração da esteira), ENEM 2023 Q98
  (circuito, com a corrente e o brilho das lâmpadas antes e depois da queima de L<sub>2</sub>)
  e Unicamp 2017 Q58 (área sob o gráfico v × t, com o carro percorrendo a via).
- **Roteiros** em `data/animacoes/<id>.json` (esquema `schemas/animacao.schema.json`,
  explicação em `docs/ANIMACOES.md`); coleção `animacoes` no banco do app e `animacoes.json`
  no site estático. Novo comando `python -m pipeline animacoes verificar|preparar`.
- **Vídeo em Manim** gerado do mesmo roteiro: `videos/manim_roteiro.py` (por enquanto só o
  modelo plano inclinado). Os vídeos ficam fora do git.

## v2.7.0 — 2026-11-14

- **Fórmulas no Einstein 2023–2027 (Prova I e Prova II).** Os 10 cadernos enviados pelo
  Lucas conferem com o sha256 do manifesto; as 30 questões passam na fidelidade sem aviso.
  Com esta versão, todas as provas do banco têm fórmulas em LaTeX.
- **Enunciados:** 6 têm fração empilhada ou radical no caderno e passaram a LaTeX: 2023
  Prova I Q39 (v = √(T/μ)); 2024 Prova I Q37 (razão m<sub>T</sub>/m<sub>L</sub>) e Q38
  (unidades de R e M); 2025 Prova I Q40 (alternativas C e E); 2025 Prova II Q03
  (T = 2,04 · √L); 2027 Prova I Q39 (relação f<sub>1</sub>/f<sub>2</sub> e alternativas A, C e E).
  Antes estavam em linha, com barra ou parênteses. Unidades que o caderno imprime em linha
  (J/(kg · °C), m/s²) continuam assim.
- **Resoluções:** 23 questões com frações, raízes e equações em LaTeX, mesmo conteúdo.

## v2.6.0 — 2026-11-14

- **Fórmulas na Acafe 2021–2026 (Verão e Inverno).** Os 12 PDFs enviados pelo Lucas (provas
  com gabarito e justificativas, fonte autorizada da Acafe) conferem com o sha256 do
  manifesto; as 84 questões passam na fidelidade sem aviso.
- **Enunciados:** 7 têm fração empilhada ou radical na prova e passaram a LaTeX:
  2021 Verão Q30 (alternativas; a B é a fração 10/1,6, antes transcrita com parênteses que a
  prova não tem); 2022 Verão Q32 (alternativas com raiz); 2023 Inverno Q29 (√2 = 1,4);
  2023 Verão Q34 (4√2 e 3√3); 2025 Inverno Q33 (√3 = 1,73); 2025 Verão Q35 (alternativas com
  √3, barras em linha como na prova); 2026 Inverno Q29 (alternativas, antes transcritas em
  linha com parênteses). O formulário e as constantes que vão no enunciado estão em linha na
  prova e continuam assim.
- **Resoluções:** 58 questões com frações, raízes e equações em LaTeX, mesmo conteúdo.
- **Conversor de fórmulas:** `\mp` (∓); espaço depois de sen/cos/log (antes saía "cosr");
  barra "/" dentro da fórmula sem o espaço de operador ("T₃/2").

## v2.5.0 — 2026-11-13

- **Fórmulas no ENEM 2017–2025.** Os 9 cadernos (2º dia, caderno 5 amarelo) enviados pelo
  Lucas conferem com o sha256 do manifesto; as 135 questões passam na fidelidade sem aviso
  (2018, 2021 e 2022 pelo texto de OCR).
- **Enunciados:** 13 têm fração empilhada no caderno e passaram a LaTeX: 2017 Q134 (todas as
  alternativas); 2018 Q117 (km/h); 2019 Q97 (1/3), Q109 (todas as alternativas) e Q122
  (k<sub>A</sub>/k<sub>B</sub>); 2021 Q126 (as duas fórmulas da condução e os dois ½); 2022 Q95 (m/s),
  Q111 (J/g°C e g/L), Q124 (W/m²) e Q126 (m/s²); 2023 Q93 (W/m²) e Q102 (M<sub>2</sub>/M<sub>1</sub>,
  ¼ e ½); 2025 Q115 (fórmula do nível sonoro). Unidades que o caderno imprime empilhadas
  também ficam empilhadas; as que imprime em linha continuam com barra (ex.: 2020 Q135,
  (P<sub>torre</sub>)/(P<sub>modelo</sub>)).
- **Resoluções:** 61 questões com frações, raízes e equações em LaTeX, mesmo conteúdo.
- **Conversor de fórmulas:** `\mathbf{...}` para letra reta em negrito (o ENEM imprime
  assim M<sub>1</sub>, M<sub>2</sub> e os índices A e B). No app o negrito vem do CSS; no .docx, do
  estilo da equação (o LibreOffice mostra essas letras em itálico; o Word, em negrito reto).

## v2.4.0 — 2026-11-13

- **Fórmulas na Unesp 2016–2026.** Os 11 PDFs enviados pelo Lucas conferem com o sha256 do
  manifesto; as 94 questões passam na fidelidade.
- **Enunciados:** 18 têm fração empilhada ou radical no caderno e passaram a LaTeX: 2016 Q79
  (\(4\sqrt{10}\)); 2017 Q79 e Q82; 2018 Q81; 2019 Q76 e Q81; 2020 Q78, Q79 e Q87; 2022 Q76
  (todas as alternativas), Q80 e Q81; 2023 Q87; 2024 Q86; 2025 Q77 e Q84; 2026 Q76 e Q79.
  Ficam em linha, como no caderno: 2019 Q73 (1/3), Q80 (t1/2) e Q85 (√3), 2020 Q77 (T²/D³)
  e Q78 (√2), 2023 Q76 e todas as unidades.
- **Resoluções:** 62 questões com frações, raízes e equações em LaTeX, mesmo conteúdo.
- **Variáveis retas:** a Unesp imprime as variáveis sem itálico; nas fórmulas dos enunciados
  (e das resoluções que citam essas variáveis) elas vão com `\mathrm{...}`.

## v2.3.0 — 2026-11-13

- **Fórmulas na Fuvest 2016–2026 e 2027.** Os 11 PDFs enviados pelo Lucas conferem com o
  sha256 do manifesto; as 137 questões de 2016–2026 passam na fidelidade sem aviso.
- **Enunciados:** 14 têm fração empilhada (ou radical com fração) no caderno e passaram a
  LaTeX: 2016 Q24 (½ e ¼ das alternativas), Q26 e Q28; 2019 Q17, Q20 e Q23; 2020 Q71;
  2021 Q46; 2023 Q36 e Q78; 2025 Q19; 2026 Q76; 2027 Q37 e Q42. Na 2023 Q78 e na 2016 Q28 a transcrição
  antiga tinha parênteses que não existem no caderno; saíram com a fração empilhada (os
  parênteses que o caderno imprime, como em 2019 Q17 e Q20, ficaram). Ficam com barra, como
  no caderno: 2016 Q12, 2017 Q76 (½ inclinado), 2019 Q45, 2020 Q75, 2021 Q49, 2022 Q54,
  2023 Q13 e Q77, 2025 Q22 e Q73, 2026 Q60 e todas as unidades.
- **Resoluções:** 91 questões com frações, raízes e equações em LaTeX (87 de 2016–2026 e
  4 de 2027), mesmo conteúdo.
- **Conversor de fórmulas:** `\boldsymbol` (vetor em negrito da 2021 Q46), número com
  milhar por ponto (`8.800`, padrão da Fuvest), `\log_{10}` com o índice junto do log,
  espaço antes de sen/cos/log e parênteses comuns que não esticam ao lado de frações.
- **Fuvest 2027:** com o PDF enviado depois (sha256 confere com o manifesto), as 12 questões
  passam na fidelidade sem aviso. Dois enunciados passaram a LaTeX: Q37 (\(P = \Delta E/\Delta t\),
  fração empilhada no "Note e adote") e Q42 (raiz cúbica com o traço do radical). VEF1/CVF da Q62
  e as unidades ficam em linha, como no caderno.
- **Unicamp 2027:** enunciados conferidos no caderno das provas S e W (mesmas questões,
  numeradas 48–55; o caderno registrado é o das provas R e Z). Nenhuma fração empilhada;
  nada mudou.

## v2.2.0 — 2026-11-13

- **Fórmulas na Unicamp 2016–2025 e 2027.** Cadernos de 2016 a 2025 (11 PDFs, com as duas
  provas de 2021) registrados no manifesto; as 102 questões passam a ter a fidelidade
  conferida pelo `verificar` (todas sem aviso).
- **Enunciados:** os traços de fração desenhados no caderno foram localizados no PDF e
  conferidos na imagem. Só 4 enunciados têm fração empilhada e passaram a LaTeX: 2018 Q41
  (\(g = GM/R^2\)), Q46 (\(F = i_S/i_V\)), Q47 (\(F = S^2T/\rho\kappa\)) e 2019 Q42 (fórmula de
  Φ, unidade de κ e razão \((T_A − T_B)/d\)). Na 2018 Q47 e na 2019 Q42 a transcrição antiga
  tinha parênteses que não existem no caderno; com a fração empilhada eles saíram. Ficam
  com barra, como no caderno: 2018 Q39 (i/e, √3/3), 2019 Q39 (1/3), 2020 Q77 (barra
  inclinada), 2021 Exatas e Humanas Q39, 2022 Q58, 2023 Q34 e todas as unidades.
- **Resoluções:** 78 resoluções reescritas (74 de 2016–2025 e 4 de 2027) com frações, raízes e equações em LaTeX
  , mesmo conteúdo. Conversões de unidade em cadeia ficaram em texto.
- **App:** espaço vertical em volta das fórmulas (frações em linhas seguidas não se
  sobrepõem mais) e o hífen dentro de fórmula vira sinal de menos.
- Os enunciados da Unicamp 2027 não foram revistos (o PDF não estava disponível).

## v2.1.0 — 2026-11-13

- **Fórmulas em LaTeX.** Trechos entre `\(` e `\)` no enunciado, na resolução e nas
  respostas são desenhados pelo app (fração empilhada, raiz, vetor, índices) e viram
  equação editável do Word na lista .docx. Um único analisador (`parseTex`, em
  `app/index.html`) gera MathML para a tela e OMML para o Word, sem biblioteca externa: o
  KaTeX foi descartado porque o artefato não carrega CSS nem fontes de CDN. Fórmula com
  erro aparece como código em vermelho na tela e como texto no .docx.
- **`verificar`:** acusa `\(` sem par, chave sem par e comando fora do subconjunto aceito;
  na comparação com o PDF, a fórmula é desmontada em texto simples.
- **Critérios:** a regra "fração empilhada vira barra em linha" foi trocada por LaTeX, só
  onde o caderno empilha; barra impressa em linha continua barra (docs/CRITERIOS.md).
- **Teste com a Unicamp 2026:** os 7 enunciados (Q8–Q14) foram conferidos com o caderno e
  não têm fração empilhada (só unidades em linha), então ficam como estavam. Resoluções de
  Q9, Q10, Q11, Q13 e Q14 reescritas em LaTeX, mesmo conteúdo. Caderno registrado no
  manifesto (`fontes/unicamp-2026-caderno.pdf`), o que passa a permitir conferir a
  fidelidade dessas questões.

## v2.0.0 — 2026-11-11

- **Modelo de dados: questões discursivas.** Novo campo `tipo` (`objetiva`, padrão quando
  ausente, ou `discursiva`). Nas discursivas, `gabarito` fica vazio e a resposta de cada item
  vai em `respostas` (`[{"item": "a", "texto": "..."}]`). Esquema, `verificar` (exige
  respostas, itens únicos e presentes no enunciado como `a)`), `publicar`, `site`,
  `rascunho` e `painel` atualizados. As 578 questões anteriores continuam válidas.
- **App:** selo "Discursiva" no cabeçalho da questão, respostas por item ao fim da
  resolução e no gabarito da lista .docx, filtro "Tipo de questão" (aparece quando há os
  dois tipos), ordenação por fase dentro do ano e fase no rótulo da lista.
- **Einstein (Vunesp), Vestibular 2023 a 2027**: 30 questões, 34 figuras.
  - Prova I (objetiva): Q36 a Q40 de cada ano (25 questões).
  - Prova II (discursiva): Q03 de cada ano (5 questões).
  - Por decisão do Lucas, o ano fica limpo e Prova I/Prova II vai no campo `edicao` (id
    `einstein-2025-prova-ii-q03`, pasta `einstein/2025-prova-ii`, `fase` `Prova II`), como
    na Acafe; não se usa mais o modelo `versao` da Unicamp 2021 A/B.
  - Gabaritos e respostas: `resolucao-propria` (o Lucas fará a conferência depois).
  - Fora: 2024 Prova I Q49 (Matemática, anos-luz) e 2025 Prova I Q33 (Química, GNV).
- **Unicamp 2021 no modelo novo**: as 16 questões saem de `versao` A/B ("2021 A", "2021 B"
  no app) para `edicao` (`Exatas e Humanas`, `Biológicas e Saúde`), com o ano limpo. Ids,
  pastas e figuras renomeados (`unicamp-2021a-q34` → `unicamp-2021-exatas-e-humanas-q34`;
  `unicamp-2021b-q56` → `unicamp-2021-biologicas-e-saude-q56`); no app, regravadas com os
  ids novos e as antigas apagadas. Listas salvas no navegador perdem essas questões e
  precisam ser remontadas. `versao` fica marcado como obsoleto.
- **Pipeline:** `registrar-prova --discursivas` e `--layout largura-total`; segmentador de
  largura total (uma questão por página, termina no quadro "RESOLUÇÃO E RESPOSTA");
  banca "Einstein" normalizada; id aceita edição com mais de uma palavra (`prova-ii`).

## v1.19.0 — 2026-11-10

- **Acafe, Vestibular de Medicina Verão 2021**: 7 questões, 5 figuras: Q29 a Q35.
  - Fonte e gabaritos como nas demais provas da Acafe (prova com gabarito e justificativas;
    `oficial`). Nesse PDF a alternativa correta vem logo depois do enunciado, seguida da
    justificativa, e as demais depois; por decisão do Lucas, as alternativas ficaram na ordem
    do PDF (A, B, C, D como impressas), registrado em `revisao.notas`.
  - Q30: dados do "FORMULÁRIO DE FÍSICA" da prova antes das alternativas; o valor lunar está
    impresso como "g_T = 1,6 m/s²" e foi transcrito literalmente (a resolução explica).
  - Q31 e Q32: as figuras não aparecem na renderização da página; recortadas da imagem
    embutida no PDF.

## v1.18.0 — 2026-11-10

- **Acafe, Vestibular de Medicina, Inverno 2021 a Inverno 2026** (10 provas): 70 questões,
  29 figuras, Q29 a Q35 de cada prova (Inverno 2021; Verão e Inverno de 2022 a 2025;
  Inverno 2026).
  - Fonte do enunciado e gabaritos: como na v1.17.0 (prova com gabarito e justificativas
    da Acafe; `oficial`).
  - Novo campo `edicao` (`Verão`/`Inverno`): entra no id (`acafe-2025-verao-q29`), na pasta e
    na `fase` (`Medicina · Verão`); o app mostra só o ano. As 7 questões da Verão 2026 foram
    renomeadas para `acafe-2026-verao-qNN` (e a figura para `acafe-2026-verao-q34-1.png`).
  - Fora, por decisão do Lucas: Verão 2023 Q37, Verão 2025 Q39 e Inverno 2025 Q36.
    Verão 2021 não entrou: a ordem aplicada das alternativas é desconhecida.
  - Erros da banca anotados nas resoluções (gabarito oficial mantido): Verão 2022 Q33,
    Inverno 2022 Q31 e Q32, Verão 2025 Q33.
  - Pipeline: `--edicao` em `registrar-prova`; segmentador Acafe aceita título "NN" sem
    parêntese e escolhe os títulos em sequência; `figuras detectar` apaga recortes antigos.

## v1.17.0 — 2026-11-10

- **Acafe, Vestibular de Medicina Verão 2026** (02/11/2025): 7 questões, 1 figura: Q29 a Q35
  (bloco de Física). Primeira prova da Acafe. Q36 (Química, fissão nuclear) ficou de fora por
  decisão do Lucas.
  - Fonte do enunciado: a prova com gabarito e justificativas divulgada pela própria Acafe
    (o caderno aplicado é de difícil acesso). Exceção à regra "prova comentada não é fonte",
    autorizada pelo Lucas; registrada em `revisao.notas` de cada questão.
  - Gabaritos: `oficial`, do mesmo documento; todas as resoluções próprias conferem.
  - O formulário e a tabela de constantes do início do bloco não são repetidos: só entra o
    dado de que a questão precisa (Q29: `CONSTANTES FÍSICAS` / g = 10 m/s², antes das alternativas).
  - Pipeline: segmentador de coluna única para chaves `acafe-*` (título "NN)" em negrito; o
    quadro "Dados da questão" fica fora do segmento); `registrar-prova` normaliza "Acafe".

## v1.16.0 — 2026-11-08

- **ENEM 2017, 2º dia (caderno 5 amarelo)**: 14 questões, 14 figuras: Q93, Q97, Q99, Q101,
  Q103, Q108, Q111, Q113, Q123, Q124, Q125, Q127, Q130 e Q134.
  - Gabaritos: `resolucao-propria`. Não foi encontrado gabarito do caderno amarelo acessível
    nesta sessão; a Q97 foi conferida pela questão correspondente do caderno azul.
  - Q103 ocupa a largura total da página.

## v1.15.0 — 2026-11-08

- **ENEM 2018, 2º dia (caderno 5 amarelo)**: 15 questões, 24 figuras: Q92, Q96, Q98, Q103,
  Q106, Q109, Q110, Q117, Q118, Q122, Q124, Q127, Q128, Q131 e Q133.
  - Gabaritos: `resolucao-propria`, todos conferidos com o gabarito oficial do caderno
    amarelo reproduzido pelo Guia da Carreira (sem anulações em Ciências da Natureza).
  - Camada de texto por OCR; a fidelidade foi conferida pela imagem. Q128 e Q131 ocupam a
    largura total da página.

## v1.14.0 — 2026-11-08

- **ENEM 2019, 2º dia (caderno 5 amarelo)**: 14 questões, 7 figuras: Q91, Q95, Q97, Q100,
  Q103, Q107, Q109, Q113, Q117, Q120, Q122, Q124, Q129 e Q132.
  - Gabaritos: `resolucao-propria`. Q91, Q95, Q97, Q100 e Q103 conferem com o gabarito
    não oficial do caderno amarelo publicado pelo Estratégia; Q120 e Q129 conferem com as
    questões correspondentes do caderno azul.
  - A camada de texto troca as ligaduras "fi" e "fl" (por exemplo "ftia", "fgiura"); o texto
    foi conferido pela imagem.

## v1.13.0 — 2026-11-08

- **ENEM 2020, 2º dia (caderno 5 amarelo)**: 16 questões, 18 figuras: Q92, Q94, Q96, Q101,
  Q106, Q108, Q109, Q112, Q113, Q122, Q125, Q130, Q131, Q133, Q134 e Q135.
  - Gabaritos: `resolucao-propria`. Não foi possível conferir com um gabarito publicado do
    caderno amarelo nesta sessão (os sites encontrados usavam outra numeração); a Q106 foi
    conferida pela questão correspondente do caderno azul. A anulação do INEP no caderno
    amarelo (Q114) não é de Física.
  - 'Eiffel' em Q135 e 'Pensando' em Q106 ficaram em `revisao.divergenciasAceitas`
    (ligadura e falso aviso do verificador).

## v1.12.0 — 2026-11-08

- **ENEM 2021, 2º dia (caderno 5 amarelo)**: 14 questões, 22 figuras: Q92, Q93, Q96, Q99,
  Q104, Q105, Q111, Q112, Q116, Q117, Q121, Q126, Q128 e Q134.
  - Gabaritos: `resolucao-propria`, conferidos com o gabarito do caderno amarelo publicado
    pela Estratégia Vestibulares.
  - Camada de texto cifrada; a fidelidade foi conferida pela imagem e pelo OCR. Três
    leituras erradas do OCR (Q112, Q116, Q128) ficaram registradas em
    `revisao.divergenciasAceitas`.

## v1.11.0 — 2026-11-08

- **ENEM 2022, 2º dia (caderno 5 amarelo)**: 16 questões, 26 figuras: Q92, Q95, Q96, Q99,
  Q101, Q105, Q108, Q111, Q115, Q118, Q119, Q124, Q126, Q129, Q132 e Q133.
  - Gabaritos: `resolucao-propria`, conferidos com o gabarito do caderno amarelo publicado
    pela Estratégia Vestibulares.
  - Camada de texto parcialmente cifrada; a fidelidade foi conferida pela imagem e pelo OCR.

## v1.10.0 — 2026-11-08

- **ENEM 2023, 2º dia (caderno 5 amarelo)**: 16 questões, 11 figuras: Q91, Q92, Q93, Q95,
  Q98, Q101, Q102, Q106, Q114, Q115, Q118, Q119, Q125, Q130, Q133 e Q135.
  - Gabaritos: `resolucao-propria`, conferidos com o gabarito do caderno amarelo publicado
    pela Estratégia Vestibulares.
  - O caderno de 2023 mistura blocos em largura total da página (páginas 2, 3, 10, 11, 13
    e 15) com o layout em duas colunas; o segmentador assume duas colunas, então essas
    questões foram lidas e recortadas pela página inteira.

## v1.9.0 — 2026-11-08

- **ENEM 2024, 2º dia (caderno 5 amarelo)**: 16 questões, 29 figuras: Q95, Q100, Q101,
  Q102, Q103, Q104, Q106, Q109, Q110, Q114, Q117, Q118, Q119, Q124, Q126 e Q129.
  - Gabaritos: `resolucao-propria`, conferidos com o gabarito do caderno amarelo publicado
    pela Estratégia Vestibulares, que incorpora as retificações do INEP. O PDF do INEP
    não pôde ser baixado na sessão.
  - **Q102 anulada pelo INEP**: com os dados, a eficiência sairia maior que 100%. Mantida
    com a resposta provavelmente pretendida (B, razão invertida) e aviso na resolução.

## v1.8.0 — 2026-11-08

- **ENEM 2025, 2º dia (Ciências da Natureza, caderno 5 amarelo)**: 14 questões, 24 figuras:
  Q91, Q97, Q103, Q104, Q105, Q113, Q115, Q118, Q120, Q124, Q125, Q128, Q130 e Q135.
  Primeira prova do ENEM no banco (banca "ENEM", fase "2º dia · Caderno Amarelo").
  - Gabaritos: `oficial` (INEP, caderno amarelo, aplicação regular). Lido na transcrição
    publicada pelo O Povo em 19/11/2025, porque o PDF do INEP não pôde ser baixado na
    sessão; as 13 respostas conferem com as resoluções.
  - **Q115 anulada pelo INEP** (uma das três questões anuladas do 2º dia, por suspeita de
    vazamento). Mantida no banco com a resposta pretendida (C) e aviso na resolução.
  - Alternativas transcritas como `(A) ...`, e as alternativas-desenho viram uma figura por
    alternativa. A fórmula do nível sonoro da Q115 é desenho no caderno e foi transcrita
    em linha.
- Registrados no manifesto os cadernos do 2º dia do ENEM 2017–2025 (caderno 5, amarelo).
  Os de 2018, 2021 e 2022 têm a camada de texto cifrada e foram passados pelo OCR
  (`camadaTexto: "ocr"`).

## v1.7.0 — 2026-11-02

- **Unesp 2016–2020, 1ª fase (Prova de Conhecimentos Gerais)**: 45 questões, 58 figuras.
  - Bloco de Física: 2016 Q76–Q83; 2017 Q77–Q83; 2018, 2019 e 2020 Q76–Q82.
  - Interdisciplinares aprovadas pelo Lucas: 2016 Q74; 2017 Q70; 2019 Q64, Q66, Q73, Q74
    e Q85; 2020 Q70 e Q87. Ficaram de fora, por decisão dele, 2017 Q71, 2019 Q50 e
    2020 Q73.
  - Gabaritos: `oficial` em 2016 (Vunesp, versão 1, conferido questão a questão);
    `resolucao-propria` em 2017–2020.
- Fuvest 2027: banca padronizada como "Fuvest" (estava "fuvest"); `registrar-prova` passa
  a normalizar o nome da banca.

## v1.6.0 — 2026-11-01

- **Fuvest 2027, 1ª fase (Prova de Conhecimentos Gerais, caderno V1, 80 questões)**:
  12 questões, 9 figuras: Q35, Q36, Q37, Q42, Q56, Q73, Q74, Q75 e as interdisciplinares
  em dúvida aprovadas pelo Lucas, Q28 (oceanos), Q41 (papel com álcool e água), Q54
  (Tensão de Hubble) e Q62 (espirometria).
  - Gabaritos: `resolucao-propria`; a prova foi aplicada em 01.11.2026 e o gabarito oficial
    ainda não foi conferido.

## v1.5.0 — 2026-11-01

- **Unesp 2021–2026, 1ª fase (Prova de Conhecimentos Gerais)**: 49 questões, 72 figuras.
  - Bloco de Física (Q76–Q82) de cada ano, incluídas as de tema de outra disciplina
    (2021 Q77 respiração/pressão, Q81 escala Richter; 2024 Q77 DNA, Q80 icterícia, Q81
    mielina; 2026 Q80 auxina).
  - Interdisciplinares em dúvida aprovadas pelo Lucas: 2021 Q84 (Mach), 2023 Q70 (gases,
    Química), 2023 Q87 (MUV, Matemática), 2024 Q86 (centro de massa), 2025 Q48 (velocidade
    média, Geografia), 2025 Q84 (escalas termométricas), 2025 Q90 (MRU, Matemática).
  - 2021 e 2022: caderno da área de Biológicas (001), registrado na fonte.
  - Gabaritos: `oficial` em 2021, 2024 e 2025 (gabarito Vunesp, versão 1, conferido questão
    a questão com as resoluções); `resolucao-propria` em 2022 e 2026 (conferem com gabaritos
    divulgados por cursinhos) e 2023 (não conferido com fonte externa).
- Script de trabalho `aplicar.py` (fora do git, em `trabalho/final/`) passou a aceitar a banca.

## v1.4.0 — 2026-11-01

- **Site estático para o GitHub Pages**: novo comando `python -m pipeline site` (gera `site/`
  com o app, `questoes.json` e as figuras) e workflow `.github/workflows/pages.yml`, que
  verifica, gera e publica o site a cada envio ao `main`.
- App: fora do Claude, lê `questoes.json` e baixa a lista .docx direto pelo navegador;
  dentro do artefato, continua igual.
- Correção no app: em telas estreitas (celular), o botão **Filtros** não aparecia, porque
  uma regra CSS posterior escondia o botão; agora ele aparece e abre o painel de tópicos.

## v1.3.0 — 2026-11-01

- **Fuvest 2016–2019, 1ª fase (prova V)**: 56 questões, 41 figuras.
  - 2016 (15): Q3, Q12, Q24–Q35, Q44 · 2017 (14): Q57–Q68, Q76, Q90 ·
    2018 (13): Q1–Q11, Q23, Q34 · 2019 (14): Q13, Q15–Q24, Q27, Q36, Q45.
  - Incluídas as interdisciplinares em dúvida aprovadas pelo Lucas (Química com Física,
    Matemática e Biologia com Física); 2016 Q67 (Geografia, ventos) ficou de fora por
    decisão dele.
  - Gabaritos: `resolucao-propria` (não conferidos com o gabarito oficial).
- Pipeline (`segmentar`): títulos em negrito 9 pt (Fuvest 2016–2017) e títulos desenhados
  como vetor, achados por OCR (Fuvest 2018), com ajuste manual opcional em
  `trabalho/<prova>/titulos-ajustes.json`.
- No PDF de 2016 (e em fórmulas de 2017) o editor de equações não deixa texto: essas partes
  foram transcritas da imagem; as divergências do `verificar` estão registradas na questão.
- Banco: 253 questões (116 Unicamp + 137 Fuvest); tópicos sem questão: 34 → 32.

## v1.2.0 — 2026-11-01

- **Fuvest 2020–2026, 1ª fase (Prova de Conhecimentos Gerais, prova V/V1)**: 81 questões,
  93 figuras. Primeira banca nova depois da Unicamp.
  - 2020 (14): Q2, Q8, Q11, Q69–Q79 · 2021 (11): Q45–Q55 · 2022 (10): Q50–Q57, Q72, Q75 ·
    2023 (13): Q13, Q36, Q54, Q66, Q67, Q70–Q73, Q76–Q79 · 2024 (12): Q24–Q27, Q29, Q42,
    Q51, Q55, Q57, Q71–Q73 · 2025 (12): Q18, Q19, Q22, Q23, Q32, Q33, Q52, Q59, Q61, Q62,
    Q73, Q74 · 2026 (9): Q25, Q60, Q61, Q71–Q73, Q75–Q77.
  - Por pedido do Lucas, entraram também as interdisciplinares marcadas "em dúvida",
    inclusive Química com Física forte (2020 Q2, Q8, Q11; 2022 Q75; 2023 Q71; 2024 Q25,
    Q29; 2025 Q73) e outras áreas (2022 Q57 Geografia; 2023 Q36 e 2025 Q52 Matemática;
    2023 Q70 e 2026 Q25 Inglês).
  - Gabaritos: 2025 conferido no gabarito oficial (fuvest.br) → `oficial`; demais anos com
    `resolucao-propria` (2024 e 2026 conferem com o gabarito divulgado).
  - **2022 Q54 foi anulada pela Fuvest** (nenhuma alternativa traz a velocidade v); entra
    com o gabarito pretendido (B) e aviso na resolução e em `revisao.notas`.
- Pipeline:
  - `segmentar` reconhece o título das questões da Fuvest (só o número, "01" ou "{ 01}").
  - Novo comando `ocr` (etapa 2b): texto de referência por OCR para cadernos com camada de
    texto ilegível (Fuvest 2021, "Caderno Reserva"); o manifesto marca `camadaTexto: "ocr"`
    e o `verificar` confere a fidelidade contra `fontes/<arquivo>.ocr.txt`.
- Banco: 197 questões (116 Unicamp + 81 Fuvest); tópicos sem questão: 71 → 34.

## v1.1.0 — 2026-11-01

- Unicamp 2027, 1ª fase (provas R e Z): 7 questões de Física (Q8 a Q14), 6 figuras.
  Gabaritos de resolução própria (`resolucao-propria`), a conferir com o gabarito
  oficial da Comvest quando sair.
  - Q8 onda gravitacional (MRU, notação científica) · Q9 aceleração da gravidade ·
    Q10 polia móvel invertida · Q11 atrito cinético · Q12 gálio, calor sensível e
    latente (alternativas em gráfico) · Q13 potência elétrica · Q14 resistores em paralelo.
  - Ficaram de fora Q25 (Química com gás e pressão: regra "por enquanto, não"),
    Q31, Q50 e Q53 (Física só como cenário).
- Banco: 116 questões.
- Correção: `.gitignore` ignorava `data/fontes/` (padrão `fontes/`); passou a `/fontes/`,
  e o `data/fontes/manifesto.json` entra no repositório.

## v1.0.0 — 2026-10-31

- 109 questões de Física da Unicamp, 1ª fase, 2016–2026 (inclui 2021 A e 2021 B),
  todas com resolução comentada, gabarito e tópicos; 60 figuras dos cadernos oficiais.
- App de consulta (uma questão por vez, filtro por interseção de tópicos, banca e ano,
  lista de exercícios exportada em .docx com resoluções ao final).
- Pipeline de importação em 9 etapas (`python -m pipeline`) com verificação de
  fidelidade ao PDF oficial.
- Documentação: fluxo de trabalho, critérios editoriais, modelo de dados, roadmap SaaS.
