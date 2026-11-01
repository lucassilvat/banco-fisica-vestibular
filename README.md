# Banco de Física Vestibular

Banco de questões de Física de vestibulares brasileiros, com enunciados transcritos
literalmente das provas oficiais, resolução comentada, classificação em 151 tópicos e
exportação de listas de exercícios (.docx, abre no Word e no Google Docs).

**Situação atual:** 109 questões da Unicamp, 1ª fase, de 2016 a 2026 (incluindo as duas
provas de 2021), 60 figuras recortadas dos cadernos oficiais. Todas passam na
verificação automática.

## Estrutura

```
app/index.html            app publicado como artefato do Claude (consulta, filtros, lista .docx)
data/questoes/            uma questão por arquivo JSON: a fonte da verdade
data/figuras/             figuras recortadas dos cadernos (PNG, 200 dpi)
data/taxonomia.json       15 áreas, 151 tópicos
data/fontes/manifesto.json  PDFs oficiais usados (com sha256)
data/figuras-publicadas.json figura -> id no armazenamento do app
pipeline/                 ferramentas de importação (python -m pipeline -h)
schemas/                  esquema JSON da questão
docs/                     fluxo de trabalho, critérios, modelo de dados, roadmap SaaS
fontes/   (fora do git)   PDFs oficiais
trabalho/ (fora do git)   arquivos intermediários de cada importação
```

## Começando

```
pip install -r requirements.txt      # e poppler-utils (pdftotext) no sistema
python -m pipeline painel            # cobertura por prova e por tópico
python -m pipeline verificar         # checa todas as questões
```

Para conferir a fidelidade ao texto, coloque os PDFs oficiais em `fontes/` com os nomes
listados em `data/fontes/manifesto.json` (o sha256 garante que é o mesmo arquivo).

## Documentação

- [docs/WORKFLOW.md](docs/WORKFLOW.md): como importar uma prova, etapa por etapa
- [docs/CRITERIOS.md](docs/CRITERIOS.md): fidelidade, convenções de transcrição, o que entra no banco
- [docs/MODELO-DE-DADOS.md](docs/MODELO-DE-DADOS.md): campos da questão e do app
- [docs/ROADMAP-SAAS.md](docs/ROADMAP-SAAS.md): caminho para virar produto, incluindo direitos autorais
- [docs/HISTORICO-E-PENDENCIAS.md](docs/HISTORICO-E-PENDENCIAS.md): decisões tomadas e o que falta
- [CLAUDE.md](CLAUDE.md): regras para o Claude trabalhar neste repositório

## App

`app/index.html` é o código do app publicado como artefato privado no Claude. Para mudar o
app, edite esse arquivo e publique de novo no mesmo artefato. As questões não ficam no
HTML: o app lê do banco do artefato, alimentado pela etapa `publicar`.
