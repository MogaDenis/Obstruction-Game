import random
import copy


class AI:
    def __init__(self, board_service):
        self._board_service = board_service

    def search_valid_positions(self):
        """
            This method searches inside the the board all the possible moves the computer can make and associates to each of them
        the number of adjacent spaces it blocks.

        :return: Dicitionary having as keys positions and as values the number of spaces blocked by each move.
        """
        valid_positions = {}
        for i in range(self._board_service.get_board_size()):
            for j in range(self._board_service.get_board_size()):
                # If the position is empty, it means a move there is valid. 
                if self._board_service.get_symbol(i, j) == ' ':
                    valid_positions[(i, j)] = self.calculate_num_of_positions_blocked(i, j)

        return valid_positions

    def calculate_num_of_positions_blocked(self, row, col):
        """
            This method calculates and returns the number of adjacent positions blocked by a given move. 

        :param row: Integer
        :param col: Integer
        :return: Integer
        """
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # If a position inside the board is empty and is not the one in which the move is made, then it is counted. 
                if self._board_service.check_if_position_is_in_board(i, j) and (i != row or j != col) and self._board_service.get_symbol(i, j) == ' ':
                    count += 1

        return count

    def find_best_moves(self, valid_positions):
        """
            This method chooses and returns the moves from a list of valid moves which block the highest number of adjacent spaces. 

        :param valid_positions: Dicitionary having as keys positions and as values the number of spaces blocked by each move.
        :return: List of the moves which block the largest number of spaces. 
        """
        max_profit = 0
        best_moves = []

        for position in valid_positions:
            if valid_positions[position] > max_profit:
                max_profit = valid_positions[position]
                best_moves = [position]
            elif valid_positions[position] == max_profit:
                best_moves.append(position)

        return best_moves, max_profit

    def find_average_moves(self, valid_positions, max_profit):
        """
            This method works similarly to the one which searches for the best moves, only difference is that this one finds the best 
        set of moves worse than the best ones found previously. 

        :param valid_positions: Dicitionary having as keys positions and as values the number of spaces blocked by each move.
        :param max_profit: The maximum number of positions blocked by a previous set of moves. 
        :return: List of the moves which block the largest number of spaces, less than a given maximum.
        """
        average_profit = 0
        average_moves = []

        for position in valid_positions:
            if valid_positions[position] > average_profit and valid_positions[position] < max_profit:
                average_profit = valid_positions[position]
                average_moves = [position]
            elif valid_positions[position] == average_profit:
                average_moves.append(position)

        return average_moves, average_profit

    def computer_move(self, first_move=False):
        """
            This method executes the best computer move possible by choosing the one which blocks the highest number of adjacent positions. 
            It also takes into account the situations when the user is one move away from winning. In this case, the computer looks for a move
        which will stop the player from winning, even though it is not the one which blocks the highest number of spaces. 
        """
        
        if first_move:
            valid_positions = self.search_valid_positions()

            list_of_positions = []
            for position in valid_positions:
                list_of_positions.append(position)

            random_position_move = random.choice(list_of_positions)
            random_row, random_col = random_position_move

            self._board_service.make_move(random_row, random_col, 'O')

        else:

            # Figure out the valid moves and select those who are the best. 
            valid_positions = self.search_valid_positions()
            best_moves, max_profit = self.find_best_moves(valid_positions)

            # Randomly choose between the best moves, if there are more than one. 
            row, col = random.choice(best_moves)

            first_game_board_copy = copy.deepcopy(self._board_service.get_board())

            # Make the move.
            self._board_service.make_move(row, col, 'O')

            second_game_board_copy = copy.deepcopy(self._board_service.get_board())

            # Make the move, then pretend the user will choose the best move possible.
            # Check if the game is finished, if so, it means that the computer should not choose the "best move", but instead an average one
            # will be better. 

            user_valid_positions = self.search_valid_positions()
            best_user_moves, max_user_profit = self.find_best_moves(user_valid_positions)

            if len(best_user_moves) > 0:
                row, col = random.choice(best_user_moves)

                # Make a move from the player's perspective. 
                self._board_service.make_move(row, col, 'X')

                # Now, let's check if the board is full. 
                if self._board_service.check_if_game_over():
                    # This means that the user is about to win the game. 
                    # The computer must try to prevent this. 
                    # We have to search for the "average case" move. 
                    
                    # Revert back to the initial board. 
                    self._board_service.undo_move(first_game_board_copy)

                    # Find an average set of moves, the best moves worse than the max profit moves before. 
                    average_moves, average_profit = self.find_average_moves(valid_positions, max_profit)

                    if len(average_moves) > 0:
                        # Make a copy of the board since we will try each move and see which one works the best.
                        initial_board = copy.deepcopy(self._board_service.get_board())
                        optimal_average_move = None

                        for move in average_moves:
                            # Reset the board. 
                            self._board_service.undo_move(initial_board)

                            # Make a move from the list. 
                            self._board_service.make_move(move[0], move[1], 'O')

                            # Search for the user's valid moves. 
                            user_valid_positions = self.search_valid_positions()
                            best_user_moves, max_user_profit = self.find_best_moves(user_valid_positions)

                            if len(best_user_moves) > 0:
                                # Execute the user's best move, if it is the only one, then it should be a winning move. 
                                row, col = random.choice(best_user_moves)
                                self._board_service.make_move(row, col, 'X')

                                # If the game is not won by the user executing that previous move, then the computer's move is a good one. 
                                if not self._board_service.check_if_game_over():
                                    optimal_average_move = move
                                    break
                        
                        if optimal_average_move is None:
                            # Choose randomly one of them if there is no move that stops the player from winning. 
                            row, col = random.choice(average_moves)
                        else:
                            # Save the move that prevents the player from winning straight away. 
                            row, col = optimal_average_move

                        # Go back to the initial board. 
                        self._board_service.undo_move(initial_board)

                        # Make a copy before doing the move. 
                        third_game_board_copy = copy.deepcopy(self._board_service.get_board())

                        # Make the optimal or the random average move. 
                        self._board_service.make_move(row, col, 'O')

                        # Make a copy of the board also after the move. 
                        fourth_game_board_copy = copy.deepcopy(self._board_service.get_board())

                        # Search through the user's valid moves. 
                        user_valid_positions = self.search_valid_positions()
                        best_user_moves, max_user_profit = self.find_best_moves(user_valid_positions)

                        # If the user can still make moves, check if he is in game winning situation after the computer's move. 
                        if len(best_user_moves) > 0:
                            # Execute the user's best move. 
                            row, col = random.choice(best_user_moves)

                            self._board_service.make_move(row, col, 'X')

                            # Check if it is a game winning move. 
                            if self._board_service.check_if_game_over():
                                # If that is the case, revert back to the third board. 
                                self._board_service.undo_move(third_game_board_copy)
                                
                                # Search for "worse" moves.
                                worst_moves, worst_profit = self.find_average_moves(valid_positions, average_profit)

                                if len(worst_moves) > 0:
                                    # Execute that move instead, this way the user shouldn't be able to win by a single move. 
                                    row, col = random.choice(worst_moves)

                                    self._board_service.make_move(row, col, 'O')

                                else:
                                    self._board_service.undo_move(fourth_game_board_copy)
                            else:
                                # Revert back to the move made by the computer if the user can't win the game yet. 
                                self._board_service.undo_move(fourth_game_board_copy)

                    else:
                        self._board_service.undo_move(second_game_board_copy)
            
                else:
                    # Revert back to the move made by the computer if the user can't win the game yet. 
                    self._board_service.undo_move(second_game_board_copy)
        
