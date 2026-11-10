# Instruções para o Claude neste projeto

Projeto do Lucas (professor de Física do ensino médio): banco de questões de Física de
vestibulares brasileiros, com app web de consulta e exportação de listas.
Responda e escreva documentação em português do Brasil.

## Regras que não se negociam

1. **Enunciado literal.** Reproduzir exatamente o caderno aplicado da banca: sem frase de
   abertura, sem reescrever, sem trocar verbo de comando, sem mencionar figura que o
   original não menciona. Se o texto literal não for obtido, avisar antes de entregar em
   vez de preencher lacunas. Detalhes em `docs/CRITERIOS.md`.
2. **Nunca publicar sem `python -m pipeline verificar` sem erros.** Avisos de fidelidade
   são olhados um a um; os legítimos vão para `revisao.divergenciasAceitas`.
3. **Fonte oficial.** Só PDFs registrados em `data/fontes/manifesto.json`. Prova
   comentada não é fonte de enunciado (só de gabarito, marcado como tal); exceção: Acafe
   (ver `docs/CRITERIOS.md`).
4. **Resolução comentada passo a passo** em toda questão revisada.
5. Na dúvida se uma questão é de Física, mostrar a lista ao Lucas antes de transcrever.

## Fluxo

Antes de começar, leia `docs/HISTORICO-E-PENDENCIAS.md` (estado atual, links do app e do
repositório, pendências). Siga `docs/WORKFLOW.md` (etapas 1–9). Comandos: `python -m pipeline -h`.
Para ler uma questão, use as imagens de `trabalho/<prova>/imagens/`; o texto extraído do
PDF é só rascunho (fórmulas e frações saem embaralhadas).

## Mapa do projeto

- `data/questoes/` fonte da verdade (um JSON por questão); `data/figuras/` recortes PNG
- `data/taxonomia.json` tópicos; `data/fontes/manifesto.json` PDFs oficiais
- `pipeline/` ferramentas (segmentar, triagem, renderizar, rascunho, figuras, verificar, publicar, painel)
- `app/index.html` código do app publicado como artefato
- `fontes/` e `trabalho/` ficam fora do git
