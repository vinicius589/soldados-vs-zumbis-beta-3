# 🎮 Soldados vs Zumbis — Beta 4

> **Projeto acadêmico de programação** — Tower defense original em Python/Pygame

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.8-green?logo=python)](https://pyga.me)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um jogo de defesa por faixas: escolha tropas, administre suprimentos e detenha
os infectados em **Nova York**, no **Deserto do Egito** e na **Cachoeira de
Minas Gerais**. Cada mapa tem oito cartas e uma campanha de 12 ondas (duas
comuns, uma de subchefe e uma de chefe, por ciclo).

---

## 📋 Sumário

- [Jogar no Windows](#-jogar-no-windows-1011)
- [Executar pelo Código-Fonte](#-executar-pelo-código-fonte)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Como Contribuir](#-como-contribuir)
- [Versões Anteriores](#-versões-anteriores)
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

## 💻 Executar pelo Código-Fonte

**Requisitos:** Python 3.12 ou superior

```bash
# Clone o repositório
git clone https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git
cd soldados-vs-zumbis-beta-4

# Crie e ative um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute o jogo
python run.py
```

> [!NOTE]
> Substitua `python` por `py` no Windows ou `python3` no macOS/Linux,
> conforme necessário. O jogo usa CPU como caminho padrão, sem exigir
> placa de vídeo dedicada.

---

## 📁 Estrutura do Projeto

```
soldados-vs-zumbis-beta-4/
├── src/                          # Código-fonte
│   ├── main.py                   # Game loop, UI, campanha
│   ├── engine/                   # Motores reutilizáveis
│   │   ├── animation2d.py        #   Animação 2D, sprites, VFX
│   │   ├── opengl_presenter.py   #   Compositor OpenGL + shaders
│   │   └── asset_paths.py        #   Resolução de caminhos
│   └── game/                     # Lógica específica do jogo
│       ├── visual_layout.py      #   Contratos de tamanho/ancoragem
│       ├── beta4_expansion_roster.py
│       ├── beta4_production_animations.py
│       └── beta4_scenario_runtime.py
├── assets/                       # Recursos visuais e sonoros
├── tools/                        # Scripts de produção (cenários, sprites)
├── tests/                        # Testes automatizados
├── docs/                         # Documentação do projeto
├── .github/                      # Templates de Issues e PRs
├── run.py                        # Ponto de entrada
├── pyproject.toml                # Configuração Python
├── requirements.txt              # Dependências
└── JOGAR AGORA.exe               # Executável Windows
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Diagrama de módulos e fluxo de dados |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | Como configurar o ambiente e contribuir |
| [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) | Padrão Conventional Commits |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Histórico de mudanças |

---

## 🤝 Como Contribuir

1. Leia o [guia de contribuição](docs/CONTRIBUTING.md)
2. Crie uma branch a partir de `develop` seguindo o padrão:
   - `feat/nome` · `fix/nome` · `art/nome` · `docs/nome`
3. Use [Conventional Commits](docs/COMMIT_CONVENTION.md)
4. Abra um Pull Request para `develop`

Ao reportar bugs, informe: **mapa**, **onda**, **unidade** e, se possível,
anexe uma captura de tela.

---

## 📦 Versões Anteriores

As versões de referência, Alfas de correção, Betas anteriores e textos de
desenvolvimento estão nos [Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases).
O [pacote histórico completo](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases/tag/historico-corrigido-2026-09-30)
é para consulta e pode exigir Python.

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
