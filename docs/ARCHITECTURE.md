# Arquitetura — Soldados vs Zumbis

## Visão Geral

Soldados vs Zumbis é um tower defense em faixas construído com **Pygame-CE** e
renderizado via **PyOpenGL**. O jogador posiciona tropas em quatro pistas para
deter ondas de infectados em três regiões temáticas: Nova York, Deserto do Egito
e Cachoeira de Minas Gerais.

## Diagrama de Módulos

```
run.py                    ← ponto de entrada
 └── src/main.py          ← game loop, UI, campanha
      ├── src/engine/
      │   ├── animation2d.py        ← sprites, clips, VFX, câmera
      │   ├── opengl_presenter.py   ← compositor OpenGL + shaders
      │   └── asset_paths.py        ← resolução de caminhos de assets
      └── src/game/
          ├── visual_layout.py              ← contratos de tamanho/ancoragem
          ├── beta4_expansion_roster.py     ← elenco de expansão (Lote 2)
          ├── beta4_production_animations.py ← sprite sheets regionais
          └── beta4_scenario_runtime.py     ← animações ambientais
```

## Camadas

### Engine (`src/engine/`)

Código reutilizável que não conhece regras do jogo:

- **`animation2d.py`** — SpriteSheet, AnimationClip, AnimationManager, Entity,
  Camera2D, partículas e VFX. Todas as durações são em segundos (nunca frames).
- **`opengl_presenter.py`** — Envia o framebuffer Pygame para uma textura
  OpenGL e aplica shaders de pós-processamento (cor, contraste, vinheta).
- **`asset_paths.py`** — Resolve a raiz do jogo tanto para execução via código
  quanto para o executável empacotado (PyInstaller).

### Game (`src/game/`)

Lógica específica do jogo:

- **`visual_layout.py`** — Tabela de dimensões e pontos de ancoragem de cada
  personagem. Arte e lógica consultam a mesma fonte.
- **`beta4_expansion_roster.py`** — Registro de soldados e zumbis do Lote 2.
  Uma carta só sai de produção quando receber sprite sheet aprovada.
- **`beta4_production_animations.py`** — Carrega e configura clips de animação
  para os elencos regionais (cidade, deserto, praia).
- **`beta4_scenario_runtime.py`** — Animações ambientais (braseiros, ondas do
  mar, relâmpagos) e contenções de cenário.

### Assets (`assets/`)

| Diretório | Conteúdo |
|-----------|----------|
| `v7/` | Sprite sheets finais e cenários de fundo |
| `beta4_producao/` | Folhas de produção por personagem |
| `audio_beta4/` | Efeitos sonoros e música |
| `audio_sources_cc0/` | Créditos das fontes CC0 |

### Ferramentas (`tools/`)

Scripts de pipeline de produção que **não** fazem parte do runtime:

| Diretório | Origem | Finalidade |
|-----------|--------|------------|
| `cenarios/` | `CENARIOS_BETA4_CONCEITOS/` | Preparação e QA de cenários |
| `sprites/` | `PIXEL_ART_SPRITES_BETA4/` | Laboratório de animações e chroma |
| `prototipo_carta/` | `PROTOTIPO_CARTA_CAMPO/` | Protótipo visual de cartas |

## Fluxo de Dados

```
Assets (PNG/WAV)
    ↓
asset_paths.game_root()  →  resolve caminho raiz
    ↓
animation2d.SpriteSheet  →  recorta folhas em frames
    ↓
beta4_production_animations  →  monta clips por estado
    ↓
main.py (game loop)  →  atualiza lógica a 60 FPS
    ↓
opengl_presenter  →  renderiza framebuffer final com shaders
    ↓
Tela do jogador
```

## Constantes Importantes

- **Resolução:** 1280×720
- **FPS alvo:** 60
- **Grade:** 4 faixas × 9 colunas (colunas 7–8 não posicionáveis)
- **Campanha:** 12 ondas (2 comuns + 1 subchefe + 1 chefe por ciclo × 3)
- **Regiões:** city (Nova York), desert (Egito), beach (Cachoeira-MG)
