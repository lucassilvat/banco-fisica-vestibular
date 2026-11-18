# Descritivo do projeto no Claude

Texto para colar nas instruções do Project "Banco de questões" no claude.ai (o Claude não consegue
alterá-las sozinho). Quando mudar algo aqui, colar de novo lá.

---

Este projeto é o Banco de Física Vestibular do Lucas, professor de Física do ensino médio: banco de questões de Física de vestibulares brasileiros (Unicamp, Fuvest, Unesp, ENEM, Einstein, Acafe e outros; número atual de questões e versão no CHANGELOG.md). Há um app web de consulta por tópico, com resolução comentada, resolução animada e exportação de listas em .docx.

Onde as coisas estão:

- App de revisão (artefato privado, com banco de dados e figuras próprios): https://claude.ai/artifact/R1zq9bpSmPV41kyzg12dxA. Só o Lucas acessa. Mostra todas as resoluções animadas, e ele marca cada uma como Não revisada, Comentada ou Aprovada, com comentário (coleção "revisoes"). Para alterar o app ou gravar questões, use esse artefato pelo link; nunca crie um novo.
- Site dos alunos (GitHub Pages, em beta): gerado a partir do ramo main. Só leva as resoluções animadas aprovadas pelo Lucas.
- Código e dados versionados: repositório GitHub lucassilvat/banco-fisica-vestibular (ramo main). O conhecimento deste projeto é uma cópia sincronizada dele.
- PDFs oficiais das provas: com o Lucas; ele envia na conversa quando for importar.

Ao começar uma conversa de trabalho, leia HISTORICO-E-PENDENCIAS.md (decisões já tomadas e o que falta) e siga CLAUDE.md, WORKFLOW.md e CRITERIOS.md. Para resoluções animadas, leia também ANIMACOES.md (formato) e DIRETRIZES-ANIMACOES.md (o que o Lucas pediu nas revisões).

Regras que valem em todas as conversas:

- Enunciado literal. Reproduzir exatamente o caderno de questões aplicado da banca: sem frase de abertura, sem reescrever, sem trocar verbo de comando, sem mencionar figura que o original não menciona. Prova comentada ou material de cursinho não é fonte de enunciado. Se o texto literal não puder ser obtido, avisar antes de entregar.
- Antes de transcrever uma prova nova, mostrar ao Lucas a lista de questões de Física escolhidas.
- Toda questão leva resolução comentada passo a passo, gabarito com a origem indicada (oficial ou resolução própria) e tópicos da taxonomia.json.
- Nada é gravado no app sem verificação: cada palavra e cada número do enunciado conferidos contra o PDF oficial, número de [[figura N]] igual ao de figuras, tópicos válidos. `python -m pipeline verificar` sem erros.
- Mudanças sobem ao GitHub num ramo novo, com pull request para o main. O merge é sempre do Lucas: nunca enviar direto ao main nem fazer o merge.
- Ao terminar uma importação, entregar os JSON das questões novas e as figuras (para o repositório), atualizar o CHANGELOG.md e informar o que mudou.
- Listas de exercícios: .docx editável, questões primeiro e gabarito com resoluções ao final.

Resoluções animadas:

- São um adicional à resolução comentada, feitas prova a prova quando o Lucas pede, no formato "aula": cadência de professor na lousa (frases e equações uma a uma, negrito onde importa), cancelamentos e "passar para o outro lado" animados, mais de um método em abas quando houver, cada método terminando com o gabarito e "Fim da resolução.".
- Resolver como o aluno resolveria na prova: enunciar a fórmula antes de usar, sinais corretos (sem módulo), não supor o que a questão não garante e, quando os valores forem difíceis, mostrar também a versão aproximada com o mesmo gabarito.
- Desenho fiel à figura da prova e à física, legível no app (linhas importantes grossas e escuras, cores coerentes com o texto). Simulação só quando agrega; contas simples só na lousa. Forças com letra maiúscula e notação vetorial. Sem perguntas ao aluno e sem simuladores em que ele muda valores.
- Fluxo: publicar no app de revisão, o Lucas comenta, corrigir os comentários e republicar. Resolução já Aprovada não se altera direto: sugerir ao Lucas e esperar o aval (a alteração volta para a revisão dele). Antes do pull request, importar as revisões; só as aprovadas vão para o site dos alunos.

Responda em português do Brasil.
