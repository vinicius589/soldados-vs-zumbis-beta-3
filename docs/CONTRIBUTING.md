# Como contribuir

Obrigado por contribuir com Soldados vs Zumbis. Este projeto prioriza mudanças
pequenas, testes reproduzíveis e histórico de Git fácil de revisar.

## Ambiente

```bash
git clone https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git
cd soldados-vs-zumbis-beta-4
python -m venv .venv
# ative o ambiente conforme seu sistema
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Antes de programar

1. Procure uma Issue existente ou abra uma nova.
2. Defina o comportamento esperado e os critérios de aceite.
3. Parta de `develop`, nunca de uma branch de trabalho antiga.
4. Leia [`docs/REPOSITORY_GUIDE.md`](REPOSITORY_GUIDE.md) ao adicionar assets,
   ferramentas ou documentação.

## Qualidade obrigatória

```bash
python -m pytest
python -m ruff check src tests
python -m compileall -q src run.py
git diff --check
```

Mudança de lógica precisa de teste. Mudança visual precisa de verificação em
1280×720 e, quando possível, uma captura antes/depois no PR.

## Código e assets

- Python 3.12+, type hints e docstrings em português.
- Durações de animação em segundos.
- Caminhos de assets por `game_root()`.
- Arte e áudio de terceiros com crédito.
- Sem segredos, saves, caches ou arquivos temporários no Git.

## Pull Request

O PR deve explicar o problema, a solução, como testar e o impacto no jogo.
Marque a categoria correta, atualize o changelog quando aplicável e aguarde os
checks `ruff`, `pytest` e `package-smoke`.
