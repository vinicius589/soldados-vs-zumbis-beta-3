import pygame
from core.input import Input


class Base:
    # O jogo continua sendo desenhado em 1280x720.
    # No Android, essa imagem e ampliada para preencher a tela inteira.
    def __init__(self, screen_size=(1280, 720)):
        pygame.init()

        self.virtual_size = screen_size

        # Pede a area inteira disponivel do aparelho.
        # (0, 0) evita prender o jogo aos 1280x720 do PC.
        try:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        except pygame.error:
            # Fallback para ambientes que nao aceitam fullscreen.
            self.display = pygame.display.set_mode(screen_size)

        self.display_size = self.display.get_size()

        # Superficie virtual onde o jogo original continua desenhando.
        self.screen = pygame.Surface(self.virtual_size).convert()

        pygame.display.set_caption("Soldados vs Zumbis")
        self.clock = pygame.time.Clock()
        self.input = Input()
        self.running = True

    def _map_input_to_virtual_screen(self):
        """Converte toque/mouse da tela real para 1280x720."""
        display_width, display_height = self.display_size
        if display_width <= 0 or display_height <= 0:
            return

        mouse_x, mouse_y = self.input.mouse_position
        virtual_width, virtual_height = self.virtual_size

        self.input.mouse_position = (
            max(0, min(virtual_width - 1, int(mouse_x * virtual_width / display_width))),
            max(0, min(virtual_height - 1, int(mouse_y * virtual_height / display_height))),
        )

    def initialize(self):
        pass

    def update(self, delta_time):
        pass

    def draw(self):
        pass

    def _present(self):
        """Amplia a tela virtual para o tamanho real do celular."""
        if self.display.get_size() != self.display_size:
            self.display_size = self.display.get_size()

        if self.display_size == self.virtual_size:
            self.display.blit(self.screen, (0, 0))
        else:
            scaled = pygame.transform.scale(self.screen, self.display_size)
            self.display.blit(scaled, (0, 0))

        pygame.display.flip()

    def run(self):
        self.initialize()

        while self.running:
            delta_time = min(self.clock.tick(60) / 1000.0, 0.033)
            self.input.update()
            self._map_input_to_virtual_screen()

            if self.input.quit:
                self.running = False

            self.update(delta_time)
            self.draw()
            self._present()

        pygame.quit()
