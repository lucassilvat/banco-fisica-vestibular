# Caminho para SaaS

## Onde estamos (fase 0)

- App de página única publicado como artefato no Claude, com banco de documentos e
  armazenamento de figuras próprios do artefato. Uso pessoal, privado.
- Dados versionados neste repositório; publicação por lotes.
- Limites relevantes do formato atual: um único banco por artefato (até 25 mil
  documentos), sem contas de usuário próprias, sem cobrança, listas salvas só no
  navegador de quem usa.

Até umas poucas centenas de questões, a fase 0 é suficiente. O foco agora é **conteúdo**:
cada questão bem transcrita, verificada e com resolução é o ativo que vai para qualquer
versão futura.

## Antes de vender: direitos autorais (bloqueante)

Provas de vestibular são publicadas pelas bancas, mas isso não autoriza automaticamente
o uso comercial. Além do texto das bancas, muitas questões reproduzem material de
terceiros: trechos literários e jornalísticos, fotos, tirinhas, frames de desenho
animado (ex.: Unicamp 2017 Q65, Tom e Jerry). Antes de cobrar por acesso:

1. Consultar um advogado de propriedade intelectual sobre o uso de provas e do material
   de terceiros nelas.
2. Verificar os termos de uso de cada banca (Comvest, Fuvest, Vunesp, INEP).
3. Planejar o produto de forma que o valor esteja no que é seu: resoluções comentadas,
   classificação por tópico, montagem e exportação de listas, estatísticas.
4. Manter no banco a origem de cada questão (campo `fonte`) e a possibilidade de ocultar
   figuras de terceiros sem perder a questão.

Também: LGPD para dados de professores e alunos, e termos de uso e política de
privacidade próprios.

## Fases sugeridas

**Fase 1: backend próprio, uso pessoal ou piloto com colegas.**
Banco relacional (PostgreSQL) com as mesmas entidades de `data/`; armazenamento de
objetos para figuras; API simples; login. Um script de importação lê `data/` e popula o
banco (a etapa `publicar` ganha um segundo destino). O front atual pode ser reaproveitado.

**Fase 2: multiusuário.**
Contas por professor e por escola; listas salvas no servidor; exportação .docx gerada no
servidor; filtros por dificuldade (a classificação de dificuldade que o Lucas já usa pode virar
um campo `dificuldade`); comentários e correções
enviados por usuários, com moderação.

**Fase 3: produto pago.**
Planos, cobrança, limites de uso, painel de escola. Só depois da revisão jurídica.

## Decisões que podem esperar

Escolha de framework, hospedagem e meio de pagamento não precisam ser feitas agora. O que
convém manter desde já: dados separados do app, ids estáveis (`banca-ano-qNN`), origem e
status de cada questão, e verificação automática antes de publicar.
