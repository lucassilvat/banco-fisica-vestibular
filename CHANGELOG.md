# Histórico de versões

Cada versão corresponde a um lote de importação ou a uma mudança no app/pipeline.
Formato: `vMAIOR.MENOR.CORREÇÃO` — MENOR sobe a cada prova importada; MAIOR, em mudanças
de modelo de dados; CORREÇÃO, em correções de questões já publicadas.

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
