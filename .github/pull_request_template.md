<!-- Leia docs/CONTRIBUTING.md e docs/BRANCHING.md antes de abrir o PR. -->

## Objetivo

<!-- Qual problema este PR resolve? -->

## Tipo de mudança

- [ ] `feat` — funcionalidade
- [ ] `fix` — correção
- [ ] `art` — arte ou áudio
- [ ] `refactor` — reestruturação
- [ ] `test` — testes
- [ ] `docs` — documentação
- [ ] `chore` — build, dependências ou configuração

## Escopo afetado

- [ ] Cidade
- [ ] Deserto
- [ ] Cachoeira de Minas Gerais
- [ ] Campanha / ondas
- [ ] Cartas / unidades
- [ ] Engine / renderização
- [ ] Áudio
- [ ] Ferramentas / assets
- [ ] Documentação

## Como validar

```bash
python -m pytest
python -m ruff check src tests
python -m compileall -q src run.py
python scripts/verify_repository.py
```

Descreva também a verificação manual realizada no jogo, quando aplicável.

## Checklist

- [ ] O PR tem escopo único e título em Conventional Commits.
- [ ] Testes novos foram adicionados quando necessário.
- [ ] CI local passa sem erros.
- [ ] Não inclui `.venv`, caches, saves, logs ou segredos.
- [ ] Assets têm origem/crédito e foram revisados.
- [ ] README, changelog ou docs foram atualizados quando necessário.
- [ ] Testei as regiões afetadas em 1280×720.

## Issue relacionada

<!-- `Closes #123`, `Fixes #123` ou `Refs #123`. -->
