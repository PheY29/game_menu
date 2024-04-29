import pygame
import json
import sys


class Start:
    def __init__(self, screen, game, game_state_manager, color_manager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.game = game
        self.game_state_manager = game_state_manager
        self.color_manager = color_manager
        # self.screen_img = pygame.image.load("")
        self.font = pygame.font.Font("assets/font.ttf", size=40)

        self.text_rects = {}
        self.keys = {}
        self.mouse_button = {}
        self.mouse_pos = []

        self.default_color = [[255, 153, 102], [255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1], [-1, -1, 1]]

        self.play_selected = False
        self.setting_selected = False
        self.quit_selected = False
        self.mouse_left_click = False

    def run(self):
        self.update_screen()
        self.handle_input()

    def update_screen(self):
        self.screen.fill("aquamarine4")

        text_infos = [
            ("Play", self.width // 2, self.height // 2),
            ("Setting", self.width // 2, self.height // 2 + 50),
            ("Quit", self.width // 2, self.height // 2 + 100)
        ]

        for i, (text, x, y) in enumerate(text_infos):
            self.text_rects[text] = self.color_manager.get_text_rect(text, 40, x, y)
            self.color_manager.color_text(self.default_color[i], self.base_color_direction[i], 5, text, 40, x, y)

    def handle_input(self):
        try:
            if self.keys.get(pygame.K_ESCAPE) or (self.text_rects["Quit"].collidepoint(self.mouse_pos)
                                                  and self.mouse_button[0] and not self.mouse_left_click):
                pygame.quit()
                sys.exit()

            ############
            for button_name, button_rect in self.text_rects.items():  # dict_items([('Play', <rect(585, 375, 110, 51)>))
                setattr(self, button_name.lower() + '_selected', button_rect.collidepoint(self.mouse_pos))
                # setattr(object, attribute_name, condition)

                selected_values = [self.play_selected, self.setting_selected, self.quit_selected]
                for i, selected in enumerate(selected_values):  # 0,play - 1,setting - 2,leave
                    if selected:
                        self.base_color_direction[i] = self.color_direction[i]
                        for j in range(3):  # les 3 couleurs [x, x, x]
                            self.default_color[i][j] = max(min(self.default_color[i][j], 255), 0)
                            # fait en sorte que default_color ne dépasse pas 255 et ensuite pas en dessous de 0
                    else:
                        self.default_color[i] = [255, 153, 102]
                        self.base_color_direction[i] = [0, 0, 0]
            ############

            if (self.text_rects["Play"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.game_state_manager.set_state("game")

            if (self.text_rects["Setting"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.game_state_manager.set_state("setting")

            if not self.mouse_button[0]:
                self.mouse_left_click = False

        except TypeError:
            pass

    def reset_start_menu(self):
        self.keys = {}
        self.mouse_pos = []
        self.default_color = [[255, 153, 102], [255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1], [-1, -1, 1]]
        self.play_selected = False
        self.setting_selected = False
        self.quit_selected = False


class Setting:
    def __init__(self, screen, game, start, pause, game_state_manager, color_manager):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.game = game
        self.start = start
        self.pause = pause
        self.game_state_manager = game_state_manager
        self.color_manager = color_manager

        self.font = pygame.font.Font("assets/font.ttf", size=40)
        self.json_file = "others/setting.json"

        with open(self.json_file, "r") as f:
            self.configurations = json.load(f)

        self.text_rects = {}
        self.button_rects = {}
        self.keys = {}
        self.mouse_button = {}
        self.mouse_pos = []

        self.default_color = [[255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1]]

        self.return_selected = False
        self.save_selected = False
        self.mouse_left_click = True

        self.event = None
        self.loading_setting = []
        self.user_text = ""
        self.drawing_text = False

    def run(self):
        self.update_screen()
        self.handle_input()

    def update_screen(self):
        self.screen.fill("gray38")

        text_infos = [
            ("Setting", self.width // 2, self.height // 3 - 100, 50),
            ("Resolution", self.width // 2 - 125, self.height // 3, 30),
            ("Up", self.width // 2 - 125, self.height // 3 + 50, 30),
            ("Down", self.width // 2 - 125, self.height // 3 + 100, 30),
            ("Left", self.width // 2 - 125, self.height // 3 + 150, 30),
            ("Right", self.width // 2 - 125, self.height // 3 + 200, 30),
            ("Escape", self.width // 2 - 125, self.height // 3 + 250, 30)
        ]

        return_button_rect = pygame.Rect(self.width // 2 - 200, self.height // 3 + 350, 150, 50)
        save_button_rect = pygame.Rect(self.width // 2 + 50, self.height // 3 + 350, 150, 50)
        text_infos2 = [
            ("Return", return_button_rect.center[0], return_button_rect.center[1], 30),
            ("Save", save_button_rect.center[0], save_button_rect.center[1], 30)
        ]

        for i, (text, x, y, size) in enumerate(text_infos):
            self.text_rects[text] = self.color_manager.get_text_rect(text, size, x, y)
            if text != "Setting":
                if text == "Resolution":
                    for j in range(2):
                        button_rect = pygame.Rect(x + 190 + (j*180), y - 13.5, 150, 35)
                        pygame.draw.rect(self.screen, (150, 150, 150), button_rect)
                        self.button_rects[text + "_button" + f"{j}"] = button_rect
                else:
                    button_rect = pygame.Rect(x + 190, y - 13.5, 120, 35)
                    pygame.draw.rect(self.screen, (150, 150, 150), button_rect)
                    self.button_rects[text + "_button"] = button_rect

            self.color_manager.color_text([255, 153, 102], [0, 0, 0], 5, text, size, x, y)

        for i, (text, x, y, size) in enumerate(text_infos2):
            self.text_rects[text] = self.color_manager.get_text_rect(text, size, x, y)

            if text == "Return":
                pygame.draw.rect(self.screen, (150, 150, 150), return_button_rect)
            elif text == "Save":
                pygame.draw.rect(self.screen, (150, 150, 150), save_button_rect)

            self.color_manager.color_text(self.default_color[i], self.base_color_direction[i], 5, text, size, x, y)

        self.loading_setting = [
            ("720p", str(self.configurations["720p"])[1:-1].replace(", ", "x"),
             self.button_rects["Resolution_button0"]),
            ("1080p", str(self.configurations["1080p"])[1:-1].replace(", ", "x"),
             self.button_rects["Resolution_button1"]),
            ("Up", self.configurations["up"], self.button_rects["Up_button"]),
            ("Down", self.configurations["down"], self.button_rects["Down_button"]),
            ("Left", self.configurations["left"], self.button_rects["Left_button"]),
            ("Right", self.configurations["right"], self.button_rects["Right_button"]),
            ("Escape", self.configurations["escape"], self.button_rects["Escape_button"])
        ]

        for i, (button_name, value, rect) in enumerate(self.loading_setting):
            self.color_manager.draw_text(value, 20, [255, 153, 102], rect.center[0], rect.center[1])

    def handle_input(self):
        try:
            for button_name, button_rect in self.text_rects.items():
                if button_name in ["Return", "Save"]:
                    setattr(self, button_name.lower() + '_selected', button_rect.collidepoint(self.mouse_pos))

                    selected_values = [self.return_selected, self.save_selected]
                    for i, selected in enumerate(selected_values):
                        if selected:
                            self.base_color_direction[i] = self.color_direction[i]
                            for j in range(3):
                                self.default_color[i][j] = max(min(self.default_color[i][j], 255), 0)
                        else:
                            self.default_color[i] = [255, 153, 102]
                            self.base_color_direction[i] = [0, 0, 0]

            if (self.text_rects["Return"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.start.reset_start_menu()
                self.game_state_manager.set_state("start")
                self.game.screen = self.screen
                self.reset_setting_menu()

            if (self.text_rects["Save"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.save_configurations()

            for name, rect in self.button_rects.items():
                if rect.collidepoint(self.mouse_pos):
                    pygame.draw.rect(self.screen, (200, 200, 200), rect, 5)

                    if "Resolution" in name:
                        if self.mouse_button[0] and not self.mouse_left_click:
                            if "0" in name:
                                x = self.configurations["720p"][0]
                                y = self.configurations["720p"][1]
                                self.screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)
                                self.change_resolution(x, y)
                            elif "1" in name:
                                x = self.configurations["1080p"][0]
                                y = self.configurations["1080p"][1]
                                self.screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)
                                self.change_resolution(x, y)

                    elif self.mouse_button[0] and not self.mouse_left_click:
                        self.drawing_text = True

                        while self.drawing_text:
                            input_rect = pygame.Rect(rect)
                            pygame.draw.rect(self.screen, (150, 150, 150), input_rect)
                            pygame.draw.rect(self.screen, (200, 200, 200), rect, 5)
                            self.color_manager.draw_text("Press New Key", 20, [255, 153, 0],
                                                         input_rect.center[0] + 200, input_rect.center[1], 255)

                            self.handle_event_input()

                            key_already_assigned = False
                            for action, assigned_key in self.configurations.items():  # up, z / down, s...
                                if action != name.split("_")[0].lower() and assigned_key == self.user_text:
                                    # True : down != up (wanted) and s == s (wanted)
                                    # False : up not != up (wanted) and z (old) == z or anything (wanted)
                                    key_already_assigned = True
                                    break

                            if not key_already_assigned:
                                self.color_manager.draw_text(self.user_text, 20, [255, 153, 102], input_rect.center[0],
                                                             input_rect.center[1])

                                if self.user_text:
                                    self.modify_configurations(name.split("_")[0].lower(), self.user_text)
                                    self.user_text = ""
                                    self.drawing_text = False
                            else:
                                self.color_manager.draw_text("Key Already Assigned", 20, [255, 153, 0], self.width // 2,
                                                             self.height // 3 + 325, 255)
                                self.user_text = ""

                            pygame.display.update()

            if not self.mouse_button[0]:
                self.mouse_left_click = False

        except TypeError:
            pass

    def handle_event_input(self):
        for event in pygame.event.get():
            self.mouse_button = pygame.mouse.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                self.event = event
            if event.type == pygame.KEYUP:
                self.keys[event.key] = False

        if self.event:
            if self.drawing_text:
                if self.keys.get(pygame.K_BACKSPACE):
                    self.user_text = self.user_text[:-1]
                else:
                    if self.event.key == 27:
                        self.user_text = "ESCAPE"
                    elif self.event.unicode.isalpha() and len(self.user_text) < 1:
                        self.user_text += self.event.unicode

                self.event = None

    def modify_configurations(self, key, value):
        self.configurations[key] = value

    def save_configurations(self):
        end_time = pygame.time.get_ticks() + 500
        show_message = True

        with open(self.json_file, 'w') as f:
            json.dump(self.configurations, f, indent=4)

        while show_message:
            current_time = pygame.time.get_ticks()
            if current_time > end_time:
                show_message = False
            if show_message:
                self.color_manager.draw_text("Setting Saved", 20, [255, 153, 0], self.width // 2,
                                             self.height // 3 + 325, 255)

            pygame.display.update()

    def change_resolution(self, x, y):
        state_list = ["game", "start", "pause"]
        for state in state_list:
            state_obj = getattr(self, state)
            state_obj.screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)
            state_obj.width = state_obj.screen.get_width()
            state_obj.height = state_obj.screen.get_height()

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

    def reset_setting_menu(self):
        self.keys = {}
        self.mouse_pos = []
        self.default_color = [[255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1]]
        self.return_selected = False
        self.save_selected = False


class Pause:
    def __init__(self, screen, game, start, game_state_manager, color_manager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.game = game
        self.start = start
        self.game_state_manager = game_state_manager
        self.color_manager = color_manager

        self.font = pygame.font.Font("assets/font.ttf", size=40)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.text_rects = {}
        self.keys = {}
        self.mouse_button = {}
        self.mouse_pos = []

        self.default_color = [[255, 153, 102], [255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1], [-1, -1, 1]]
        self.text_opacity = 0
        self.max_text_opacity = 255
        self.text_appear_speed = 1

        self.resume_selected = False
        self.restart_selected = False
        self.quit_selected = False
        self.mouse_left_click = True

    def run(self):
        self.update_screen()
        self.handle_input()

    def update_screen(self):
        pygame.draw.rect(self.surface, (128, 128, 128, 1), [0, 0, self.width, self.height])
        self.screen.blit(self.surface, (0, 0))

        self.color_manager.color_text([255, 153, 102], [0, 0, 0], 5, "Paused", 50, self.width // 2,
                                      self.height // 2 - 100, self.text_opacity)

        text_infos = [
            ("Resume", self.width // 2, self.height // 2 + 100, 30),
            ("Restart", self.width // 2, self.height // 2 + 150, 30),
            ("Quit", self.width // 2, self.height // 2 + 200, 30)
        ]

        for i, (text, x, y, size) in enumerate(text_infos):
            self.text_rects[text] = self.color_manager.get_text_rect(text, size, x, y)
            self.color_manager.color_text(self.default_color[i], self.base_color_direction[i], 5, text, size, x, y,
                                          self.text_opacity)

        self.check_opacity()

    def check_opacity(self):
        if self.text_opacity < self.max_text_opacity:
            self.text_opacity += self.text_appear_speed

    def handle_input(self):
        try:
            for button_name, button_rect in self.text_rects.items():
                setattr(self, button_name.lower() + '_selected', button_rect.collidepoint(self.mouse_pos))

                selected_values = [self.resume_selected, self.restart_selected, self.quit_selected]
                for i, selected in enumerate(selected_values):
                    if selected:
                        self.base_color_direction[i] = self.color_direction[i]
                        for j in range(3):
                            self.default_color[i][j] = max(min(self.default_color[i][j], 255), 0)
                    else:
                        self.default_color[i] = [255, 153, 102]
                        self.base_color_direction[i] = [0, 0, 0]

            if (self.text_rects["Quit"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.game.reset_game_init()
                self.start.reset_start_menu()
                self.game_state_manager.set_state("start")
                self.reset_pause_menu()

            if self.keys.get(pygame.K_ESCAPE) or (self.text_rects["Resume"].collidepoint(self.mouse_pos)
                                                  and self.mouse_button[0] and not self.mouse_left_click):
                self.mouse_left_click = True
                self.game.pause = False
                self.game_state_manager.set_state("game")
                self.reset_pause_menu()

            if (self.text_rects["Restart"].collidepoint(self.mouse_pos) and self.mouse_button[0]
                    and not self.mouse_left_click):
                self.mouse_left_click = True
                self.game.reset_game_init()
                # TODO self.game.reset_game_stat()
                self.game_state_manager.set_state("game")
                self.text_opacity = 0

            if not self.mouse_button[0]:
                self.mouse_left_click = False

        except TypeError:
            pass

    def reset_pause_menu(self):
        self.keys = {}
        self.mouse_pos = []
        self.default_color = [[255, 153, 102], [255, 153, 102], [255, 153, 102]]
        self.base_color_direction = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.color_direction = [[-1, -1, 1], [-1, -1, 1], [-1, -1, 1]]
        self.text_opacity = 0
        self.resume_selected = False
        self.restart_selected = False
        self.quit_selected = False
