# Changelog

Todas as mudanças notáveis do projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [4.0.2] — 2026-10-02

### Adicionado
- README refeito com instalação, comandos, estrutura e releases.
- Guia de organização de pastas em `docs/REPOSITORY_GUIDE.md`.
- Processo de release, tags e pacotes em `docs/releases/`.
- `CODEOWNERS`, Dependabot e configuração de templates do GitHub.
- CI com checks `ruff`, `pytest` e `package-smoke`.
- Workflow de publicação automática para tags SemVer.
- Verificador de higiene em `scripts/verify_repository.py`.

### Alterado
- Fluxo de branches e contribuição alinhado à proteção real do GitHub.
- Projeto atualizado para a versão `4.0.2`.

## [4.0.1] — 2026-10-02

### Adicionado
- Workflow de CI (`.github/workflows/ci.yml`) com os jobs `ruff` e `pytest`
- Suite de testes (`tests/`) cobrindo layout, conteudo e balanceamento
- Guia de branches e regras de protecao de ramo (`docs/BRANCHING.md`)
- Hook de validacao de mensagens de commit (`.githooks/commit-msg`)

### Corrigido
- Nomes dos checks de CI no guia de branches (`ruff` e `pytest`, antes `lint`)

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
