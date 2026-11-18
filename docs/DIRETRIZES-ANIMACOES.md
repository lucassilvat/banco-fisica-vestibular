# Diretrizes das resoluções animadas (revisões do Lucas)

Este documento reúne o que o Lucas pediu nos comentários de revisão das resoluções animadas
(Unesp 2019 a 2026, nov/2026). Vale para toda resolução animada nova ou refeita. Ler antes de
produzir um lote; conferir cada item antes de publicar no app para revisão. O formato técnico
(blocos, `\marca`, `cancelar`, `mover`, cenas) está em `docs/ANIMACOES.md`.

## 1. Como o aluno resolveria

- **Resolver do jeito que o aluno vai fazer na prova**, seguindo o caminho que a questão sugere.
  Ex.: meia-vida térmica (Unesp 2019 Q80): meia-vida por meia-vida, com a temperatura inicial e a
  final de cada uma, e depois Q = m c ΔT.
- **Não assumir o que o problema não garante.** Um gráfico ou desenho que sugere uma informação
  não dada (ex.: meias-vidas de mesma duração) induz o aluno ao erro; nesse caso, sem gráfico.
- **Enunciar a fórmula antes de usá-la**: primeiro E<sub>p</sub> = m g h, depois os valores
  (2019 Q85); primeiro T<sub>y</sub> = T sen θ, mostrando o ângulo e o seno (ou cosseno) no
  triângulo retângulo, depois a conta (2022 Q77). Na segunda vez, o mesmo raciocínio mais rápido.
- **Ordem lógica das grandezas**: calcular primeiro o que se conserva e usá-lo depois. Ex.: na
  refração de ondas, a frequência primeiro; mantendo a frequência, o novo comprimento de onda
  (2022 Q81).
- **Áreas sob gráficos por partes simples**: figuras abaixo da curva (dois triângulos, não um
  triângulo "acima" que se subtrai) e cada parte com a sua conta antes da soma (2020 Q76).
- **Contas longas em etapas que o aluno reconhece**: em misturas, tomar 1 000 g, isolar o volume
  na fórmula da densidade antes de calcular, somar os volumes ("a cada 1 kg temos esse volume") e
  fechar com regra de três (2020 Q87).
- **Versão aproximada quando os valores são "feios"**: depois da resolução completa, refazer com
  valores arredondados (ex.: densidades 20 e 6; 528/170 ≈ 3), dizendo que na hora da prova
  aproximar é boa estratégia, e mostrar que o gabarito é o mesmo (2020 Q87, 2019 Q73).

## 2. Álgebra na lousa

- **Sinais corretos, sem módulo**: o aluno precisa se apropriar das fórmulas com o sinal. Ex.:
  imagem real, portanto invertida: p' > 0 e A < 0; A = −p'/p, os sinais de menos se cancelam
  (2020 Q80). Calor cedido: Q negativo, e o texto explica o sinal.
- **Demonstrar visualmente as passagens**: cancelamentos animados e termos que "passam para o
  outro lado" (ex.: de A = −p'/p até p = 5 000 p'). Na passagem de logaritmos, a **regra do
  tombamento** animada (2021 Q81): muitos alunos têm dificuldade com ela.
- **Cancelamento só onde é algébrico** (fator comum, termo que aparece dos dois lados). Igualar
  membros de uma cadeia de igualdades não é cancelar.
- **O traço do cancelamento fica sobre o termo**, em qualquer tamanho de tela (2025 Q79 e Q81).
- **Entidades HTML** (`&lt;`) nunca: usar os caracteres `<`, `>` e `&` (2021 Q78, enunciado).

## 3. Fidelidade do desenho

- **O desenho segue a figura da prova** e a física: nada fundido ou omitido que mude o sentido
  (o baço estava junto com os intestinos; na prova, baço e intestinos estão em paralelo e em série
  com o fígado: 2019 Q66).
- **Conferir o gabarito e as grandezas contra a figura** antes de animar: na 2019 Q81, α é o
  ângulo de incidência na interface A/B (na camada A), e o gabarito gravado estava errado.
- **Escala real quando o desenho é cinemático**: o ponto mais alto da parábola tem de estar no
  vértice, e o vetor velocidade no ponto que ele descreve, mesmo que a figura da prova não esteja
  em escala (2022 Q78). Órbitas desenhadas contêm os planetas (2020 Q77).
- **Óptica**: imagem virtual do lado virtual do espelho, com o tamanho dado pelo aumento
  (2026 Q79). Raios pelo centro óptico; objeto e imagem com setas opostas quando a imagem é
  invertida (2020 Q80). Marcar o **olho** do observador quando importa a orientação, e **todas
  as distâncias** envolvidas na formação das imagens (2021 Q80).
- **Ângulos bem marcados**: setor entre as duas retas certas, rótulo legível (2023 Q80).
- **Correntes e campos com sentido certo em todo o ciclo**, inclusive quando a animação recomeça
  (2026 Q82).
- **Representar o fenômeno com o modelo que o professor usaria**: a Terra com um ímã de barra
  dentro (S magnético perto do N geográfico), linhas de campo grandes, saindo do N e entrando no S,
  com setas de orientação. Nada de vetores pequenos ou confusos (2019 Q82).

## 4. Movimento nas simulações

- **Colisões**: os corpos se movem juntos depois do contato (quando é o caso), com a velocidade
  indicada perto do corpo. Mostrar duas "fotografias": imediatamente antes e imediatamente depois
  da colisão. A animação serve para o aluno entender o que aconteceu (2023 Q78).
- **Aceleração uniforme de verdade**: o corpo ganha velocidade uniformemente enquanto anda
  (2023 Q87).
- Simulação só quando agrega; contas simples ficam só na lousa.

## 5. Legibilidade

- **Linhas importantes em preto (#111111) e grossas**, com bom contraste também no tema escuro
  (2021 Q76: segmentos do triângulo).
- **Cor citada no texto = cor do desenho**: se o texto fala da seta vermelha, a seta é vermelha
  (2021 Q80).
- Desenho grande o suficiente para ver os detalhes no painel do app; rótulos sem sobreposição.

## 6. Processo

- Uma resolução já **Aprovada** não se altera direto: sugerir a mudança ao Lucas e esperar o aval;
  depois ela volta à revisão (vale também para mudanças no player que alterem o que ela mostra).
- Ao corrigir um comentário, conferir a captura de **todas** as telas da questão.
- Merge sempre pelo Lucas (`CLAUDE.md`).
