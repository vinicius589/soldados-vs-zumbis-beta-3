# Histórico de Versões e Sprints

Este documento rastreia a evolução do projeto "Soldados vs Zumbis", desde suas concepções iniciais até o estado atual, ajudando a manter um registro histórico (Git) de todo o percurso de desenvolvimento.

## Linha do Tempo (Roadmap de Evolução)

O projeto passou/passará pelas seguintes iterações formativas:

1. **Beta 1 (Atual)**: Fundação do projeto, estrutura básica de classes (Base, Game, Input), implementação inicial de Pygame. Foco em execução livre de erros e layout primário.
2. **Alfa Inicial**: Primeiras tentativas de adicionar mecânicas de contenção, disparo e instanciamento dinâmico de tropas.
3. **Beta 2**: Expansão do tabuleiro, criação de múltiplos cenários rudimentares e refatoração de código espaguete para módulos menores.
4. **Alfa (Intermediária)**: Introdução do sistema de ondas e correções críticas no balanceamento.
5. **Beta 3**: Revisão dos zumbis (adicionando chefes e subchefes) e refinamento do sistema de recursos e suprimentos.
6. **Alfa (Polimento)**: Correções de layout, ajustes em caixas de colisão e primeiros testes com animações baseadas em estado.
7. **Beta 4**: Versão final consolidada, contendo o gerenciador de animação de estados (AnimationManager), sprites separados por região (Cidade, Deserto, Cachoeira) e renderização baseada em OpenGL (OpenGLPresenter).

---

## Sprints do Novo Projeto (Beta 1 -> Integração)

Para organizar o trabalho nesta fase atual de reestruturação do Beta 1, dividimos as tarefas nas seguintes *Sprints*:

### Sprint 1: Estruturação e Versionamento (Concluída)
- [x] Separar código-fonte em `src/`.
- [x] Isolar documentações em `docs/`.
- [x] Criar `README.md` com diretrizes do projeto e Conventional Commits.
- [x] Criar arquivo `.gitignore`.
- [x] Preparar scripts de compilação sem dependência direta do PyCharm ou Python pré-instalado.

### Sprint 2: Empacotamento e Acessibilidade (Concluída)
- [x] Criar `GERAR_EXECUTAVEL.bat` via PyInstaller para tornar o jogo um `.exe` autônomo (não requer Python no computador do jogador).
- [x] Criar script de união com o repositório oficial (`SINCRONIZAR_GITHUB.bat`).

### Sprint 3: Compatibilização de Código (A fazer)
- [ ] Revisar variáveis e classes do `core/base.py` para facilitar o *merge* futuro com a lógica avançada da Beta 4.
- [ ] Documentar o funcionamento interno do laço de eventos no `game.py`.
- [ ] Preparar a migração das constantes mágicas do `game.py` (ex: `WIDTH`, `HEIGHT`, `LANES`) para um arquivo de configurações isolado.

### Sprint 4: Merge com a Beta 4 (A fazer via GitHub)
- [ ] Rodar o `SINCRONIZAR_GITHUB.bat`.
- [ ] Aprovar o Pull Request da branch `historico/beta-1` e preservar as tags históricas no repositório `vinicius589/soldados-vs-zumbis-beta-4`.
