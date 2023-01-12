from board.board import Board
from service.board_service import BoardService
from ai.ai import AI
from config.definitions import ROOT_DIR
import pygame
import os


class GraphicalUI:
    def __init__(self, last_winner):
        self._board_size = 6
        self._last_winner = last_winner
        self.first_computer_move = True

        # Initialize the pygame instance and the mixer used for sound effects. 
        pygame.init()
        pygame.mixer.init()

        # Create instances of the board, the board service and the computer player. 
        self.game_board = Board(self._board_size)
        self.board_service = BoardService(self.game_board)
        self.computer_player = AI(self.board_service)
        
        # Define the window size.  
        self.WIN_SIZE = 600
        self.CELL_SIZE = self.WIN_SIZE // 6
        self.screen = pygame.display.set_mode((self.WIN_SIZE, self.WIN_SIZE))
        pygame.display.set_caption("Obstruction")
        self.clock = pygame.time.Clock()

        # Load the images. 
        self.board_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/board.png"))
        self.x_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/x.png"))
        self.o_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/o.png"))
        self.blocked_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/blocked.png"))
        self.menu_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/menu.png"))
        self.rules_image = pygame.image.load(os.path.join(ROOT_DIR, "assets/images/rules.png"))

        # Load the sound effects. 
        self.player_draw_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "assets/sounds/draw_sound0.ogg"))
        self.computer_draw_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "assets/sounds/draw_sound1.ogg"))
        self.button_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "assets/sounds/button_sound.ogg"))
        self.win_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "assets/sounds/win_sound.ogg"))
        self.loss_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "assets/sounds/loss_sound.ogg"))

    def draw_objects(self):
        """
            This method draws the objects over the background image(the game board).
        """
        for i in range(self._board_size):
            for j in range(self._board_size):
                symbol = self.board_service.get_symbol(i, j)
                if symbol != None:
                    if symbol == 'X':
                        self.screen.blit(self.x_image, (j * self.CELL_SIZE, i * self.CELL_SIZE))
                    elif symbol == 'O':
                        self.screen.blit(self.o_image, (j * self.CELL_SIZE, i * self.CELL_SIZE))
                    elif symbol == '-':
                        self.screen.blit(self.blocked_image, (j * self.CELL_SIZE, i * self.CELL_SIZE))

    def show_menu(self):
        self.screen.blit(self.menu_image, (0, 0))

    def show_rules(self):
        self.screen.blit(self.rules_image, (0, 0))

    def run_menu(self):
        mouse_y, mouse_x = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and mouse_y >= 222 and mouse_y <= 380 and mouse_x >= 183 and mouse_x <= 250:
            return 'play'

        elif left_click and mouse_y >= 211 and mouse_y <= 393 and mouse_x >= 284 and mouse_x <= 352:
            return 'rules'

        elif left_click and mouse_y >= 217 and mouse_y <= 383 and mouse_x >= 383 and mouse_x <= 450:
            return 'quit'

        return None

    def run_rules(self):
        mouse_y, mouse_x = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and mouse_y >= 200 and mouse_y <= 400 and mouse_x >= 498 and mouse_x <= 552:
            return 'return'

        return None

    def draw(self):
        self.screen.blit(self.board_image, (0, 0))
        self.draw_objects()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return not None

        return None

    def run_game_process(self):
        mouse_y, mouse_x = pygame.mouse.get_pos()
        col, row = mouse_y // self.CELL_SIZE, mouse_x // self.CELL_SIZE
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.board_service.get_symbol(row, col) == ' ':
            self.board_service.make_move(row, col, 'X')
            pygame.mixer.Sound.play(self.player_draw_sound)
            if not self.board_service.check_if_game_over():
                self.draw()
                pygame.display.update()
                pygame.time.wait(500)
                self.computer_player.computer_move(self.first_computer_move)
                self.first_computer_move = False
                pygame.mixer.Sound.play(self.computer_draw_sound)
            else:
                return 'player'

            if self.board_service.check_if_game_over():
                return 'computer'

    def start(self):
        player_score = 0
        computer_score = 0

        stop_game = False
        winner = None
        game_over = False

        while True:
            self.show_menu()
            pygame.display.update()
            quit_game = self.check_events()
            self.clock.tick(60)

            if quit_game is not None:
                pygame.quit()
                break

            if self.run_menu() == 'play':
                pygame.mixer.Sound.play(self.button_sound)
                while True:
                    self.first_computer_move = True
                    quit_game = None
                    winner = None
                    pygame.time.wait(300)

                    if self._last_winner == 'computer':
                        self.computer_player.computer_move(self.first_computer_move)
                        self.first_computer_move = False

                    while True:
                        self.draw()
                        pygame.display.update()

                        pygame.display.set_caption(f"Obstruction                                    Player: {player_score} vs. Computer: {computer_score}")

                        quit_game = self.check_events()
                        self.clock.tick(60)

                        if winner is not None:
                            quit_game = not None

                        if quit_game is not None and winner is None:
                            stop_game = True
                            break

                        elif quit_game is not None and winner is not None:
                            if winner == 'player':
                                pygame.time.wait(100)
                                player_score += 1
                                pygame.mixer.Sound.play(self.win_sound)
                            else:
                                pygame.time.wait(100)
                                computer_score += 1
                                pygame.mixer.Sound.play(self.loss_sound)

                            pygame.time.wait(1000)
                            break
                        
                        winner = self.run_game_process()

                    self.game_board = Board(self._board_size)
                    self.board_service = BoardService(self.game_board)
                    self.computer_player = AI(self.board_service)

                    if winner is not None:
                        self._last_winner = winner

                    if quit_game is not None and winner is None:
                        stop_game = True
                        break

                if stop_game:
                    break

            elif self.run_menu() == 'rules':
                pygame.mixer.Sound.play(self.button_sound)
                pygame.time.wait(50)
                while True:
                    self.show_rules()
                    pygame.display.update()
                    quit_game = self.check_events()
                    self.clock.tick(60)

                    if self.run_rules() == 'return':
                        pygame.time.wait(50)
                        pygame.mixer.Sound.play(self.button_sound)
                        break

                    if quit_game is not None:
                        stop_game = True
                        break

            elif self.run_menu() == 'quit':
                break

            if stop_game:
                break

        pygame.quit()
        return self._last_winner
