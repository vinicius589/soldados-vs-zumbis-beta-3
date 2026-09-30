# Possíveis decisões para a próxima etapa

Esta lista contém **perguntas e propostas**, não funcionalidades aprovadas.
Ela existe para a equipe não transformar uma sugestão antiga em regra do jogo
sem conversar com o autor. O comportamento vigente da Beta 4 está em
[`betas/beta-4/README.md`](betas/beta-4/README.md).

## 1. O que significa concluir a Beta 4?

**Decidir com o autor:** a entrega passa para “jogo final” quando todas as
12 ondas forem vencíveis nos três mapas e dificuldades, ou só depois de
aprovação visual quadro a quadro dos personagens e efeitos? Minha sugestão é
exigir ambos, com vídeos curtos gravados dentro do jogo e registro de cada
combinação de mapa e dificuldade. Nenhum desses critérios foi formalmente
aprovado ainda.

## 2. Qual é a próxima prioridade?

**Opções para escolher:** (a) corrigir animações, origem de efeitos, áudio e
interface existentes; (b) ajustar economia e curva das ondas; (c) ampliar
elenco e ameaças. Pela quantidade de problemas visuais relatados, recomendo
terminar (a) e validar (b) antes de implementar (c), mas isto é apenas uma
prioridade proposta.

## 3. Como o jogador entende os counters?

Alguns inimigos resistem a explosivos ou balas comuns e exigem unidade
específica. **Perguntar:** o jogo deve avisar o counter na carta, na ficha do
inimigo, por um ícone durante a onda ou por uma apresentação antes da missão?
Sugestão: aviso curto na ficha e um feedback claro quando um ataque for
resistido, sem entregar toda a estratégia automaticamente.

## 4. Quão rígida deve ser a separação de faixas?

A regra atual é que uma pista não interfere na outra, com exceção de chefes.
**Perguntar:** os efeitos visuais de explosão podem atravessar a divisória
apenas como decoração, mesmo sem dano, ou também devem ser recortados na
faixa? A escolha afeta a leitura de colisão e as futuras habilidades.

## 5. O que fazer com os marcos históricos?

As Betas 1–3 são executáveis de referência; as Alfas preservam o código dos
ciclos de correção. **Perguntar:** a equipe só consulta essas versões ou
também deve manter compatibilidade delas com Python futuro? Recomendo
mantê-las como arquivos congelados e fazer alterações novas apenas em
`betas/beta-4/`, a menos que o autor peça uma correção retroativa.

## 6. Que evidência acompanha uma mudança de animação?

Sugestão para a equipe: PR com nome de personagem, mapa, estado, quadros
alterados, GIF no cenário, origem do efeito e som sincronizado; testes para
escala, pivô, direção e recorte. Isso facilitaria aprovação do autor sem
apresentar só folhas de sprites, que já esconderam erros em versões passadas.

Questões concretas de qualidade e jogabilidade já observadas estão em
[`PENDENCIAS_PARA_EQUIPE.md`](PENDENCIAS_PARA_EQUIPE.md). Nenhuma proposta
desta página altera o jogo por si só.
