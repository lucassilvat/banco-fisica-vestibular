# Histórico de versões

Cada versão corresponde a um lote de importação ou a uma mudança no app/pipeline.
Formato: `vMAIOR.MENOR.CORREÇÃO` — MENOR sobe a cada prova importada; MAIOR, em mudanças
de modelo de dados; CORREÇÃO, em correções de questões já publicadas.

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
