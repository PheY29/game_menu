import pygame
import random


class Game:
    def __init__(self, screen, game_state_manager, color_manager):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.game_state_manager = game_state_manager
        self.color_manager = color_manager

        self.font = pygame.font.Font("assets/font.ttf", size=40)
        self.rgb_color = random.randint(0, 90), random.randint(0, 90), random.randint(0, 90)

        self.keys = {}
        self.mouse_button = {}
        self.mouse_pos = []
        self.pause = False

    def run(self):
        if not self.pause:
            self.update_screen()
            self.handle_input()

    def handle_input(self):
        if self.keys.get(pygame.K_ESCAPE):
            self.pause = True
            self.keys = {}
            self.game_state_manager.set_state("pause")

    def update_screen(self):
        for y in range(self.height):
            interpolation = y / self.height
            color = (
                # on part de noir (0) + le dégradé qui augmente jusqu'a la couleur choisis
                int(((1 - interpolation) * 0) + (interpolation * self.rgb_color[0])),
                int(((1 - interpolation) * 0) + (interpolation * self.rgb_color[1])),
                int(((1 - interpolation) * 0) + (interpolation * self.rgb_color[2]))
            )
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

    def handle_collision(self):
        pass

    def timer(self, screen):
        pass

    def reset_game_init(self):
        self.rgb_color = random.randint(0, 90), random.randint(0, 90), random.randint(0, 90)
        self.keys = {}
        self.mouse_button = {}
        self.mouse_pos = []
        self.pause = False
