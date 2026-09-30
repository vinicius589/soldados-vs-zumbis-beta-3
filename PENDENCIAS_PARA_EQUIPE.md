# Beta 4 — passagem de trabalho para a equipe

Esta entrega reúne o jogo executável, o histórico de versões, artes de
produção, ferramentas, referências e testes. O autor pediu que os colegas
finalizem o projeto a partir dela. Os pontos abaixo continuam abertos e não
devem ser apresentados como aprovados apenas porque os testes passam.

## Prioridade visual

1. Revisar, jogando nos três cenários, as animações de disparo, recarga,
   dano, mordida, corrida e habilidades. O autor rejeitou diversas prévias
   anteriores por corte e avanço de quadro, mudança de tamanho e efeitos
   soltos do corpo ou da arma. A última revisão de água, fogo e gás foi
   integrada e testada, mas ainda não recebeu aprovação visual explícita.
2. Confirmar que toda arma usa seu próprio recuo, carregamento, clarão e
   munição. A SWAT é o exemplo aprovado de alinhamento na boca do cano,
   não um modelo para as outras armas. A relação entre cada arma e seus
   perfis está em `visual_layout.py` e
   `REFERENCIAS_VISUAIS_ARMAS_BETA4.md`.
3. Conferir em movimento a escala fixa e o pivô dos pés de soldados,
   zumbis comuns, subchefes, chefes, barco e submarino. A aparência deve
   continuar no estilo 16 bits com gestos críveis e leitura clara.
4. Conferir se a água nasce da mangueira do Bombeiro, a chama nasce do
   bocal do Incinerador e a granada do Antipraga abre o gás no impacto,
   sempre dentro da própria pista. Chefes são a exceção permitida para
   alcançar mais de uma faixa.

As prévias ficam em `visual_qa_beta4/entrega/`. Os comandos
`python tools/export_interaction_sync_qa.py` e
`python tools/export_gameplay_roster_qa.py` geram material novo a partir do
renderizador do jogo.

## Jogabilidade e equilíbrio

1. Jogar as 12 ondas em cada mapa nos modos Fácil, Médio e Difícil. Os
   testes verificam regras e inicialização, não demonstram que pessoas
   consigam concluir todas as 36 combinações de mapa e dificuldade.
2. Observar se o começo do Médio e do Difícil permite montar uma defesa
   coerente e se as ondas finais ainda exigem decisões. Registrar a onda,
   mapa, dificuldade, cartas usadas e quantidade de suprimentos ao reportar
   qualquer desequilíbrio.
3. Conferir se counters especiais são compreensíveis pela arte e pela
   interface. O jogador precisa perceber por que um inimigo é resistente e
   qual carta abre a defesa.
4. Revalidar a disponibilidade automática das oito cartas regionais ao
   entrar no mapa, sem tela de seleção pré-partida. A documentação de
   propostas antigas ainda menciona cartas descartadas ou números de
   suprimentos anteriores; `main.py` e `README.md` descrevem a produção vigente.

## Perguntas a decidir com o autor

- Quais animações da última revisão de água, fogo e gás estão aprovadas e
  quais precisam de uma nova direção visual? Anexar vídeo ou GIF do momento
  exato ajuda mais do que avaliar apenas uma folha estática.
- O equilíbrio das 12 ondas deve ser afinado primeiro por mapa ou em uma
  curva única para as três regiões?
- A próxima etapa acrescentará cartas e inimigos ou priorizará polimento,
  acessibilidade e apresentação? Evitar incorporar propostas antigas sem
  aprovação específica.
- Quando a equipe considerar a Beta 4 concluída, qual critério de aceite
  define a saída da Beta e a versão final do jogo?

## Como contribuir

1. Instale Python 3 e as dependências de `requirements.txt`.
2. Clone o repositório e execute `git lfs pull` para obter as artes e o áudio.
3. Rode `python -m unittest discover -s . -p "test_*.py"` e
   `python smoke_test.py` antes de alterar a lógica.
4. Abra `executar.bat` e faça a revisão visual em uma janela real. O modo
   padrão utiliza CPU/RAM; PyOpenGL é apenas uma opção.
5. Descreva no PR a região, a carta ou ameaça, o estado de animação, o quadro
   e um antes/depois capturado dentro do jogo. Não substitua os assets
   aprovados de suprimento sem necessidade.

Os históricos em `historico/` são registros. A implementação em andamento
fica na raiz do repositório. Áudios derivados de fontes CC0 e seus links
estão descritos em `assets/audio_sources_cc0/SOURCES.md`.
