# 🌿 Estratégia de Branches e Proteção de Código

Este projeto usa **[Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)** adaptado a um time acadêmico: cinco ramos nomeados, ramos de apoio descartáveis e **Pull Requests obrigatórios**.

---

## 1. Ramos permanentes

| Ramo | Origem | Aceita PR de | Protegido |
| --- | --- | --- | --- |
| `main` | — | apenas `develop` e `hotfix/*` | ✅ **Sim** |
| `develop` | `main` | `feat/*` · `fix/*` · `art/*` · `docs/*` · `test/*` · `refactor/*` | ✅ **Sim** |
| `release/x.y.z` | `develop` | correções pontuais | ✅ **Sim** |
| `hotfix/x.y.z` | `main` | correção urgente | ✅ **Sim** |

**Regra de ouro:** ninguém escreve código direto em `main` nem em `develop`. Toda alteração entra por Pull Request.

> O branch `develop` nasce de `main` com o histórico intacto. Ramos históricos (`historico/*`) são **somente leitura** e nunca recebem push.

---

## 2. Ramos de apoio (descartáveis)

Prefixos **obrigatórios**, sempre derivados de `develop`:

| Prefixo | Para quê |
| --- | --- |
| `feat/` | Nova funcionalidade visível ao jogador |
| `fix/` | Correção de defeito |
| `art/` | Assets visuais ou sonoros |
| `docs/` | Só documentação |
| `test/` | Criação ou correção de testes |
| `refactor/` | Reestruturação sem mudar comportamento |
| `perf/` | Ganho de desempenho |
| `chore/` | Build, dependências, tooling |

**Formato:** `<prefixo>/<descricao-curta-em-kebab-case>`

```bash
git switch develop
git pull origin develop
git switch -c feat/onda-13-mini-boss
```

✅ `feat/onda-13-mini-boss` · `fix/sprite-rastejador-cortado` · `art/deserto-incinerador-v2`
❌ `feature1` · `novo-codigo` · `Joao-Task-3` · `Feat/Onda 13`

> Use apenas `a-z`, `0-9` e `-`. Sem acentos, espaços, maiúsculas nem `_`.

---

## 3. Ciclo de vida

```
                     release/4.1.0
                    ┌──────────────┐
                    │              ▼
  main ──●──────────●───(tag v4.1.0)──────────────►  estável, sempre publicável
                    ▲              ▲
                    │              │
  develop ──●───────●──────────────┴───────●──►  integração, sempre testável
                    ▲                       ▲
        ┌───────────┴──────────┐   ┌────────┴─────────┐
        │                      │   │                  │
   feat/onda-13          art/incinerador  docs/readme  hotfix/4.0.1
   (ramo de apoio)                                         │
                                                           └─► nasce de main
```

**Passo a passo de uma feature:**

```bash
# 1. Atualize e crie o ramo
git switch develop && git pull origin develop
git switch -c feat/nome-da-feature

# 2. Trabalhe em commits pequenos e Conventional Commits
git add -p
git commit -m "feat(area): descricao imperativa"

# 3. Mantenha sincronizado com develop
git fetch origin
git rebase origin/develop

# 4. Publique e abra o PR para develop
git push -u origin feat/nome-da-feature

# 5. Após aprovação e checks verdes → Squash & Merge
# 6. Delete o ramo (botão "Delete branch" no GitHub)
```

---

## 4. Branch Protection Rules

Configure em **GitHub → Settings → Branches → Add branch protection rule**.
Aplique o padrão abaixo. *Em repositórios privados, algumas opções exigem GitHub Pro/Team.*

### 4.1 `main` — produção

| Regra | Valor | Por quê |
| --- | --- | --- |
| **Require a pull request before merging** | ✅ | Nada entra sem revisão |
| **Required approving reviews** | **1** | No mínimo 1 aprovação |
| **Dismiss stale pull request approvals** | ✅ | Aprovação expira se houver novo commit |
| **Require review from Code Owners** | ✅ | Dono do módulo revisa o módulo |
| **Require status checks to pass** | ✅ | CI verde é obrigatório |
| **Required status checks** | `pytest`, `lint` | Testes e estilo |
| **Require branches to be up to date** | ✅ | Sem merge surpresa |
| **Require conversation resolution** | ✅ | Nenhuma discussão pendente |
| **Require signed commits** | opcional | Recomendado se o time tiver GPG |
| **Include administrators** | ✅ | A regra vale também para admins |
| **Restrict force pushes** | ✅ Ninguém | Histórico nunca é reescrito |
| **Restrict deletions** | ✅ Ninguém | `main` nunca é apagado |
| **Do not allow bypassing** | ✅ | Ninguém pula a regra |

### 4.2 `develop` — integração

Mesmo padrão, com três diferenças:

| Regra | Valor |
| --- | --- |
| Required approving reviews | **1** |
| Allow force pushes | ✅ **Apenas para admins** (facilita *rebase* na semana) |
| Required status checks | ✅ `pytest` |

### 4.3 `release/*` e `hotfix/*`

| Regra | Valor |
| --- | --- |
| Require a pull request before merging | ✅ |
| Required approving reviews | **1** |
| Required status checks | ✅ `pytest`, `lint` |
| Restrict deletions | ✅ |

### 4.4 Ramos históricos (`historico/*`)

| Regra | Valor |
| --- | --- |
| **Lock branch** | ✅ Totalmente bloqueado |
| Restrict force pushes | ✅ Ninguém |
| Restrict deletions | ✅ Ninguém |

> `historico/beta-1` preserva a primeira versão jogável. É **somente leitura** por decisão.

### 4.5 Ramos de apoio (`feat/*`, `fix/*`, `art/*`, …)

Sem proteção — são descartáveis. Exclusão automática ao fechar o PR.

---

### 4.6 Resumo rápido (copiar e colar)

```
main:
  ☑ Require a pull request before merging
      ☑ Require approvals: 1
      ☑ Dismiss stale pull request approvals
      ☑ Require review from Code Owners
  ☑ Require status checks to pass → pytest, lint
      ☑ Require branches to be up to date
  ☑ Require conversation resolution
  ☑ Include administrators
  ☐ Allow force pushes
  ☐ Allow deletions

develop:
  ☑ Require a pull request before merging
      ☑ Require approvals: 1
      ☑ Dismiss stale pull request approvals
  ☑ Require status checks to pass → pytest
  ☑ Require conversation resolution
  ☑ Include administrators
  ☑ Allow force pushes → Administrators only
  ☐ Allow deletions
```

---

## 5. Proteções complementares no GitHub

Além das regras de branch, configure em **Settings**:

| Onde | Configuração | Valor |
| --- | --- | --- |
| **General** | *Pull Requests* → **Allow squash merging** | ✅ |
| **General** | *Pull Requests* → **Allow merge commits** | ❌ |
| **General** | *Pull Requests* → **Automatically delete head branches** | ✅ |
| **General** | *Vulnerability alerts* → **Dependabot alerts** | ✅ |
| **Actions** | *General* → *Workflow permissions* → **Read repository contents** | ✅ |
| **Tags** | Proteger `v*` contra exclusão | ✅ |

---

## 6. Checklist de revisão de código

O revisor confere, **nesta ordem**:

- [ ] O PR resolve o que a Issue descreve — **nada além disso** (*scope creep*).
- [ ] Mensagens seguem a [Convenção de Commits](COMMIT_CONVENTION.md).
- [ ] `pytest` passa e **novos comportamentos têm teste**.
- [ ] O jogo **roda de ponta a ponta** no mapa afetado.
- [ ] Nenhum asset temporário, `.venv` ou `__pycache__` foi versionado.
- [ ] Nenhum segredo ou credencial foi versionado.
- [ ] Arte seguiu o fluxo `art/` e passou por QA visual.
- [ ] `docs/` atualizado se a mudança alterou comportamento.
- [ ] Nomes e comentários seguem o vocabulário do projeto (ver [CONTRIBUTING](CONTRIBUTING.md)).

---

## 7. Commits de merge

- **Preferido:** *Squash and merge* — um commit limpo no `develop`.
- **Aceitável:** *Rebase and merge* — para PRs com histórico já limpo.
- **Proibido:** *Create a merge commit* com mensagem padrão.

---

## 8. Resolução de conflitos

```bash
git switch feat/minha-branch
git fetch origin
git rebase origin/develop
# resolve os conflitos nos arquivos
git add <arquivo>
git rebase --continue
git push --force-with-lease
```

- Nunca use `git push --force` puro — sempre `--force-with-lease`.
- Nunca resolva conflito editando o arquivo direto em `develop`.
- Conflito em binário (PNG/WAV): **o do seu ramo vence**; refaça o QA visual.
