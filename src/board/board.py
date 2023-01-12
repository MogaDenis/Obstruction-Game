import texttable
import copy


class InvalidMoveException(Exception):
    pass


class Board:
    def __init__(self, board_size):
        self._size = board_size
        self._board = self._create_board()

    @property
    def size(self):
        return self._size

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board):
        self._board = new_board

    def _create_board(self):
        """
            This method creates the game board. It is called when the constructor of the class is called. 

        :return: Matrix (N x N)
        """
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(' ')

            board.append(row)

        return board

    def add_indices_to_board(self):
        """
            This method adds to the board indices on the sides in order to help with choosing the desired spot.
        """
        for i, row in enumerate(self.board):
            row.append(i + 1)
        column_indices = []
        for i in range(self.size):
            column_indices.append(i + 1)
        column_indices.append('/')

        self.board.append(column_indices)

    def get_symbol(self, row, col):
        """
            This method returns the symbol of a position inside the board.

        :param row: Integer
        :param col: Integer
        :return: String ('X' or 'O' or '-' or ' ')
        """
        return self._board[row][col]

    def check_if_position_is_in_board(self, row, col):
        """
            This method checks if a position given by its row and column is inside the game board. It return True if thr position is valid or
        False if it is outside the game board. 

        :param row: Integer
        :param col: Integer
        :return: True, if the position is inside the board, False otherwise. 
        """
        if row < 0 or row > (self.size - 1) or col < 0 or col > (self.size - 1):
            return False
        return True

    def check_if_valid_move(self, row, col):
        """
            This method checks if a move can be made by using the previous method. If the method which checks the position returns True, then this 
        method returns None. If the previous method returns False, then this method raises an exception. 

        :param row: Integer
        :param col: Integer
        :raises InvalidMoveException: Exception raised if the move is invalid. 
        """
        # If the move's coordinates are out of the board, raise an exception. 
        if not self.check_if_position_is_in_board(row, col):
            raise InvalidMoveException

        # If the position is already occupied, raise an exception.
        if self.board[row][col] != ' ':
            raise InvalidMoveException

    def block_adjacent_positions(self, row, col):
        """
            This method blocks the adjacent spaces of a position which was occupied. 

        :param row: Integer
        :param col: Integer
        """
        # Given the row and column of a executed move, block the adjacent spaces. 
        # Blocked spaces are marked with '-'. 
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if self.check_if_position_is_in_board(i, j) and (i != row or j != col):
                    self.board[i][j] = '-'

    def make_move(self, row, col, symbol):
        """
            This method checks if a given move can be executed and if so, it makes the move and blocks the adjacent spaces. 

        :param row: Integer
        :param col: Integer
        :param symbol: String
        """
        # Check if the move is possible. 
        self.check_if_valid_move(row, col)

        # If that's the case, make the move. 
        self.board[row][col] = symbol

        # Block the adjacent positions. 
        self.block_adjacent_positions(row, col)

    def undo_move(self, previous_board):
        """
            This method replaces the game board with a previous copy of it. 

        :param previous_board: Previous copy of the game board.
        """
        self.board = copy.deepcopy(previous_board)

    def check_full_board(self):
        """
            This method checks if the game board is full. It returns True if the board is full, False otherwise. 

        :return: True, if the board is full, False if it finds at least an empty space. 
        """
        for row in self.board:
            for position in row:
                if position == ' ':
                    return False
        return True

    def __str__(self):
        table = texttable.Texttable()
        for row in self.board:
            table.add_row(row)

        return table.draw()

    def __repr__(self):
        return self.__str__()