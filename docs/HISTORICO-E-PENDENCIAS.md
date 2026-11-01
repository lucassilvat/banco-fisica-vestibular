# Histórico de decisões e pendências

Resumo do trabalho feito até a v1.0.0 (outubro de 2026), para quem continuar o projeto
numa conversa nova. As regras permanentes estão em `CLAUDE.md` e `docs/CRITERIOS.md`.

## Onde as coisas estão

| O quê | Onde |
|---|---|
| App publicado (artefato privado, com banco de dados e figuras próprios) | https://claude.ai/artifact/R1zq9bpSmPV41kyzg12dxA |
| Código e dados versionados | github.com/lucassilvat/banco-fisica-vestibular (privado, ramo `main`) |
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

## Pendências

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
- **Próximas provas**: o `painel` mostra 71 tópicos sem questão (mais pobres:
  Eletromagnetismo, Física moderna, Ondulatória). Candidatas naturais: Unicamp anteriores
  a 2016 (mesmo formato) e depois Fuvest, Unesp, ENEM (exigem ajustar o segmentador na
  primeira prova de cada banca).

## Limites conhecidos do formato atual

- As figuras no app vêm do armazenamento do artefato; `data/figuras-publicadas.json` mapeia
  cada PNG ao id no artefato.
- O artefato aceita até 25 mil documentos e lotes de 50 escritas.
- A lista selecionada no app fica salva só no navegador.
