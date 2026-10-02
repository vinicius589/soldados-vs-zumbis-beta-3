# Soldados vs Zumbis (Beta 1)

Repositório acadêmico do projeto "Soldados vs Zumbis". Este repositório reflete a estrutura da Beta 1, com o projeto organizado para suportar evolução contínua.

## Estrutura de Diretórios

- `src/`: Contém o código-fonte principal do jogo.
- `docs/`: Documentação do projeto, instruções de uso e arquivos de referência de versões passadas.
- `assets/`: Pasta destinada a armazenar recursos futuros como imagens, sprites e efeitos sonoros.

## Executando o Projeto

O jogo requer as dependências indicadas em `requirements.txt` (neste caso, a biblioteca Pygame CE).

```bash
# 1. Crie um ambiente virtual e ative-o (recomendado)
python -m venv .venv
# Ativação no Windows:
.venv\Scripts\activate
# Ativação no Linux/Mac:
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o jogo
python src/main.py
```

## Regras de Versionamento e Contribuição

Para padronização, a equipe utilizará o **Git Flow** simplificado e mensagens baseadas em **Conventional Commits**.

### Fluxo de Branches

- `main`: Branch principal, deve conter código estável e funcional correspondente a versões (releases).
- `develop`: (Opcional) Branch de integração para testar funcionalidades antes da submissão para `main`.
- `feature/*`: Branches dedicadas ao desenvolvimento de novas mecânicas (ex: `feature/adicionar-som`, `feature/menu-principal`).
- `bugfix/*`: Para correção de problemas menores ou falhas.

As contribuições devem ser feitas via *Pull Request* da branch `feature/` para `main` (ou `develop`).

### Conventional Commits

Utilize um dos seguintes prefixos nas suas mensagens de commit:

- `feat:` Inclusão de um novo recurso ou funcionalidade (ex: `feat: adiciona sistema de pontuação`).
- `fix:` Resolução de um erro (ex: `fix: conserta colisão do projetil`).
- `docs:` Modificações exclusivas em arquivos de documentação.
- `style:` Alterações de formatação (espaçamentos, vírgulas faltando) que não mudam a lógica.
- `refactor:` Alteração que não resolve um bug nem adiciona uma feature, mas melhora o código estruturalmente.
- `test:` Adição ou correção de testes.
- `chore:` Atualizações em configurações ou dependências (ex: `.gitignore`, `requirements.txt`).
