# Alfa após Beta 1 — arenas e estabilidade

Correções registradas no `README.md` original da reconstrução v7.1:

- Cidade e Praia passaram a usar arenas em que os pontos de movimento ficam
  sobre asfalto, areia ou água, não sobre céu, prédios ou paredões.
- Foi corrigida a falha na criação de efeitos de morteiro, fogo ou ácido que
  podia encerrar a partida.

Esta pasta também representa uma reconstrução visual separada, não apenas um
pequeno patch em cima dos arquivos da Beta 1. Por isso a comparação de
código deve considerar a mudança de base e não assumir que cada diferença é
uma correção de bug.

`python smoke_test.py` passou em 30/09/2026. O marco de adições seguinte
está em [`../../betas/beta-2/`](../../betas/beta-2/).
