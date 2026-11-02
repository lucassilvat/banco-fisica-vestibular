# Histórico de versões

Cada versão corresponde a um lote de importação ou a uma mudança no app/pipeline.
Formato: `vMAIOR.MENOR.CORREÇÃO` — MENOR sobe a cada prova importada; MAIOR, em mudanças
de modelo de dados; CORREÇÃO, em correções de questões já publicadas.

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
