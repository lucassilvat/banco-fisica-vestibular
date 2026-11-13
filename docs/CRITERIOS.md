# Critérios editoriais

## Fidelidade ao enunciado (regra principal)

- O enunciado é reproduzido **exatamente como foi cobrado no dia da prova**: sem frase de
  abertura, sem contexto acrescentado, sem reescrever, sem trocar verbo de comando
  ("calcule" não vira "determine"), sem mencionar figura que o original não menciona.
- Fonte: **caderno de questões aplicado**, da banca. Prova comentada, resolução de
  cursinho ou site de terceiros não servem como fonte do texto.
  Exceção autorizada pelo Lucas: Acafe, cuja prova com gabarito e justificativas é divulgada
  pela própria banca (o caderno aplicado é de difícil acesso).
- Se o texto literal não puder ser obtido (PDF escaneado ilegível, trecho faltando),
  a questão **não entra**; registre o motivo no commit ou na conversa.
- Erros do original ficam como estão (ex.: Unicamp 2017 Q60, alternativas sem "×").

## Convenções de transcrição

| Situação | Como fica |
|---|---|
| Itálico, negrito, sublinhado | `<i>`, `<b>`, `<u>` (nenhuma outra marcação HTML) |
| Índices e expoentes | `<sub>`, `<sup>`: `<i>v</i><sub>0</sub>`, `m/s<sup>2</sup>` |
| Vetor | letra + seta combinante: `<i>F</i>⃗` |
| Fração empilhada, raiz, fórmula montada | LaTeX entre `\(` e `\)`, só quando o caderno imprime assim: `\(g = \dfrac{GM}{R^2}\)` (ver "Fórmulas" abaixo) |
| Barra em linha (`1/3`, `m/s`) | como no caderno, com barra |
| Figura | `[[figura N]]` numa linha própria, no ponto em que aparece |
| Legenda/fonte da figura | texto, logo abaixo da figura |
| Texto comum a várias questões | repetido no início de cada uma, com o título original |
| Instrução geral ("use g = 10 m/s²") | repetida nas questões em que vale, conforme a prova |
| Alternativas | no fim, uma por linha, com o rótulo do caderno: `a) ...` (Unicamp), `(A) ...` (Fuvest, Unesp, ENEM; no ENEM a letra é um círculo, transcrito como `(A)`) |
| Alternativas (Acafe) | `A. ...`, como no caderno |
| Formulário/constantes (Acafe) | não se repete o quadro; só o dado necessário, como bloco antes das alternativas, com o título literal da prova (`CONSTANTES FÍSICAS`, `Dados para realização das questões` ou `DADOS PARA REALIZAÇÃO DAS QUESTÕES`) |
| Edição (Acafe) | Verão/Inverno é descritivo: campo `edicao` e `fase` (`Medicina · Inverno`); a prova fica marcada só com o ano |
| Edição (Einstein) | Prova I (objetiva) e Prova II (discursiva) são do mesmo vestibular e ano: campo `edicao` e `fase` (`Prova I`, `Prova II`); o ano fica limpo (a Unicamp 2021 também usa `edicao`: `Exatas e Humanas`, `Biológicas e Saúde`) |
| Itens de questão discursiva | `a) ...`, `b) ...` no fim do enunciado, um por linha, sem o negrito do rótulo; o quadro "RESOLUÇÃO E RESPOSTA" e a marca d'água "RASCUNHO" ficam fora |
| Título de texto de apoio (Einstein) | linha própria, antes do texto (ex.: `O “pêndulo humano” é atração radical na Serra Catarinense`) |
| Listas com marcador (•) | um item por linha, começando por `• ` |
| Itens I, II... e ( ) (Acafe) | um por linha; o destaque em vermelho da alternativa correta não é reproduzido; legendas "FIGURA N" vão no recorte |
| "Note e adote" (Fuvest) | bloco de texto antes das alternativas, começando por `Note e adote:` |
| Tabela | figura recortada do caderno |

## Fórmulas (LaTeX)

Desde a v2.1.0, frações, raízes e equações podem ser escritas em LaTeX entre `\(` e `\)`.
O app desenha a fórmula (MathML) e a lista .docx a converte em equação editável do Word.
Não se usa `$...$`, porque o banco tem "R$".

- **Enunciado:** empilha-se só o que o caderno imprime empilhado (fração com traço,
  radical, expoente sobre fração). Barra em linha impressa no caderno (`1/3 do volume`,
  `(T²/R³)`, todas as unidades como `m/s²`) fica com barra. Cada fórmula é conferida contra
  a imagem da questão. Fórmula desenhada pela banca e transcrita assim deixa de ser
  divergência a registrar.
- **Resolução e respostas:** texto nosso, então frações e equações vão em LaTeX sempre que
  ajudam a leitura. Conversões de unidade em cadeia podem ficar em texto.
- **Escrita:** vírgula decimal e milhar com espaço como no resto do banco (`3,6`, `54 000`);
  índice que é palavra fica reto (`R_{\text{eq}}`, `F_{\text{res}}`); índice que é letra
  segue a prova (`U_b`); unidade fica fora da fórmula (`\(... = 0,5\) A`); módulo com
  `\left|a\right|`; `\dfrac` para frações; `\sen` para seno. Variável que o caderno
  imprime reta (padrão da Unesp) vai com `\mathrm{...}`, para não virar itálico; reta e em
  negrito (ENEM), com `\mathbf{...}`. Unidade que o caderno imprime empilhada (`km` sobre
  `h`) também vai empilhada: `\(108\,\dfrac{\text{km}}{\text{h}}\)`.
- **Comandos aceitos:** `\frac \dfrac \tfrac \sqrt \sqrt[n] \vec \boldsymbol \text \mathrm \left \right`,
  letras gregas (`\Delta`, `\rho`...), `\cdot \times \approx \neq \leq \geq \Rightarrow \to
  \propto \pm \infty \circ`, `\sen \cos \tg \log \ln`, espaços `\, \; \quad`; índices `_` e `^`.
  Fora disso o `verificar` acusa erro (a lista fica em `LATEX_CMDS`, em `pipeline/verificar.py`,
  e precisa bater com `parseTex` em `app/index.html`).

## O que entra no banco

Entra toda questão cuja **resolução depende de um conceito de Física do Ensino Médio**,
inclusive as interdisciplinares em que a outra disciplina também é necessária
(ex.: 2019 Q15 Física e Literatura, Q36 Física e Geografia, Q81 Física e História;
2017 Q32, Q35, Q38; 2018 Q38 em inglês; 2020 Q79 com contexto de Biologia).

Não entra questão em que a Física só aparece como cenário e não é usada na resolução
(ex.: 2018 Q32 e Q35, de Inglês).

**Química com conteúdo físico forte**: na importação da Fuvest 2020–2026 o Lucas mandou
incluir (ex.: Fuvest 2020 Q2, Q8, Q11; 2023 Q71). As da Unicamp que ficaram de fora
(2020 Q45 a Q48, 2021 Biológicas e Saúde Q33, 2027 Q25) continuam em aberto até nova decisão.

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
- **Questão discursiva** (`tipo: "discursiva"`): sem `gabarito` (fica vazio); a resposta
  final de cada item vai em `respostas` (`[{"item": "a", "texto": "..."}]`, com as unidades),
  e a resolução separa os itens com linhas `a)`, `b)` antes dos passos numerados.
