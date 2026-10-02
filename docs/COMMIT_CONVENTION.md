# Convenção de Commits

Este projeto segue o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/)
para manter um histórico legível e possibilitar geração automática de changelogs.

## Formato

```
<tipo>(escopo opcional): descrição curta

[corpo opcional]

[rodapé(s) opcional(is)]
```

## Tipos Permitidos

| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade para o jogador |
| `fix` | Correção de bug |
| `art` | Mudança em assets visuais ou sonoros |
| `docs` | Alteração apenas em documentação |
| `refactor` | Refatoração sem mudar comportamento externo |
| `test` | Adição ou correção de testes |
| `chore` | Configuração, CI, dependências, build |
| `style` | Formatação de código (sem mudança de lógica) |
| `perf` | Melhoria de performance |

## Escopos Sugeridos

| Escopo | Área |
|--------|------|
| `campanha` | Sistema de ondas e progressão |
| `animacao` | Sistema de animação 2D |
| `render` | OpenGL / compositor |
| `audio` | Efeitos sonoros e música |
| `ui` | Interface do jogador |
| `cidade` | Mapa de Nova York |
| `deserto` | Mapa do Egito |
| `praia` | Mapa da Cachoeira-MG |
| `carta` | Sistema de cartas |
| `boss` | Chefes e subchefes |
| `deps` | Dependências do projeto |
| `ci` | Integração contínua |

## Exemplos

```bash
# Funcionalidade nova
git commit -m "feat(campanha): adicionar onda 13 com mini-boss regional"

# Correção de bug
git commit -m "fix(animacao): corrigir sprite do rastejador cortado na borda"

# Novo asset
git commit -m "art(deserto): nova folha do incinerador v2"

# Documentação
git commit -m "docs(readme): atualizar instruções de instalação"

# Refatoração
git commit -m "refactor(render): extrair shader de vinheta para função separada"

# Mudança que quebra compatibilidade
git commit -m "feat(campanha)!: mudar formato de save para JSON v2

BREAKING CHANGE: saves da Beta 3 não são mais compatíveis."
```

## Regras

1. **Descrição curta** — máximo 72 caracteres, começando com verbo no infinitivo
2. **Corpo** — opcional; explica o *porquê*, não o *o quê*
3. **Escopo** — opcional, mas recomendado para facilitar buscas
4. **Idioma** — português para manter consistência com o projeto
5. **Um commit, uma mudança lógica** — evite commits "resolvi tudo"
