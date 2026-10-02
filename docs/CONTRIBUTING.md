# Contribuindo com Soldados vs Zumbis

Obrigado por querer contribuir! Este documento descreve o fluxo de trabalho
para manter o projeto organizado e facilitar a revisão entre colegas.

## Configuração do Ambiente

```bash
# 1. Clone o repositório
git clone https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git
cd soldados-vs-zumbis-beta-4

# 2. Crie um ambiente virtual
python -m venv .venv

# 3. Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute o jogo
python run.py
```

## Fluxo de Branches

Seguimos um **Git Flow simplificado**:

| Branch | Propósito |
|--------|-----------|
| `main` | Versão estável (releases) |
| `develop` | Integração contínua |
| `feat/<nome>` | Nova funcionalidade |
| `fix/<nome>` | Correção de bug |
| `art/<nome>` | Mudanças em assets (arte, som) |
| `docs/<nome>` | Apenas documentação |

### Criando uma branch

```bash
# Sempre parta de develop
git checkout develop
git pull origin develop
git checkout -b feat/minha-funcionalidade
```

### Abrindo um Pull Request

1. Faça push da sua branch: `git push origin feat/minha-funcionalidade`
2. Abra um PR em GitHub apontando para `develop`
3. Preencha o template do PR
4. Aguarde revisão de pelo menos um colega

## Convenção de Commits

Usamos **Conventional Commits** — veja [`docs/COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md)
para a referência completa.

**Formato:** `<tipo>(escopo): descrição curta`

```
feat(campanha): adicionar onda 13 com mini-boss regional
fix(animacao): corrigir sprite do rastejador cortado na borda
art(deserto): nova folha do incinerador v2
docs(readme): atualizar instruções de instalação
```

## Reportando Bugs

Ao encontrar um defeito:

1. Abra uma Issue usando o template **Bug Report**
2. Informe: **mapa**, **onda**, **unidade** envolvida
3. Se possível, anexe uma captura de tela ou gravação
4. Descreva o comportamento esperado vs. o observado

## Padrões de Código

- **Python 3.12+** com type hints
- Docstrings em português para manter consistência com o projeto
- Nomes de variáveis em inglês para código, português para textos do jogador
- Tempos de animação sempre em **segundos** (nunca contagem de frames)
- `asset_paths.game_root()` para qualquer caminho de recurso

## Estrutura de Diretórios

```
src/engine/   → código reutilizável (animação, render, paths)
src/game/     → lógica específica do jogo
assets/       → recursos visuais e sonoros
tools/        → scripts de pipeline de produção
tests/        → testes automatizados
docs/         → documentação do projeto
```

## Testes

```bash
# Rodar testes (quando disponíveis)
python -m pytest tests/
```

Cobertura de testes é encorajada para lógica de jogo (dano, recarregamento,
seleção de alvo). Módulos visuais são testados manualmente.
