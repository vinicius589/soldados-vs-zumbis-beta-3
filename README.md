# 🎮 Soldados vs Zumbis — Beta 4

> **Projeto acadêmico de programação** — tower defense original em Python, Pygame-CE e PyOpenGL.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pygame-CE 2.5.8](https://img.shields.io/badge/Pygame--CE-2.5.8-8CBF3F?logo=pygame&logoColor=black)](https://pyga.me)
[![PyOpenGL](https://img.shields.io/badge/PyOpenGL-3.1.10-555555?logo=opengl&logoColor=white)](https://pyopengl.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-E5726B.svg)](docs/COMMIT_CONVENTION.md)
[![Git Flow](https://img.shields.io/badge/Git-Flow-FC6D26.svg)](docs/BRANCHING.md)

Defenda **Nova York**, o **Deserto do Egito** e a **Cachoeira de Minas Gerais**. Escolha **8 cartas** por operação, administre suprimentos e detenha os infectados em **12 ondas** — duas comuns, uma de subchefe e uma de chefe, por ciclo.

---

## 📋 Sumário

- [Jogar no Windows](#-jogar-no-windows-1011)
- [Executar pelo código-fonte](#-executar-pelo-código-fonte)
- [Sobre o jogo](#-sobre-o-jogo)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Arquitetura](#-arquitetura)
- [Testes](#-testes)
- [Documentação](#-documentação)
- [Como contribuir](#-como-contribuir)
- [Versões anteriores](#-versões-anteriores)
- [Licença](#-licença)

---

## 🖥️ Jogar no Windows 10/11

1. No botão verde **Code**, escolha **Download ZIP**
2. **Extraia o ZIP inteiro** (7-Zip, WinRAR ou Explorador do Windows)
3. Abra a pasta extraída e execute **`JOGAR AGORA.exe`**

> [!WARNING]
> Não execute o jogo de dentro do ZIP e não mova o `.exe` sozinho — as pastas
> de arte e áudio precisam ficar ao lado dele. O executável não é assinado
> digitalmente; confirme que o arquivo veio deste repositório.

---

## 💻 Executar pelo código-fonte

**Requisitos:** Python 3.12 ou superior.

```bash
# 1. Clone o repositório
git clone https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git
cd soldados-vs-zumbis-beta-4

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o jogo
python run.py
```

> [!NOTE]
> Substitua `python` por `py` no Windows ou `python3` no macOS/Linux, conforme
> necessário. O jogo usa **CPU como caminho padrão**, sem exigir placa de vídeo
> dedicada.

### Dependências

| Pacote | Versão | Papel |
| --- | --- | --- |
| `pygame-ce` | 2.5.8 | Janela, entrada, áudio, blit |
| `PyOpenGL` | 3.1.10 | Compositor e shaders de pós-processamento |
| `numpy` | 2.5.3 | Operações em lote sobre frames |
| `Pillow` | 12.3.0 | Pipeline de sprites e cenários |

---

## 🕹️ Sobre o jogo

| | |
| --- | --- |
| **Gênero** | Tower defense por faixas |
| **Resolução** | 1280 × 720 |
| **FPS alvo** | 60 |
| **Grade** | 4 faixas × 9 colunas (colunas 7–8 não posicionáveis) |
| **Campanha** | 12 ondas por região — 2 comuns + 1 subchefe + 1 chefe, ×3 ciclos |
| **Elenco** | 8 cartas por mapa |
| **Regiões** | `city` · `desert` · `beach` |

### As três regiões

| Chave | Região | Identidade |
| --- | --- | --- |
| `city` | **Nova York** | Avenida urbana, sombras duras, combate curto |
| `desert` | **Deserto do Egito** | Areia, ruínas e pirâmides, longo alcance |
| `beach` | **Cachoeira de Minas Gerais** | Água, vegetação e terreno irregular |

As regiões são desbloqueadas em sequência e cada uma tem seu próprio elenco regional, cenário e animações ambientais.

### Ritmo da campanha

```
ciclo = [ comum ][ comum ][ SUBCHEFE ][ CHEFE ]   →  4 ondas
campanha = ciclo × 3 regiões                        → 12 ondas
```

---

## 📁 Estrutura do projeto

```
soldados-vs-zumbis-beta-4/
├── src/                            # Código-fonte
│   ├── main.py                     #   Game loop, UI, campanha (10k linhas)
│   ├── engine/                     #   Motores reutilizáveis
│   │   ├── animation2d.py          #     Animação 2D, sprites, VFX, câmera
│   │   ├── opengl_presenter.py     #     Compositor OpenGL + shaders
│   │   └── asset_paths.py          #     Resolução de caminhos
│   └── game/                       #   Lógica específica do jogo
│       ├── visual_layout.py        #     Contratos de tamanho/ancoragem
│       ├── beta4_expansion_roster.py
│       ├── beta4_production_animations.py
│       └── beta4_scenario_runtime.py
├── assets/                         # Recursos visuais e sonoros
│   ├── v7/                         #   Sprite sheets e cenários finais
│   ├── beta4_producao/             #   Folhas de produção por personagem
│   └── audio_beta4/                #   Efeitos e música
├── tools/                          # Pipeline de produção (fora do runtime)
│   ├── cenarios/                   #   Preparação e QA de cenários
│   ├── sprites/                    #   Laboratório de animação e chroma
│   └── prototipo_carta/            #   Protótipo visual de cartas
├── tests/                          # Testes automatizados
├── docs/                           # Documentação do projeto
├── .github/
│   ├── pull_request_template.md    #   Template estruturado de PR
│   └── ISSUE_TEMPLATE/             #   Templates de Bug e Feature
├── run.py                          # Ponto de entrada
├── pyproject.toml                  # Metadados, dependências, configs
├── requirements.txt                # Dependências de execução
├── .gitignore                      # O que nunca versionar
├── LICENSE                         # MIT
└── JOGAR AGORA.exe                 # Executável Windows
```

---

## 🏗️ Arquitetura

```
run.py
 └── src/main.py ─────────── game loop, UI, campanha, save
       │
       ├── src/engine/   (genérico — NÃO conhece regras do jogo)
       │     animation2d.py        sprites · clips · VFX · câmera
       │     opengl_presenter.py   framebuffer → textura → shaders
       │     asset_paths.py        raiz do jogo (código vs PyInstaller)
       │
       └── src/game/     (específico — regras e contrato visual)
             visual_layout.py               fonte única de dimensões
             beta4_expansion_roster.py      elenco do Lote 2
             beta4_production_animations.py clips por região
             beta4_scenario_runtime.py      animações ambientais
```

**Fluxo de dados**

```
Assets (PNG/WAV)
   ↓  asset_paths.game_root()
animation2d.SpriteSheet          ← recorta folhas em frames
   ↓
beta4_production_animations      ← monta clips por estado
   ↓
main.py (game loop @ 60 FPS)     ← atualiza lógica
   ↓
opengl_presenter                 ← pós-processamento (cor, contraste, vinheta)
   ↓
Tela do jogador
```

**Princípios**

- `engine/` é **reutilizável** e não referencia conteúdo do jogo.
- `game/` é a **única** fonte de verdade para dimensões e ancoragem — arte e lógica consultam a mesma tabela (`visual_layout.py`).
- Durações de animação são sempre em **segundos**, nunca em contagem de frames.

Detalhes completos em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## 🧪 Testes

```bash
pip install -e ".[dev]"
python -m pytest
```

> Sem `pytest`? `python -m pytest` também roda após `pip install pytest`.

---

## 📚 Documentação

| Documento | Descrição |
| --- | --- |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Diagrama de módulos e fluxo de dados |
| [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) | Regras **estritas** de Conventional Commits |
| [`docs/BRANCHING.md`](docs/BRANCHING.md) | Git Flow, Branch Protection Rules e revisão |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | Ambiente, padrões de código e fluxo de PR |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Histórico de mudanças |

---

## 🤝 Como contribuir

1. Leia o **[Guia de Branching](docs/BRANCHING.md)** e a **[Convenção de Commits](docs/COMMIT_CONVENTION.md)**.
2. Abra uma **[Issue](.github/ISSUE_TEMPLATE/bug_report.md)** antes de codar — Bugs e Features têm templates próprios.
3. Crie sua branch a partir de `develop`:

   ```bash
   git switch develop && git pull
   git switch -c feat/nome-da-feature
   ```

   `feat/` · `fix/` · `art/` · `docs/` · `test/` · `refactor/`

4. Faça commits **Conventional Commits** e abra um **[Pull Request](.github/pull_request_template.md)** para `develop`.
5. Nenhum PR é mesclado sem **1 aprovação** e com os **checks verdes**.

Ao reportar um bug, informe **mapa, onda e unidade** — e, se possível, anexe uma captura de tela.

> Nenhum PR é aceito sem: `pytest` verde · jogo rodando no mapa afetado · `docs/` atualizado quando o comportamento muda.

---

## 📦 Versões anteriores

As versões de referência, Alfas de correção, Betas anteriores e textos de desenvolvimento estão nos [Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases).

- [**Beta 1 — histórico completo**](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/tree/historico/beta-1) — preservada no branch [`historico/beta-1`](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/tree/historico/beta-1), com `src/game.py`, `src/core/` e notas das versões V19/V20.
- [Pacote histórico corrigido](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases/tag/historico-corrigido-2026-09-30) — para consulta; pode exigir Python.

---

## 📄 Licença

Distribuído sob a licença **[MIT](LICENSE)** — © 2026 Equipe Soldados vs Zumbis.
