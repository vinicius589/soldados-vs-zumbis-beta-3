# Histórico preservado do jogo

O autor definiu **Beta** como um marco com adições de conteúdo ou funções e
**Alfa** como uma rodada de correções. Por isso os nomes abaixo descrevem a
função de cada snapshot na sequência, mesmo quando a pasta original tinha
outro nome técnico. Nenhuma cópia foi rebatizada dentro da sua própria pasta.

| Ordem | Marco | Cópia neste repositório | Origem local preservada | Motivo da classificação |
|---:|---|---|---|---|
| 1 | Alfa inicial | `01-alfa-inicial/` | `soldados-vs-zumbis/` | Base jogável inicial antes das adições de menu. |
| 2 | Beta 1 | `02-beta-1/` | `soldados-vs-zumbis-v6-menu/` | Adição da abertura e do fluxo de menu. |
| 3 | Alfa pós-Beta 1 | `03-alfa-pos-beta-1/` | `_verificacao-v7-1/` | Correções de arena, terreno e inicialização. |
| 4 | Beta 2 | `04-beta-2/` | `Soldados-vs-Zumbis-v7.4-Promocao-e-Equilibrio-Distribuicao/` | Marco de adições de promoção e seleção regional. |
| 5 | Alfa pós-Beta 2 | `05-alfa-pos-beta-2/` | `Soldados-vs-Zumbis-v7.5-Minas-e-Equilibrio-Distribuicao/` | Correções de minas e equilíbrio. |
| 6 | Beta 3 | `06-beta-3/` | `Soldados-vs-Zumbis-Beta-3-Distribuicao/` | Distribuição identificada no próprio código como Beta 3. |
| 7 | Alfa pós-Beta 3 | `07-alfa-pos-beta-3/` | `Soldados_vs_Zumbis_Beta4-Revisao-Final-2026-09-22/` | Snapshot de revisão e correção anterior ao fechamento desta entrega. O nome original traz “Beta4”, mas sua função nesta linha é a rodada Alfa. |
| 8 | Beta 4 | [raiz do repositório](../README.md) | `soldados-vs-zumbis-v7-reconstrucao/` em 30/09/2026 | Integração atual de três regiões, elenco regional, campanha de 12 ondas, áudio e animações. |

Cada pasta histórica mantém os arquivos de código, arte, áudio e documentação
que estavam na origem. Foram omitidos apenas cache Python, progresso pessoal
`campanha_v7.json`, a pasta de verificação `QA_ANIMACOES` do sétimo snapshot e
metadados `.git`; nenhum desses itens é necessário para executar o marco.
Essas pastas são registros independentes. Execute `executar.bat` dentro da
versão desejada, sem misturar arquivos entre elas.

O código da Beta 4 na raiz descende também do histórico de commits Git da
antiga Beta 3. As pastas acima preservam os snapshots anteriores que não
existiam como commits separados nesse repositório. O inventário original e
seus critérios estão em
[`HISTORICO_DE_VERSOES_PRE_GITHUB.md`](../HISTORICO_DE_VERSOES_PRE_GITHUB.md).

## Conferência das cópias

Antes de publicar, foram conferidos a existência das sete origens, a
quantidade de arquivos copiados e a ausência dos caches e do salvamento
pessoal. `python smoke_test.py` terminou com sucesso **em cada uma das sete
pastas** neste computador em 30/09/2026; isso confirma inicialização e
checagens básicas, não uma partida visual ou campanha inteira em cada versão.
O estado atual da Beta 4 é validado separadamente pelos testes e pela
inicialização descritos no README da raiz. Não se deve interpretar esses
smokes como garantia de compatibilidade com todo computador dos colegas.
