# Material bruto e explicação dos arquivos

Esta pasta tira da página inicial os textos de planejamento, prompts,
relatórios e anotações que se acumularam durante o desenvolvimento. Os
originais estão em [`textos/`](textos/). Eles foram preservados para pesquisa
e para os colegas entenderem o contexto; **não são instruções automáticas
para mudar o jogo**. Alguns descrevem estados antigos ou ideias não
implementadas. Para jogar ou programar, comece por
[`../betas/beta-4/README.md`](../betas/beta-4/README.md).

Os renders, capturas, caches e protótipos não publicados que já estavam na
pasta de trabalho foram **movidos, não apagados**, para `rascunhos-locais/`.
Essa subpasta é ignorada pelo Git: existe apenas neste computador, não no
GitHub. Se uma dessas imagens precisar entrar no jogo, ela deve ser revisada
e copiada conscientemente para a Beta correspondente.

## Como ler estes textos

| Grupo | Arquivos | O que explicam | Cuidado |
|---|---|---|---|
| Elenco, fichas e história | `BETA4_ELENCO*`, `BETA4_FICHAS*`, `BETA4_HISTORIA*`, `ELENCO_FUTURO*` | Personagens, armas, papéis e ideias narrativas discutidos em etapas diferentes. | Uma ficha pode falar de carta ainda não lançada. Compare com o elenco ativo no README da Beta 4. |
| Ondas e inimigos | `BETA4_12_ONDAS*`, `AMEACAS_BETA4_PROPOSTA*` | Propostas de progressão, subchefes, chefes e counters. | Números de vida, suprimento e seleção de cartas podem ter sido alterados depois. |
| Arte e animação | `PROMPT*`, `REFERENCIAS_VISUAIS_ARMAS*`, `ANIMATION_REVIEW*`, `ASSET_MANIFEST*` | Intenção visual, origem de sprites, armas, efeitos e problemas observados. | Um prompt não é uma sprite aprovada; conferir a animação dentro do jogo. |
| Revisão e passagem | `REVISAO_PRE_GITHUB*`, `BETA4_PEDIDOS*`, `BETA4_LEIA-ME*`, `PENDENCIAS_PARA_EQUIPE*` | O que estava sendo pedido, testado ou ainda faltava revisar. | “Passou no teste” não significa aprovação visual ou campanha vencida. |
| Organização e decisões | `HISTORICO_DE_VERSOES*`, `PROXIMAS_DECISOES*` | Origem da classificação dos marcos e perguntas propostas para a equipe. | O histórico é anterior à organização atual; perguntas não são decisões tomadas pelo autor. |

O `requirements.txt` antigo da raiz foi guardado em `textos/` só como
registro. **Para instalar uma versão, use o `requirements.txt` que está
dentro da pasta daquela Alfa ou Beta.**

## Onde está o conteúdo que realmente roda

Na Beta 4, os arquivos principais estão todos em
[`../betas/beta-4/`](../betas/beta-4/):

- `main.py` controla menu, cartas, posicionamento, inimigos e partida.
- `campaign_content.py` descreve conteúdo da campanha e progressão.
- `animation2d.py`, `beta4_production_animations.py` e
  `beta4_runtime_animations.py` preparam e trocam quadros de animação.
- `beta4_scenario_runtime.py` cuida de efeitos e elementos dos cenários.
- `assets/v7/` traz cenários e arte herdada ainda usada; `assets/beta4_producao/`
  traz as folhas de personagens e efeitos da Beta 4; `assets/audio_beta4/`
  traz os sons usados pelo jogo.
- `test_*.py` e `smoke_test.py` verificam regras e inicialização. Os arquivos
  `tools/` e os protótipos são apoio de produção dentro da própria Beta 4,
  não um quinto jogo separado.

As Alfas e as Betas antigas mantêm seus próprios arquivos equivalentes.
Uma pasta não deve importar imagens ou código da outra.

## O que vale hoje e o que é apenas registro

A produção atual usa **quatro faixas, oito cartas automáticas por mapa e
12 ondas**. Textos antigos podem mencionar 15 ondas, evolução N1/N2/N3,
seleção de três cartas ou cartas retiradas: isso explica uma fase passada,
não muda a Beta 4. Se houver conflito, confira o código e o README de
`betas/beta-4/` e leve a divergência ao autor antes de implementar algo.

As perguntas futuras em `PROXIMAS_DECISOES.md` são propostas para conversa;
os problemas ainda conhecidos estão em `PENDENCIAS_PARA_EQUIPE.md`. Nenhum
dos dois é uma autorização para acrescentar personagens ou mudar as regras
sem nova decisão.
