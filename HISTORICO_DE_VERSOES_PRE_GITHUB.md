# Inventário histórico antes da publicação

> Este inventário foi escrito antes da entrega. A localização atual das
> cópias preservadas está em `historico/README.md`; a Beta 4 atual está na
> raiz do repositório.

Este inventário usa a regra definida pelo autor do jogo:

- **Alfa**: etapa centrada em correção, estabilidade, alinhamento, arte ou
  balanceamento de algo que já existia.
- **Beta**: marco aprovado que consolida o estado jogável e passa a receber
  novas funções, personagens ou conteúdo.

Nenhuma pasta foi renomeada e nada foi publicado. Os caminhos abaixo apontam
para os artefatos preservados neste computador.

## Linha histórica reconstruída pelos arquivos

| Ordem | Rótulo histórico | Artefato preservado | Evidência encontrada |
|---:|---|---|---|
| 1 | Alfa inicial | `soldados-vs-zumbis` | Primeiro projeto jogável datado de 03/09; campanha, economia, chefes e cartas já existem, ainda sem o pacote posterior de abertura/menu. |
| 2 | Beta 1 | `soldados-vs-zumbis-v6-menu` | Marco seguinte do mesmo jogo; acrescenta abertura, carregamento e arquivos táticos, uma adição de produto sobre a base anterior. |
| 3 | Alfa pós-Beta 1 | `_verificacao-v7-1` | O próprio README chama a versão de “correção v7.1”: corrige arenas, terrenos e crash de projéteis. |
| 4 | Beta 2 | `Soldados-vs-Zumbis-v7.4-Promocao-e-Equilibrio-Distribuicao` | Consolida a reconstrução e adiciona Nível 2 visível, Sargento de Promoção, escolha das regiões e Núcleo temporário. É a primeira distribuição preservada dessa família com adições completas. |
| 5 | Alfa pós-Beta 2 | `Soldados-vs-Zumbis-v7.5-Minas-e-Equilibrio-Distribuicao` | Revisão de minas e equilíbrio sobre o marco v7.4; representa a rodada de correção anterior às adições v7.6–v7.9. |
| 6 | Beta 3 | `Soldados-vs-Zumbis-Beta-3-Distribuicao` e `Soldados-vs-Zumbis-Beta-3-Final.zip` | Identificação explícita no código (`VERSION = "BETA 3"`), README, manifesto e pacote final. |
| 7 | Alfa pós-Beta 3 | `soldados-vs-zumbis-v7-reconstrucao` e pacotes `Revisao-Pre-GitHub` | Reconstrução e correções sucessivas de cenário, escala, sprites, grid, animação, áudio e curva de dificuldade. É a etapa atualmente em revisão. |
| 8 | Beta 4 | **será congelada somente após a aprovação atual** | Existem distribuições anteriores chamadas Beta 4, mas a versão destinada ao GitHub ainda está sendo corrigida. O snapshot final não será substituído nem publicado antes da aprovação do autor. |

## Pacotes intermediários preservados

As versões v7.3 a v7.9 permanecem como evidência de evolução, sem serem
apagadas nem fingirem ser oito lançamentos independentes:

- v7.3: contenções regionais, HUD, pausa e correção dos chefes;
- v7.4: promoção e progressão visual;
- v7.5: minas e equilíbrio;
- v7.6: mira e unidades costeiras;
- v7.7: modos de dificuldade;
- v7.8: auditoria das cartas, arte regional e reequilíbrio;
- v7.9: regras da água e identidade regional.

## Regra para o futuro GitHub

O repositório deverá guardar cada marco numa tag/pasta própria e manter os
arquivos originais do snapshot. A publicação só acontece depois de o pacote
de revisão atual ser executado e aprovado. Até lá, o repositório remoto não é
alterado.
