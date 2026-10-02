# Branches, Pull Requests e proteção

O repositório usa um Git Flow simples com revisão obrigatória. O objetivo é
manter `main` sempre reproduzível e pronta para download.

## Branches permanentes

| Branch | Função | Base |
| --- | --- | --- |
| `main` | Código estável e releases | — |
| `develop` | Integração da próxima versão | `main` |
| `historico/*` | Material histórico somente leitura | tag/commit histórico |

Branches `release/*` e `hotfix/*` são temporárias e têm ciclo documentado em
[`releases/RELEASE_PROCESS.md`](releases/RELEASE_PROCESS.md).

## Branches de trabalho

Use nomes minúsculos, sem acentos, espaços ou `_`:

```text
feat/<mudanca>       fix/<problema>       art/<asset>
docs/<documento>     test/<cobertura>     refactor/<modulo>
perf/<melhoria>      chore/<ferramenta>
```

Exemplos válidos: `feat/onda-13`, `fix/audio-menu`,
`docs/atualizar-readme`.

## Fluxo normal

```bash
git fetch origin
git switch develop
git pull --ff-only origin develop
git switch -c feat/nome-da-mudanca
# editar e testar
git add <arquivos>
git commit -m "feat(campanha): adicionar nova onda"
git push -u origin feat/nome-da-mudanca
```

Abra o PR para `develop`. O PR deve ter escopo único, testes e descrição
reproduzível. Depois de aprovado e com CI verde, use **Squash and merge** e
apague a branch de trabalho.

## Proteção recomendada no GitHub

Aplique em `main` e `develop`: Pull Request obrigatório; uma aprovação;
descartar aprovações antigas; resolver conversas; branch atualizada; checks
`ruff`, `pytest` e `package-smoke`; bloquear force push e exclusão; e permitir
apenas squash ou fast-forward. Aplique as regras também a administradores quando
essa opção estiver disponível.

Proteja `v*` contra exclusão e mantenha `historico/*` como somente leitura.
Branches de trabalho não precisam de proteção permanente.

## Commits

Use [Conventional Commits](COMMIT_CONVENTION.md). Antes do push:

```bash
git diff --check
python -m pytest
python -m ruff check src tests
git status --short
```

Nunca inclua `.venv`, caches, saves, segredos ou arquivos gerados.
