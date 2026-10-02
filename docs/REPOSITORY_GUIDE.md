# Guia de organização do repositório

Este documento define onde cada tipo de material deve ficar. A regra principal é
separar **runtime**, **produção**, **testes**, **documentação** e **distribuição**.

## Pastas oficiais

| Pasta | Pode conter | Não deve conter |
| --- | --- | --- |
| `src/` | Código Python importado pelo jogo | PNG temporário, script de exportação, save |
| `src/engine/` | Componentes reutilizáveis | Regras específicas de uma região |
| `src/game/` | Regras, dados e contratos visuais do jogo | Código de ferramenta de arte |
| `assets/` | Arte e áudio necessários ao runtime | Rascunhos, fontes sem crédito, duplicatas |
| `tools/` | Scripts, referências e laboratório de produção | Imports obrigatórios do runtime |
| `tests/` | Testes rápidos, determinísticos e headless | Dependência de monitor ou save pessoal |
| `docs/` | Decisões, arquitetura, contribuição e releases | Código executável do jogo |
| `scripts/` | Checks auxiliares de manutenção | Lógica do gameplay |
| `.github/` | CI, templates, CODEOWNERS e dependabot | Segredos ou arquivos locais |

## Assets

- Assets usados pelo jogo ficam em `assets/` e devem ter nome descritivo.
- Material bruto e intermediário fica fora do Git ou em um release de produção.
- Todo áudio ou imagem de terceiros precisa de crédito em
  `assets/audio_sources_cc0/SOURCES.md` ou documento equivalente.
- Antes de adicionar um arquivo grande, confirme se ele é carregado pelo runtime
  e se não existe uma versão duplicada.

## Arquivos gerados e pessoais

Nunca versionar: `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`,
`*.egg-info/`, saves, logs, dumps, credenciais, exports de QA e arquivos
temporários. O `.gitignore` é a proteção padrão; revise `git status` antes de
cada commit.

## Regra de dependências

- Dependências de execução ficam em `[project].dependencies` no `pyproject.toml`.
- Ferramentas de desenvolvimento ficam em `[project.optional-dependencies].dev`.
- `requirements.txt` é mantido como espelho mínimo das dependências de runtime
  para instalações simples e CI legado.
- Não instale dependências diretamente no código e não versione ambientes.

## Regra de caminhos

Use sempre `game_root()` ou caminhos relativos à raiz do projeto. O jogo deve
funcionar a partir da raiz do repositório, de uma instalação editável e do
executável empacotado.
