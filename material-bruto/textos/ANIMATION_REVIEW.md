# Laboratório de animação — etapa de aprovação

Esta etapa serve para avaliar movimentos antes de qualquer integração no jogo.
O laboratório não importa `main.py`, não altera campanha, salvamento,
balanceamento, tela de carregamento nem menu principal.

## Como abrir

No Windows, dê dois cliques em `testar_animacoes.bat`.

Também é possível abrir pelo terminal, dentro desta pasta:

```powershell
python animation_lab.py
```

## Protótipos incluídos

1. Irradiado Civil da cidade: andar e morder.
2. Múmia Operária do deserto: andar.
3. Afogado Costeiro da praia: andar.
4. Mutante Nadador do mar: nadar.

Cada protótipo usa oito quadros recortados de uma folha de sprites. A troca dos
quadros é calculada por `dt`: reduzir ou aumentar o FPS do computador não muda a
duração lógica da animação.

## Controles

| Tecla | Função |
|---|---|
| `1`, `2`, `3`, `4` | Escolher o protótipo |
| `Tab` | Ir ao próximo protótipo |
| `Q` | Trocar a ação disponível, como andar/morder |
| `Espaço` | Pausar ou continuar |
| `←` / `→` | Voltar/avançar exatamente um quadro quando pausado |
| `-` / `+` | Reduzir/aumentar a velocidade da animação |
| `R` | Reiniciar o ciclo e a posição |
| `F` | Mostrar/esconder a linha de contato com o chão |
| `B` | Alternar entre cenário e fundo quadriculado de inspeção |
| `A` | Marcar a animação atual como **APROVADA** |
| `X` | Marcar a animação atual como **AJUSTAR** |
| `C` | Limpar a avaliação da animação atual |
| `S` | Salvar uma captura da tela |
| `Esc` | Fechar |

As avaliações ficam gravadas em `animation_review.json`. Uma ação tem sua
própria avaliação: por exemplo, é possível aprovar `andar` e pedir ajuste em
`morder` para o mesmo zumbi.

## O que observar durante a aprovação

- Os pés, nadadeiras ou parte inferior do corpo permanecem apoiados na linha do
  terreno sem flutuar.
- O volume e a escala do personagem não pulam entre os quadros.
- Pernas, braços, tronco e cabeça realmente mudam de pose; o movimento não é
  somente uma imagem deslizando.
- A mordida tem preparação, ataque, contato e recuperação.
- O ciclo volta do último para o primeiro quadro sem um salto visual evidente.
- A leitura continua boa nas velocidades de 6, 10 e 14 quadros por segundo.

## Módulo genérico

O arquivo `animation2d.py` pode ser importado por qualquer projeto Pygame. Ele
contém `SpriteSheet`, `AnimationClip`, `AnimationManager`, `Entity`, `Camera2D`,
`Particle`, `OneShotVFX`, `VFXManager` e `apply_color_overlay`.

Exemplo mínimo:

```python
import pygame

from animation2d import AnimationClip, AnimationManager, SpriteSheet

sheet = SpriteSheet.from_file("personagem.png")
frames = sheet.slice_equal(frame_count=8)

animations = {
    "idle": AnimationClip.uniform(frames, fps=6),
    "move": AnimationClip.uniform(frames, fps=10),
}
animator = AnimationManager(animations, initial_state="idle")

clock = pygame.time.Clock()
running = True
while running:
    dt = min(clock.tick(60) / 1000.0, 0.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    animator.update(dt)
    current_image = animator.frame
```

Para ver a demonstração genérica completa, execute:

```powershell
python animation2d.py
```

Para conferir os testes automatizados:

```powershell
$env:SDL_VIDEODRIVER = "dummy"
python -m unittest -v test_animation2d.py
```

## Regra desta etapa

Nenhuma animação deste laboratório é considerada definitiva por estar apenas
presente. A integração com o jogo principal será feita somente depois da
aprovação visual do usuário.
