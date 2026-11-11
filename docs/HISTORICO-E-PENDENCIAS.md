# Histórico de decisões e pendências

Resumo do trabalho feito até a v1.0.0 (outubro de 2026), para quem continuar o projeto
numa conversa nova. As regras permanentes estão em `CLAUDE.md` e `docs/CRITERIOS.md`.

## Onde as coisas estão

| O quê | Onde |
|---|---|
| App publicado (artefato privado, com banco de dados e figuras próprios) | https://claude.ai/artifact/R1zq9bpSmPV41kyzg12dxA |
| Código e dados versionados | github.com/lucassilvat/banco-fisica-vestibular (privado, ramo `main`) |
| Site público (GitHub Pages) | gerado por `python -m pipeline site` e publicado pelo workflow `pages.yml` a cada envio ao `main`; precisa ser ativado em Settings › Pages |
| PDFs oficiais | com o Lucas (fora do git); nomes e sha256 em `data/fontes/manifesto.json` |

O app lê as questões do banco do artefato. Para mudar o app, edita-se `app/index.html` e
publica-se de novo **no mesmo artefato** (pelo link acima, nunca um artefato novo).
Para gravar questões, usam-se os lotes da etapa `publicar` (docs/WORKFLOW.md).

## Como chegamos aqui

1. App criado com filtro por interseção de tópicos (151 tópicos em 15 áreas).
2. Primeira importação (Unicamp 2026) feita a partir da **Prova Comentada**. O Lucas
   pediu para apagar tudo e refazer a partir dos **cadernos aplicados**: daí a regra de que
   prova comentada não é fonte de enunciado (só de gabarito).
3. Importados os cadernos da Unicamp 2022–2026, depois 2016–2021 (2021 teve duas provas:
   A = Exatas e Tecnológicas / Humanas e Artes, provas E e G; B = Biológicas e Saúde,
   provas Q e Z; no app aparecem como "2021 A" e "2021 B").
4. App mudou para **uma questão por vez**, com navegação, resolução no fim de cada
   questão e **seleção de questões para lista .docx** (questões primeiro, gabarito e
   resoluções ao final).
5. Inclusões pedidas pelo Lucas depois da triagem automática: 2020 Q79; 2019 Q15, Q36,
   Q81; 2018 Q38; 2017 Q32, Q35, Q38. Daí o critério: entra toda questão cuja resolução
   depende de Física, mesmo interdisciplinar.
6. Correção: figura da 2026 Q10 estava cortada; refeita.
7. Projeto estruturado em repositório (dados separados do app, pipeline, documentação) e
   enviado ao GitHub como v1.0.0.

8. v1.1.0: Unicamp 2027 (provas R e Z), Q8–Q14. Fase registrada como "1ª fase · Prova R".
9. v1.2.0: Fuvest 2020–2026, 1ª fase (prova V; V1 em 2025 e 2026), 81 questões. Segmentador
   adaptado ao título "NN" da Fuvest. O Lucas pediu para incluir **todas** as candidatas,
   inclusive as "em dúvida" (Química com Física forte e interdisciplinares de Geografia,
   Matemática e Inglês). O PDF de 2021 ("Caderno Reserva") tem camada de texto ilegível:
   transcrição pela imagem e conferência por OCR (`python -m pipeline ocr`).
   Na Fuvest, "Note e adote" é transcrito como bloco de texto antes das alternativas,
   começando por "Note e adote:"; textos comuns ("TEXTO PARA AS QUESTÕES...") repetidos
   em cada questão; tabelas entram como figura.
10. v1.3.0: Fuvest 2016–2019 (prova V), 56 questões, com as interdisciplinares em dúvida
    (menos 2016 Q67, Geografia, que o Lucas mandou deixar de fora). Em 2016 e 2017 as
    alternativas são "a)" minúsculas, como no caderno. O texto do caderno de 2018 está
    na camada de texto, mas os números das questões não: o segmentador os acha por OCR.
11. v1.5.0: Unesp 2021–2026 (1ª fase, Conhecimentos Gerais), 49 questões: Q76–Q82 de cada
    ano e 7 interdisciplinares em dúvida aprovadas (2021 Q84; 2023 Q70 e Q87; 2024 Q86;
    2025 Q48, Q84 e Q90). Questões só de Química ficaram de fora a pedido do Lucas.
    2021 e 2022 são os cadernos da área de Biológicas. Alternativas "(A)"; tabelas,
    alternativas-desenho e rótulos "Figura N" entram como figura; fórmulas desenhadas
    (editor de equações) são transcritas da imagem com a divergência registrada.

12. v1.6.0: Fuvest 2027 (caderno V1, 80 questões em vez de 90), 12 questões, com as 4
    interdisciplinares em dúvida (Q28, Q41, Q54, Q62). A camada de texto usa letras
    matemáticas Unicode nas fórmulas; o enunciado foi transcrito da imagem.

13. v1.7.0: Unesp 2016–2020, 45 questões (bloco de Física e 9 interdisciplinares aprovadas;
    2017 Q71, 2019 Q50 e 2020 Q73 ficaram de fora por decisão do Lucas). Textos comuns
    ("Leia o texto para responder às questões...") repetidos em cada questão. A banca da
    Fuvest 2027 foi corrigida para "Fuvest" e o `registrar-prova` normaliza o nome.

14. v1.8.0: ENEM 2025 (2º dia, caderno 5 amarelo), 14 questões. Primeira prova do ENEM.
    Lista aprovada pelo Lucas para 2017–2025 (126 certas e 9 das 22 em dúvida):
    - 2017: 93, 97, 99, 101, 103, 108, 111, 113, 123, 124, 125, 127, 130, 134
    - 2018: 92, 96, 98, 103, 106, 109, 110, 117, 118, 122, 124, 127, 128, 131, 133
    - 2019: 91, 95, 97, 100, 103, 107, 109, 113, 117, 120, 122, 124, 129, 132
    - 2020: 92, 94, 96, 101, 106, 108, 109, 112, 113, 122, 125, 130, 131, 133, 134, 135
    - 2021: 92, 93, 96, 99, 104, 105, 111, 112, 116, 117, 121, 126, 128, 134
    - 2022: 92, 95, 96, 99, 101, 105, 108, 111, 115, 118, 119, 124, 126, 129, 132, 133
    - 2023: 91, 92, 93, 95, 98, 101, 102, 106, 114, 115, 118, 119, 125, 130, 133, 135
    - 2024: 95, 100, 101, 102, 103, 104, 106, 109, 110, 114, 117, 118, 119, 124, 126, 129
    - 2025 (importada): 91, 97, 103, 104, 105, 113, 115, 118, 120, 124, 125, 128, 130, 135
    Ficaram de fora, por decisão dele: 2017 Q91, Q102, Q121; 2018 Q100; 2019 Q116, Q131;
    2020 Q99, Q118; 2021 Q127; 2022 Q130; 2024 Q98; 2025 Q101, Q110.
    Particularidades do ENEM: as questões de Física vêm misturadas com Biologia e Química
    (a triagem automática não basta); o segmentador acerta as 90 questões (91–180), mas as
    regiões de coluna (x ≈ 0–283 e 258–567) sobrepõem a outra coluna e cortam questões que
    mudam de coluna. Por isso a transcrição e as caixas das figuras foram feitas pela
    imagem das colunas (página dividida em x ≈ 290). Os cadernos de 2022, 2024 e 2025 têm
    marca d'água "ENEM20xx" na camada de texto.

15. v1.9.0–v1.16.0: ENEM 2024 → 2017 (2º dia, caderno 5 amarelo), 121 questões, com as
    listas do item 14. Com 2025, o ENEM soma 135 questões.
    - Gabaritos: o download do INEP é bloqueado nesta sessão, então todos ficaram
      `resolucao-propria`, com a fonte da conferência em `revisao.notas`: 2024–2021 pelo
      Estratégia (caderno amarelo), 2018 pelo gabarito oficial reproduzido no Guia da
      Carreira, 2019 em parte (Estratégia e questões correspondentes do caderno azul).
      2020 e 2017 não tinham gabarito do amarelo acessível; só uma questão de cada ano foi
      conferida pelo caderno azul. Todas as resoluções próprias bateram com as referências.
    - Anulada: 2024 Q102 (gabarito pretendido B, com aviso no início da resolução, como na
      Fuvest 2022 Q54). As anulações de 2020 (Q114) e 2021 não são de Física.
    - Camada de texto: 2021 cifrada e 2018 por OCR (conferidos pela imagem); 2019 troca as
      ligaduras "fi"/"fl"; 2017 e 2019 usam U+2126 para Ω (o banco usa U+03A9).
    - Layout: várias questões ocupam a largura total da página (2023: páginas 2, 3, 10, 11,
      13 e 15; 2021 Q104; 2020 Q106, Q125, Q131; 2019 Q100, Q107, Q124; 2018 Q128, Q131;
      2017 Q103, Q130). Foram lidas e recortadas pela página inteira.
    - Q125 de 2020 é uma tirinha (Garfield) reproduzida do caderno, como figura da prova.

16. v1.17.0: Acafe, Vestibular de Medicina Verão 2026, Q29–Q35 (bloco de Física). Primeira
    prova da Acafe: coluna única, alternativas "A.", itens em algarismos romanos. O Lucas
    autorizou usar como fonte do enunciado a prova com gabarito e justificativas divulgada
    pela própria Acafe (o caderno aplicado é de difícil acesso) e marcar o gabarito como
    `oficial`. Decisão dele: não repetir o formulário/constantes do bloco; só o dado necessário
    entra na questão (Q29: g = 10 m/s², bloco "CONSTANTES FÍSICAS" antes das alternativas).
    Q36 (Química, fissão) ficou de fora. Observações: a justificativa da banca para a Q33
    diz "cai para 1m/s" (o certo é 0,1 m/s); na Q29 a banca usa distância percorrida como
    "velocidade escalar média" (pelo deslocamento daria a alternativa B), registrado na resolução.

17. v1.18.0: Acafe, Vestibular de Medicina Inverno 2021 a Inverno 2026 (10 provas), 70
    questões (Q29–Q35 de cada uma), com a mesma exceção de fonte (prova com gabarito e
    justificativas da Acafe) e gabaritos `oficial`. Decisões do Lucas: a prova fica marcada só
    com o ano, e "Verão"/"Inverno" é descritivo (campo `edicao`, que entra no id, na pasta e
    na `fase`); as questões da Verão 2026 foram renomeadas (`acafe-2026-qNN` →
    `acafe-2026-verao-qNN`). Ficaram de fora Verão 2023 Q37, Verão 2025 Q39 e Inverno 2025 Q36.
    Verão 2021 não entrou (ver pendências). Erros da banca registrados nas resoluções, com o
    gabarito oficial mantido: Verão 2022 Q33 (o certo é 450 Hz; a banca errou a subtração),
    Inverno 2022 Q31 (resultado em cal, alternativas em J), Inverno 2022 Q32 (a banca trocou as
    pressões; o certo é ≈ 12,4 cm³), Verão 2025 Q33 (sem converter J em cal; o certo é 125 mg).
    Verão 2022 Q32: o formulário traz cos 30° desenhado como raiz de 3/2.
18. v1.19.0: Acafe Verão 2021, Q29–Q35. A prova com justificativas imprime a alternativa
    correta logo após o enunciado e as demais depois da justificativa; o Lucas decidiu manter
    a ordem do PDF. Gabaritos: 29A, 30A, 31C, 32D, 33C, 34B, 35B. Q30 usa o formulário da
    prova, que traz o valor da Lua como "g_T = 1,6 m/s²" (transcrito literalmente).
19. v2.0.0: modelo de dados com questões **discursivas** (`tipo`, `respostas`) e
    Einstein (Vunesp) 2023–2027: Prova I Q36–Q40 e Prova II Q03 de cada ano, 30 questões.
    Decisões do Lucas: o ano fica limpo e Prova I/Prova II é descritivo (campo `edicao`,
    como na Acafe); "o modelo da Unicamp 2021 A/B foi um erro" e não se repete; o banco
    deve aceitar discursivas desde já, porque virão outras provas discursivas; gabaritos
    serão conferidos depois por ele. Caderno da Prova II em coluna única, uma questão por
    página: `--layout largura-total`. Os PDFs do Einstein têm hífens discricionários
    (U+00AD) no meio de palavras e subscritos colados (`Qint`, `Pinicial`): divergências
    registradas em `revisao.divergenciasAceitas`.

## Pendências

- **Gabaritos Einstein 2023–2027**: todos `resolucao-propria`, inclusive as respostas das
  discursivas. Prova I: 2023 36A 37C 38E 39B 40C; 2024 36D 37E 38C 39A 40B; 2025 36A 37B
  38B 39E 40D; 2026 36C 37A 38D 39D 40B; 2027 36A 37C 38B 39E 40D. Prova II Q03: 2023
  1,25 m/s² e –1,5 × 10⁵ J; 26 s e 120 m · 2024 1,5 s; 10 kg e 60 N · 2025 4,08 s; 12,8 m
  · 2026 45 J; 20 m · 2027 10 m/s; 20 m/s. Conferir com atenção 2025 Q38 (leitura de β e δ
  na figura) e 2027 Q38 (A × B: depende de admitir que o índice da casca é maior que o do ar).
- **Unicamp 2021 A/B no modelo antigo**: o Lucas considera um erro marcar a prova no ano
  ("2021 A"). Migrar para `edicao` (ano 2021 limpo) exige renomear 16 questões e figuras e
  regravar no app; fazer só com pedido dele.

- **Acafe Inverno 2025 Q32**: a "Imagem ilustrativa da experiência de Joule" não está no PDF; a legenda foi mantida, sem figura. Q35: a distinção entre IV e V (condução × convecção) é discutível; anotada na resolução.
- **Acafe Inverno 2026 Q29**: as alternativas são frações desenhadas como equação; transcritas em linha, com parênteses.

- **ENEM 2016**: falta o caderno do **1º dia** (Ciências Humanas e Ciências da Natureza):
  o arquivo enviado (`enem-2016-caderno.pdf`) é o do 2º dia, Linguagens e Matemática, e
  não foi registrado. Antes de transcrever, mostrar a lista de questões ao Lucas.
- **Gabaritos oficiais do ENEM 2017–2025**: trocar `gabaritoFonte` para `oficial` com os
  PDFs do INEP (`20xx_GB_impresso_D2_CD5.pdf`) quando puderem ser baixados ou o Lucas
  enviar (registrar com `--tipo gabarito`). Prioridade: 2020 e 2017, que não foram
  conferidos com nenhum gabarito do caderno amarelo. 2025 hoje é `oficial` lido em
  transcrição jornalística.
- **ENEM 2025 Q115 e 2024 Q102 anuladas**: como na Fuvest 2022 Q54, decidir se ficam no app.

- **Ativar o GitHub Pages** (v1.4.0): Settings › Pages › Source: GitHub Actions. O plano
  gratuito exige repositório público; com repositório privado, só com GitHub Pro. O site
  fica aberto na internet (ver a nota de direitos autorais em `docs/ROADMAP-SAAS.md`).

- **Gabaritos oficiais Fuvest**: só 2025 foi conferido no PDF oficial (fuvest.br, lido na
  web; o arquivo não pôde ser baixado para `fontes/`). 2020–2024 e 2026 estão como
  `resolucao-propria` (2024 e 2026 conferem com o gabarito divulgado). Quando o Lucas
  enviar os PDFs de gabarito, registrar com `--tipo gabarito` e trocar para `oficial`.
  Conferir com atenção 2020 Q78 (trajetória 4) e 2023 Q70. Fuvest 2016–2019 também está
  toda como `resolucao-propria` (conferir 2016 Q35 e 2017 Q58, que dependem de leitura de
  figura).
- **Gabarito oficial Fuvest 2027**: conferir as 12 respostas (28C, 35A, 36B, 37A, 41C, 42C,
  54C, 56B, 62C, 73D, 74B, 75C) quando a Fuvest divulgar e trocar para `oficial`.
- **Gabaritos Unesp 2017–2020**: `resolucao-propria` (gabaritos oficiais não encontrados em
  texto). Conferir com atenção 2017 Q83 (sentido de giro do motor; resolvida pela figura e
  pela coerência entre as alternativas) e 2019 Q64 (afirmação II, pressão osmótica = dgΔh).
- **Gabaritos Unesp**: 2023 está como `resolucao-propria` sem conferência externa (o
  gabarito oficial só foi achado em imagem). 2022 confere com o Estratégia e 2026 com o
  gabarito divulgado pela Quero Bolsa; trocar para `oficial` quando houver o PDF da Vunesp.
  Conferir com atenção 2024 Q82 (sentido do campo do solenoide, lido na figura) e 2025 Q81
  (leitura das cotas 1,8 m e 0,6 m), que dependem de figura.
- **Fuvest 2022 Q54 anulada**: mantida no banco com o gabarito pretendido (B) e aviso.
  Decidir se fica no app ou sai.
- **Critério "Química com Física forte"**: na Fuvest o Lucas mandou incluir. Decidir se
  vale também para as Unicamp que ficaram de fora (2020 Q45–Q48, 2021 B Q33, 2027 Q25).

- **Gabarito oficial 2027**: as 7 questões estão com `resolucao-propria`. Gabaritos da
  resolução: 8A, 9B, 10D, 11C, 12B, 13B, 14D.
- **Manifesto incompleto**: até a v1.0.0 o `data/fontes/manifesto.json` não era versionado
  (o `.gitignore` o ignorava). No repositório ele agora só tem a Unicamp 2027; as entradas
  2016–2026 estão no manifesto local do Lucas e precisam ser mescladas.

- **Gabaritos oficiais 2016–2025**: os atuais vêm das resoluções (`gabaritoFonte:
  resolucao-propria`). Quando o Lucas enviar os PDFs de gabarito da Comvest, conferir e
  trocar para `oficial`. Os de 2026 conferem com a Prova Comentada.
- **Revisar resolução da 2017 Q59** (supõe que a perna equilibra mg·sen 30°).
- **2017 Q38**: o gabarito considera energia ∝ v² (fator 1/4); está registrada a
  observação sobre v³ (fator 1/8). Decidir se vale manter a observação.
- **Em aberto, "por enquanto, não"**: questões de Química com Física forte (Unicamp 2020
  Q45–Q48, 2021 B Q33). Não incluir sem novo pedido.
- **Release v1.0.0 no GitHub**: o envio de tags falhou pela sessão; criar pela aba
  Releases do site, se desejado. O `CHANGELOG.md` registra a versão.
- **Próximas provas**: o `painel` mostra 21 tópicos sem questão (v1.7.0) (mais pobre:
  Eletromagnetismo). Candidatas naturais: Fuvest anteriores a 2020 (mesmo formato),
  Unicamp anteriores a 2016, depois Unesp e ENEM (exigem ajustar o segmentador).

## Limites conhecidos do formato atual

- As figuras no app vêm do armazenamento do artefato; `data/figuras-publicadas.json` mapeia
  cada PNG ao id no artefato.
- O artefato aceita até 25 mil documentos e lotes de 50 escritas.
- A lista selecionada no app fica salva só no navegador.
