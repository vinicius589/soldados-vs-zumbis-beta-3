# Changelog

Todas as mudanças notáveis do projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [4.0.0] — 2026-10-02

### Adicionado
- Estruturação acadêmica do repositório com `src/`, `docs/`, `tools/`, `tests/`
- Documentação de arquitetura (`docs/ARCHITECTURE.md`)
- Guia de contribuição (`docs/CONTRIBUTING.md`)
- Convenção de commits (`docs/COMMIT_CONVENTION.md`)
- Templates de Issues e Pull Request (`.github/`)
- Configuração moderna Python (`pyproject.toml`)
- Script de lançamento `run.py` na raiz
- `.gitignore` expandido para IDEs e ferramentas Python

### Alterado
- Código-fonte movido para `src/engine/` (motores) e `src/game/` (lógica)
- Ferramentas de produção movidas para `tools/`
- Imports atualizados para refletir nova estrutura de pacotes
- `README.md` reformulado para contexto acadêmico
- `asset_paths.py` ajustado para resolver caminhos a partir de `src/engine/`

### Histórico Anterior
- As versões Beta 1–3 e Alfas de correção estão documentadas nos
  [Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-4/releases)
  do repositório original.
