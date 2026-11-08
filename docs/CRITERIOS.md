# Critérios editoriais

## Fidelidade ao enunciado (regra principal)

- O enunciado é reproduzido **exatamente como foi cobrado no dia da prova**: sem frase de
  abertura, sem contexto acrescentado, sem reescrever, sem trocar verbo de comando
  ("calcule" não vira "determine"), sem mencionar figura que o original não menciona.
- Fonte: **caderno de questões aplicado**, da banca. Prova comentada, resolução de
  cursinho ou site de terceiros não servem como fonte do texto.
- Se o texto literal não puder ser obtido (PDF escaneado ilegível, trecho faltando),
  a questão **não entra**; registre o motivo no commit ou na conversa.
- Erros do original ficam como estão (ex.: Unicamp 2017 Q60, alternativas sem "×").

## Convenções de transcrição

| Situação | Como fica |
|---|---|
| Itálico, negrito, sublinhado | `<i>`, `<b>`, `<u>` (nenhuma outra marcação HTML) |
| Índices e expoentes | `<sub>`, `<sup>`: `<i>v</i><sub>0</sub>`, `m/s<sup>2</sup>` |
| Vetor | letra + seta combinante: `<i>F</i>⃗` |
| Fração empilhada | em linha com barra: `<i>g</i> = <i>GM</i>/<i>R</i><sup>2</sup>` |
| Figura | `[[figura N]]` numa linha própria, no ponto em que aparece |
| Legenda/fonte da figura | texto, logo abaixo da figura |
| Texto comum a várias questões | repetido no início de cada uma, com o título original |
| Instrução geral ("use g = 10 m/s²") | repetida nas questões em que vale, conforme a prova |
| Alternativas | no fim, uma por linha, com o rótulo do caderno: `a) ...` (Unicamp), `(A) ...` (Fuvest, Unesp, ENEM; no ENEM a letra é um círculo, transcrito como `(A)`) |
| "Note e adote" (Fuvest) | bloco de texto antes das alternativas, começando por `Note e adote:` |
| Tabela | figura recortada do caderno |

## O que entra no banco

Entra toda questão cuja **resolução depende de um conceito de Física do Ensino Médio**,
inclusive as interdisciplinares em que a outra disciplina também é necessária
(ex.: 2019 Q15 Física e Literatura, Q36 Física e Geografia, Q81 Física e História;
2017 Q32, Q35, Q38; 2018 Q38 em inglês; 2020 Q79 com contexto de Biologia).

Não entra questão em que a Física só aparece como cenário e não é usada na resolução
(ex.: 2018 Q32 e Q35, de Inglês).

**Química com conteúdo físico forte**: na importação da Fuvest 2020–2026 o Lucas mandou
incluir (ex.: Fuvest 2020 Q2, Q8, Q11; 2023 Q71). As da Unicamp que ficaram de fora
(2020 Q45 a Q48, 2021 B Q33, 2027 Q25) continuam em aberto até nova decisão.

## Tópicos

- Só ids existentes em `data/taxonomia.json`. Para criar um tópico novo, edite a
  taxonomia (o `id` é gerado do nome) e o array `AREAS` em `app/index.html`.
- De 1 a 4 tópicos, do mais central ao acessório. Em interdisciplinares, só os físicos.

## Resolução

- Passo a passo numerado, com unidades e conversões explícitas.
- Usar os valores aproximados que a própria prova manda usar (π = 3, g = 10 m/s²).
- Quando a alternativa correta depender de uma leitura discutível (ex.: 2017 Q38, energia
  ∝ v² ou v³), registrar a observação no fim da resolução.
- `gabaritoFonte`: `oficial`, `prova-comentada-oficial` ou `resolucao-propria`.
