# Processo de release

## Versionamento

Usamos SemVer: `MAJOR.MINOR.PATCH`.

- `MAJOR`: quebra de compatibilidade ou mudança grande de campanha/save.
- `MINOR`: funcionalidade nova compatível.
- `PATCH`: correção compatível.

Tags oficiais têm o formato `vX.Y.Z`. Tags históricas antigas podem manter o
nome original, mas não crie novas tags sem o prefixo `v`.

## Checklist antes da release

- [ ] `pyproject.toml` está com a versão correta.
- [ ] `docs/CHANGELOG.md` possui uma seção para a versão.
- [ ] `README.md` descreve a instalação e a forma de jogar.
- [ ] `python -m pytest` passa.
- [ ] `python -m ruff check src tests` passa.
- [ ] `python -m compileall -q src run.py` passa.
- [ ] Smoke test headless passa.
- [ ] O jogo foi aberto em uma máquina com janela SDL.
- [ ] As três regiões foram verificadas visualmente.
- [ ] Nenhum save, cache, segredo ou arquivo temporário está no diff.
- [ ] O executável e os assets do pacote foram conferidos.

## Fluxo de publicação

1. Parta de `develop` e crie `release/X.Y.Z`.
2. Atualize versão, changelog, README e notas em
   `docs/releases/notes-vX.Y.Z.md`.
3. Rode toda a validação local e abra PR para `main`.
4. Após aprovação e CI verde, faça **Squash and merge**.
5. Atualize `develop` com o mesmo conteúdo por PR.
6. Crie a tag anotada na revisão que entrou em `main`:

   ```bash
   git switch main
   git pull --ff-only origin main
   git tag -a vX.Y.Z -m "release: vX.Y.Z"
   git push origin vX.Y.Z
   ```

7. Crie o GitHub Release a partir da tag e anexe somente pacotes reproduzíveis.
8. Confirme que o link aparece no README e que o changelog foi publicado.

## Release de correção urgente

Para um defeito crítico em produção, crie `hotfix/X.Y.Z` a partir de `main`,
faça a menor alteração possível, abra PR para `main`, publique a tag e depois
replique a correção em `develop`.

## O que não fazer

- Não reescrever `main` com force push.
- Não mover a tag de uma versão já publicada.
- Não publicar arquivo sem checksum ou sem instrução de instalação.
- Não misturar experimentos de arte com o pacote jogável.
