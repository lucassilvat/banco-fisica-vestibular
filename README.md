# Banco de Física Vestibular

Banco de questões de Física de vestibulares brasileiros, com enunciados transcritos
literalmente das provas oficiais, resolução comentada, classificação em 151 tópicos e
exportação de listas de exercícios (.docx, abre no Word e no Google Docs).

**Situação atual (v2.4.0):** 608 questões: 116 da Unicamp (1ª fase, 2016 a 2027, incluindo
as duas provas de 2021), 149 da Fuvest (1ª fase, 2016 a 2027), 94 da Unesp (1ª fase,
2016 a 2026), 135 do ENEM (2017 a 2025), 84 da Acafe (Medicina, Verão e Inverno, 2021 a
2026) e 30 do Einstein (2023 a 2027: Prova I objetiva e Prova II discursiva), com figuras
recortadas dos cadernos oficiais. Desde a v2.0.0 o banco aceita questões discursivas. Desde a v2.1.0, frações e equações podem ser escritas em LaTeX (docs/CRITERIOS.md).
Todas passam na verificação automática.

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

`app/index.html` é o código do app. O mesmo arquivo roda em dois lugares:

- **Artefato privado no Claude**: lê as questões do banco do artefato (etapa `publicar`).
  Para mudar o app, edite o arquivo e publique de novo no mesmo artefato.
- **Site estático (GitHub Pages)**: `python -m pipeline site` gera a pasta `site/` com o app,
  `questoes.json` e as figuras. Fora do Claude, o app lê esses arquivos e baixa a lista
  .docx direto pelo navegador. O workflow `.github/workflows/pages.yml` gera e publica o
  site a cada envio ao ramo `main`.

Teste local do site: `python -m pipeline site && python -m http.server -d site`, e abra
http://localhost:8000.

### Ativar o GitHub Pages (uma vez)

1. Em **Settings › Pages › Build and deployment › Source**, escolha **GitHub Actions**.
2. Envie algo ao `main` (ou rode o workflow em **Actions › Publicar site › Run workflow**).
3. O endereço aparece em Settings › Pages (algo como `https://<usuário>.github.io/banco-fisica-vestibular/`).

O GitHub Pages só está disponível para repositórios **públicos** no plano gratuito; em
repositório privado exige plano pago (GitHub Pro ou superior). Em qualquer caso, **o site
publicado fica aberto na internet** para quem tiver o link.
