import unittest
import copy
import random
from board.board import Board, InvalidMoveException
from service.board_service import BoardService
from ai.ai import AI


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.game_board = Board(6)

    def test_get_symbol(self):
        # When the board is empty, all positions should contain only a space. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        self.assertEqual(' ', self.game_board.get_symbol(random_row, random_col))

        # If we made a move into that position, now the value there should be the given symbol. 
        self.game_board.make_move(random_row, random_col, 'X')

        self.assertEqual('X', self.game_board.get_symbol(random_row, random_col))

    def test_check_if_position_is_in_board(self):
        # First let's try a position which is in board, so the method should return True.
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        check_result = self.game_board.check_if_position_is_in_board(random_row, random_col)
        self.assertEqual(True, check_result)

        # Now let's try a position which is outside the game board. 
        random_col = (random_col + 1) * (-1)

        check_result = self.game_board.check_if_position_is_in_board(random_row, random_col)
        self.assertEqual(False, check_result)

    def test_check_if_valid_move(self):
        # If the method returns None, the move is valid, otherwise it raises an exception. 
        # A random move inside an empty board is valid. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        check_result = self.game_board.check_if_valid_move(random_row, random_col)
        self.assertEqual(None, check_result)

        # Now let's make a move in that spot and check if the exception is raised. 
        self.game_board.make_move(random_row, random_col, 'X')
        self.assertRaises(InvalidMoveException, self.game_board.check_if_valid_move, random_row, random_col)

        # Also, check the adjacent spaces which should be blocked. 
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.game_board.check_if_position_is_in_board(i, j) and i != random_row and j != random_col:
                    self.assertRaises(InvalidMoveException, self.game_board.check_if_valid_move, i, j)

    def test_check_full_board(self):
        # This method applied on an empty board should return False. 
        self.assertEqual(False, self.game_board.check_full_board())

        # On a board 6 x 6 the min number of moves to fill it is 4. 
        self.game_board.make_move(1, 1, 'X')
        # At this stage, the method should still return False. 
        self.assertEqual(False, self.game_board.check_full_board())

        # Now, let's fill it all the way. 
        self.game_board.make_move(1, 4, 'O')
        self.game_board.make_move(4, 1, 'X')
        self.game_board.make_move(4, 4, 'O')

        self.assertEqual(True, self.game_board.check_full_board())

    def test_make_move(self):
        # Let's make a random move on the empty board. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)
        self.game_board.make_move(random_row, random_col, 'X')

        # Check if the symbol in the random position is the one given. 
        self.assertEqual('X', self.game_board.get_symbol(random_row, random_col))

        # Check if the adjacent positions were blocked/marked with '-'. 
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.game_board.check_if_position_is_in_board(i, j) and i != random_row and j != random_col:
                    self.assertEqual('-', self.game_board.get_symbol(i, j))

        # We should also be unable to make a move in a spot that is occupied. 
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.game_board.check_if_position_is_in_board(i, j):
                    self.assertRaises(InvalidMoveException, self.game_board.make_move, random_row, random_col, 'O')

    def test_block_adjacent_positions(self):
        # Obtain a random position. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)
        
        # Block the adjacent spaces to that one. 
        self.game_board.block_adjacent_positions(random_row, random_col)

        # Now check if those adjacent spaces have the appropriate symbol in them.
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.game_board.check_if_position_is_in_board(i, j) and i != random_row and j != random_col:
                    self.assertEqual('-', self.game_board.get_symbol(i, j))


class TestBoardService(unittest.TestCase):
    def setUp(self):
        self.game_board = Board(6)
        self.board_service = BoardService(self.game_board)

    def test_get_board(self):
        self.assertEqual(self.game_board.board, self.board_service.get_board())

    def test_get_board_size(self):
        self.assertEqual(self.game_board.size, self.board_service.get_board_size())

    def test_check_if_position_is_in_board(self):
        # First let's try a position which is in board, so the method should return True.
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        check_result = self.board_service.check_if_position_is_in_board(random_row, random_col)
        self.assertEqual(True, check_result)

        # Now let's try a position which is outside the game board. 
        random_col = (random_col + 1) * (-1)

        check_result = self.board_service.check_if_position_is_in_board(random_row, random_col)
        self.assertEqual(False, check_result)

    def test_check_if_game_over(self):
        # This method applied on an empty board should return False. 
        self.assertEqual(False, self.board_service.check_if_game_over())

        # On a board 6 x 6 the min number of moves to fill it is 4. 
        self.game_board.make_move(1, 1, 'X')
        # At this stage, the method should still return False. 
        self.assertEqual(False, self.game_board.check_full_board())

        # Now, let's fill it all the way. 
        self.game_board.make_move(1, 4, 'O')
        self.game_board.make_move(4, 1, 'X')
        self.game_board.make_move(4, 4, 'O')

        # Now the game should be over because the board is full.
        self.assertEqual(True, self.board_service.check_if_game_over())

    def test_get_symbol(self):
        # When the board is empty, all positions should contain only a space. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        self.assertEqual(' ', self.board_service.get_symbol(random_row, random_col))

        # If we made a move into that position, now the value there should be the given symbol. 
        self.board_service.make_move(random_row, random_col, 'X')

        self.assertEqual('X', self.board_service.get_symbol(random_row, random_col))

    def test_make_move(self):
        # Let's make a random move on the empty board. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)
        self.board_service.make_move(random_row, random_col, 'X')

        # Check if the symbol in the random position is the one given. 
        self.assertEqual('X', self.board_service.get_symbol(random_row, random_col))

        # Check if the adjacent positions were blocked/marked with '-'. 
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.board_service.check_if_position_is_in_board(i, j) and i != random_row and j != random_col:
                    self.assertEqual('-', self.board_service.get_symbol(i, j))

        # We should also be unable to make a move in a spot that is occupied, so an exception should be raised. 
        for i in range(random_row - 1, random_row + 2):
            for j in range(random_col - 1, random_col + 2):
                if self.board_service.check_if_position_is_in_board(i, j):
                    self.assertRaises(InvalidMoveException, self.board_service.make_move, random_row, random_col, 'O')


class testAI(unittest.TestCase):
    def setUp(self):
        self.game_board = Board(6)
        self.board_service = BoardService(self.game_board)
        self.computer_player = AI(self.board_service)

    def test_search_valid_positions(self):
        # When the board is empty, all positions should be valid. 
        valid_positions = self.computer_player.search_valid_positions()
        self.assertEqual(self.board_service.get_board_size() ** 2, len(valid_positions))

        # If we make a move, then that position and the adjacent ones are not valid anymore. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)
        self.board_service.make_move(random_row, random_col, 'X')

        valid_positions = self.computer_player.search_valid_positions()

        for position in valid_positions:
            # Make sure the random chosen position is not in the dictionary. 
            self.assertNotEqual((random_row, random_col), position)
            for i in range(random_row - 1, random_row + 2):
                for j in range(random_col - 1, random_col + 2):
                    # Also check if every valid positions is different to one which has been blocked. 
                    self.assertNotEqual((i, j), position)

    def test_calculate_number_of_positions_blocked(self):
        # Let's make a random move on the empty board. 
        random_row = random.randint(0, self.game_board.size - 1)
        random_col = random.randint(0, self.game_board.size - 1)

        # Calculate the number of positions blocked. 
        positions_blocked_count = self.computer_player.calculate_num_of_positions_blocked(random_row, random_col)

        # Make the move. 
        self.board_service.make_move(random_row, random_col, 'X')

        # Since that is the only move, the number of positions blocked is also the number of times the '-' symbol appears. 
        dash_count = 0
        for i in range(self.board_service.get_board_size()):
            for j in range(self.board_service.get_board_size()):
                if self.board_service.get_symbol(i, j) == '-':
                    dash_count += 1

        self.assertEqual(dash_count, positions_blocked_count)

    def test_find_best_moves(self):
        # In an empty board, the best moves are those which block 8 spaces. 
        valid_positions = self.computer_player.search_valid_positions()

        best_moves, max_profit = self.computer_player.find_best_moves(valid_positions)

        # Make sure the maximum number of positions blocked is 8. 
        self.assertEqual(8, max_profit)

        # Check if every 'best move' is inside the board. 
        for position in best_moves:
            self.assertEqual(True, self.board_service.check_if_position_is_in_board(position[0], position[1]))   

    def test_find_average_moves(self):
        # After we search for the best moves, in an empty board the average moves block 5 spaces. 
        valid_positions = self.computer_player.search_valid_positions()

        best_moves, max_profit = self.computer_player.find_best_moves(valid_positions)

        average_moves, average_profit = self.computer_player.find_average_moves(valid_positions, max_profit)

        # Make sure the maximum number of positions blocked by the average moves is 5. 
        self.assertEqual(5, average_profit)

        # Check if every 'average_move' is inside the board. 
        for position in average_moves:
            self.assertEqual(True, self.board_service.check_if_position_is_in_board(position[0], position[1]))   

    def test_computer_move(self):
        # In an empty board, the computer will make a move which blocks 8 spaces. 
        # That move is in the 'best moves' category. 

        initial_board = copy.deepcopy(self.board_service.get_board())

        valid_positions = self.computer_player.search_valid_positions()
        best_moves, max_profit = self.computer_player.find_best_moves(valid_positions)

        self.computer_player.computer_move()

        computer_move = None

        for i in range(self.board_service.get_board_size()):
            for j in range(self.board_service.get_board_size()):
                # Find the move made by the computer. 
                if initial_board[i][j] == ' ' and self.board_service.get_symbol(i, j) == 'O':
                    computer_move = (i, j)

        # Make sure it is a move which blocks the maximum number of positions. 
        self.assertEqual(True, computer_move in best_moves)


if __name__ == "__main__":
    unittest.main()