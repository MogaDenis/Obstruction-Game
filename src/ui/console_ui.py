from board.board import Board, InvalidMoveException
from service.board_service import BoardService
from ai.ai import AI
import os


class InvalidInputException(Exception):
    pass


class ConsoleUI:
    def __init__(self, last_winner):
        self._board_size = 6
        self._last_winner = last_winner

    def game_over_message(self, winner):
        if winner == 'player':
            print("\n~ Congratulations! You won the game! ~")
        elif winner == 'computer':
            print("\n~ Bad luck! The computer won the game! ~")
        elif winner is None:
            print("\n~ Leaving so soon? ~")

    def display_rules_menu(self):
        print("""
     _____       _           
    |  __ \     | |          
    | |__) |   _| | ___  ___ 
    |  _  / | | | |/ _ \/ __|
    | | \ \ |_| | |  __/\__ \\
    |_|  \_\__,_|_|\___||___/                
        """)

        print("~ The game is played on a 6 x 6 grid. The user plays with 'X' and the computer uses 'O'.")
        print("\n~ The players take turns in writing their symbol in an empty cell. Placing a symbol blocks all \n"
        "of the neighbouring cells from both players, which is indicated by the symbol '-'.")
        print("\n~ The first player unable to make a move loses.")
        print("\n~ Whoever won the last game will make the first move in the next one.")

    def invalid_input_message(self):
        return "\nInvalid input!"

    def invalid_move_message(self):
        return "\nInvalid move!"

    def display_title(self):
        print("""
     ___  _         _                   _   _             
    / _ \| |__  ___| |_ _ __ _   _  ___| |_(_) ___  _ __  
   | | | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \ 
   | |_| | |_) \__ \ |_| |  | |_| | (__| |_| | (_) | | | |
    \___/|_.__/|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_|
        """)

        print("~ After typing each command, hit ENTER.")
        print("~ To make a move: Type 'move <row> <column>'")
        print("~ Indexing starts at 1.")
        print("~ Type 'rules' to see the rules of the game.")
        print("~ Type 'exit' to stop the game.\n")

    def read_user_move(self):
        user_input = input('\n>> ').strip().lower()

        tokens = user_input.split()

        if len(tokens) == 0:
            raise InvalidInputException

        if len(tokens) == 2 or len(tokens) > 3:
            raise InvalidInputException

        if tokens[0] not in ['move', 'exit', 'rules']:
            raise InvalidInputException

        if (tokens[0] == 'exit' or tokens[0] == 'rules') and len(tokens) != 1:
            raise InvalidInputException

        if tokens[0] == 'move':
            if not tokens[1].isnumeric() or not tokens[2].isnumeric():
                raise InvalidInputException

        return tokens 

    def display_score(self, player, computer):
        print(f"\t~ Score => Player: {player} vs. Computer: {computer}\n")

    def start(self):
        stop_game = False

        player_score = 0
        computer_score = 0

        while True:
            game_board = Board(self._board_size)
            board_service = BoardService(game_board)
            computer_player = AI(board_service)

            board_service.add_indices_to_board()

            error_message = None

            winner = None
            game_over = False

            if self._last_winner == 'computer':
                computer_player.computer_move()

            while True:
                os.system('cls')
                self.display_title()
                self.display_score(player_score, computer_score)
                print(game_board)

                if game_over:
                    break

                if error_message is not None:
                    print(error_message)
                    error_message = None

                try:
                    tokens = self.read_user_move()

                    if tokens[0] == 'exit':
                        # The user chose to stop the game. 
                        stop_game = True
                        break

                    elif tokens[0] == 'rules':
                        os.system('cls')
                        self.display_rules_menu()

                        exit_rules_menu = input("\nPress ENTER to return to the game...")

                    elif tokens[0] == 'move':
                        try:
                            board_service.make_move(int(tokens[1]) - 1, int(tokens[2]) - 1, 'X')

                            if board_service.check_if_game_over():
                                winner = 'player'
                                player_score += 1
                                game_over = True

                            if not game_over:
                                computer_player.computer_move()

                                if board_service.check_if_game_over():
                                    winner = 'computer'
                                    computer_score += 1
                                    game_over = True

                        except InvalidMoveException:
                            error_message = self.invalid_move_message()

                except InvalidInputException:
                    error_message = self.invalid_input_message()

            if winner is not None:
                self._last_winner = winner

            if stop_game:
                break
            
            self.game_over_message(winner)
            round_pause = input("\nPress ENTER to advance to the next round...")

        if winner is None:
            self.game_over_message(winner)

        exit_pause = input("\nPress ENTER to exit the application...")

        return self._last_winner
            
            

            