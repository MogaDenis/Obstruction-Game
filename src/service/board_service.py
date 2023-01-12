class BoardService:
    def __init__(self, board):
        self._board = board

    def add_indices_to_board(self):
        """
            This method calls the method from the Board class which adds indices to the game board. 
        """
        self._board.add_indices_to_board()

    def undo_move(self, previous_board):
        """
            This method calls the method from the Board class which undoes a move by replacing the current game board with a copy
        of a previous version of it. 

        :param previous_board: Copy of a previous board.
        """
        self._board.undo_move(previous_board)

    def make_move(self, row, col, symbol):
        """
            This method calls the method from the Board class which makes a move into a given position on the board. 

        :param row: Integer
        :param col: Integer
        :param symbol: String
        """
        self._board.make_move(row, col, symbol)

    def get_symbol(self, row, col):
        """
            This method calls the method from the Board class which returns the symbol from a given position inside the board.

        :param row: Integer
        :param col: Integer
        :return: String
        """
        return self._board.get_symbol(row, col)

    def check_if_game_over(self):
        """
            This method calls the method from the Board class which checks if the game board is full. If the game board is full, the game is
        over so this returns True in this case, and False otherwise. 

        :return: True, if the game is over, False otherwise. 
        """
        return self._board.check_full_board()

    def check_if_position_is_in_board(self, row, col):
        """
            This method calls the method from the Board class which checks if a given position is inside the board. 

        :param row: Integer
        :param col: Integer
        :return: True, if the position is valid, False otherwise.
        """
        return self._board.check_if_position_is_in_board(row, col)

    def get_board_size(self):
        """
            This method returns the size of the game board. 

        :return: Integer
        """
        return self._board.size

    def get_board(self):
        """
            This method returns the game board.

        :return: Matrix (N x N)
        """
        return self._board.board