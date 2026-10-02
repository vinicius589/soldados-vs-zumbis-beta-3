# Soldados vs Zumbis — Beta 4

[![CI](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/actions/workflows/ci.yml/badge.svg)](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/actions/workflows/ci.yml)
[![Licença MIT](https://img.shields.io/badge/licença-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg)](https://www.python.org/)
[![Pygame CE](https://img.shields.io/badge/Pygame--CE-2.5.8-8CBF3F.svg)](https://pyga.me/)

**Soldados vs Zumbis** é um tower defense 2D original, desenvolvido em Python,
Pygame-CE e PyOpenGL. Defenda três regiões, escolha seu esquadrão e sobreviva
a 12 ondas de infectados.

> **Estado atual:** Beta 4 jogável. A branch `main` representa a versão estável;
> alterações novas entram por Pull Request e passam pela CI antes do merge.

## Jogue agora no Windows

1. Abra a página de [Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases).
2. Baixe o pacote da versão desejada, ou clone o repositório completo.
3. Extraia todos os arquivos para uma única pasta.
4. Execute `JOGAR AGORA.exe`.

Não mova o executável para fora da pasta: os cenários, sprites e áudios são
recursos externos necessários ao jogo. O executável não é assinado digitalmente;
use somente arquivos baixados deste repositório oficial.

## Execute pelo código-fonte

### Requisitos

- Python **3.12 ou superior**;
- Windows, Linux ou macOS;
- suporte a uma janela SDL para jogar. Os testes também funcionam em modo
  headless, sem monitor e sem áudio.

### Instalação recomendada

```bash
git clone https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git
cd soldados-vs-zumbis-beta-4
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/macOS
source .venv/bin/activate
```

Instale o pacote e as ferramentas de desenvolvimento:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Inicie o jogo:

```bash
python run.py
# ou, depois da instalação editável:
soldados-vs-zumbis
```

## Comandos de desenvolvimento

```bash
python -m pytest
python -m ruff check src tests
python -m compileall -q src run.py
```

Para o smoke test sem janela e sem áudio, usado no CI:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python run.py
```

O último comando mantém o loop interativo aberto; encerre-o com `Ctrl+C` após
confirmar que não houve erro. No PowerShell, defina as duas variáveis de
ambiente com `$env:NOME="dummy"` antes de executar.

## O jogo

| Elemento | Valor |
| --- | --- |
| Gênero | Tower defense por faixas |
| Resolução | 1280 × 720 |
| FPS alvo | 60 |
| Tabuleiro | 4 faixas × 9 colunas |
| Campanha | 12 ondas por região |
| Regiões | `city`, `desert`, `beach` |
| Progressão | comuns, subchefes e chefes em ciclos de 4 ondas |

- **Nova York (`city`)**: combate urbano e distâncias curtas.
- **Deserto do Egito (`desert`)**: ruínas, areia e defesa de longo alcance.
- **Cachoeira de Minas Gerais (`beach`)**: água, vegetação e ameaças submersas.

## Estrutura do repositório

```text
.
├── src/                    # Código do jogo
│   ├── engine/             # Animação, paths e compositor OpenGL
│   └── game/               # Regras, elencos e layout visual
├── assets/                 # Cenários, sprites, efeitos e música versionados
├── tools/                  # Pipeline de produção e QA de arte
├── tests/                  # Testes automatizados
├── docs/                   # Arquitetura, contribuição e releases
├── scripts/                # Verificações auxiliares do repositório
├── .github/                # CI, templates, CODEOWNERS e dependabot
├── run.py                  # Entrada simples para executar o jogo
├── pyproject.toml          # Metadados, dependências e configuração Python
└── JOGAR AGORA.exe         # Build Windows distribuída na raiz histórica
```

O código de runtime nunca deve depender de caminhos absolutos. Use
`src.engine.asset_paths.game_root()` para localizar recursos. Arquivos gerados,
saves, ambientes virtuais, caches e arte temporária não entram no Git.

## Fluxo de branches

- `main`: estável e pronta para release.
- `develop`: integração da próxima versão.
- `release/x.y.z`: congelamento e preparação de release.
- `hotfix/x.y.z`: correção urgente derivada de `main`.
- `feat/*`, `fix/*`, `art/*`, `docs/*`, `test/*`, `refactor/*`, `chore/*` e
  `perf/*`: branches curtas de trabalho.

Nenhuma alteração deve ser feita diretamente em `main` ou `develop`.
Consulte [`docs/BRANCHING.md`](docs/BRANCHING.md) e
[`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md).

## Releases e versões

O projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/) e
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Tags oficiais têm
o formato `vX.Y.Z`; versões históricas antigas preservam seus nomes originais.
O checklist completo está em
[`docs/releases/RELEASE_PROCESS.md`](docs/releases/RELEASE_PROCESS.md).

## Documentação

| Documento | Finalidade |
| --- | --- |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Camadas e fluxo do runtime |
| [`docs/BRANCHING.md`](docs/BRANCHING.md) | Branches, PRs e proteção |
| [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) | Mensagens de commit |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | Ambiente e contribuição |
| [`docs/releases/RELEASE_PROCESS.md`](docs/releases/RELEASE_PROCESS.md) | Releases e tags |
| [`docs/REPOSITORY_GUIDE.md`](docs/REPOSITORY_GUIDE.md) | Organização das pastas |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Histórico de mudanças |

## Licença

Distribuído sob a licença [MIT](LICENSE). © 2026 Equipe Soldados vs Zumbis.
