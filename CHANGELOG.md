# Histórico de versões

Cada versão corresponde a um lote de importação ou a uma mudança no app/pipeline.
Formato: `vMAIOR.MENOR.CORREÇÃO` — MENOR sobe a cada prova importada; MAIOR, em mudanças
de modelo de dados; CORREÇÃO, em correções de questões já publicadas.

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
