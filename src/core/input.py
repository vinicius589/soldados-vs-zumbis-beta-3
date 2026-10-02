import pygame


class Input:
    def __init__(self):
        self.quit = False
        self.mouse_position = (0, 0)
        self.mouse_pressed = (False, False, False)
        self.just_clicked = False
        self.just_right_clicked = False
        self.keys_pressed = set()

    def update(self):
        self.just_clicked = False
        self.just_right_clicked = False
        self.keys_pressed.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.just_clicked = True
                elif event.button == 3:
                    self.just_right_clicked = True
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)

        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
