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

## Pendências

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
- **Próximas provas**: o `painel` mostra 24 tópicos sem questão (v1.6.0) (mais pobre:
  Eletromagnetismo). Candidatas naturais: Fuvest anteriores a 2020 (mesmo formato),
  Unicamp anteriores a 2016, depois Unesp e ENEM (exigem ajustar o segmentador).

## Limites conhecidos do formato atual

- As figuras no app vêm do armazenamento do artefato; `data/figuras-publicadas.json` mapeia
  cada PNG ao id no artefato.
- O artefato aceita até 25 mil documentos e lotes de 50 escritas.
- A lista selecionada no app fica salva só no navegador.
