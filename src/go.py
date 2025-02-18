"""
For Go(GoBase)
"""
from base import GoBase, BoardGridType, ListMovesType
from copy import deepcopy

class Board:
    """
    Class for representing a game board
    """
    _size: int #length of a square board
    _board: BoardGridType #represents the board

    def __init__(self, size: int):
        self._size = size
        self._board = [[None] * size for _ in range(size)]

    @property
    def size(self) -> int:
        """
        Length of the square board
        """
        return self._size

    @property
    def board(self) -> BoardGridType:
        """
        Generates board
        """
        return self._board

    def set_piece(self, player: int | None, pos: tuple[int, int]) -> None:
        """
        Inserts a player piece at a specified row and column, or sets a square
        to None

        Inputs:
            player: the player number
            pos: a row and a column on the board

        Raises: ValueError if the desired position is not on the board
        """
        row, col = pos
        row_i, col_i = (row - 1, col - 1)

        try:
            self._board[row_i][col_i] = player
        except ValueError:
            print("Invalid position.")

    def get_player_at(self, pos: tuple[int, int]) -> int | None:
        """
        Returns the player at a given position

        Inputs:
            pos: a row and a column on the board

        Raises: ValueError if the desired position is not on the board
        """
        row, col = pos
        row_i, col_i = (row - 1, col - 1)

        if not 0 <= row_i < self._size or not 0 <= col_i < self._size:
            raise ValueError("Invalid position")

        return self._board[row_i][col_i]

    def valid_pos(self, pos: tuple[int, int]) -> bool:
        """
        Determines if a given posiiton is on the board

        Inputs:
            pos: a given row and column
        
        Returns: True of the given row, column is on the board, False otherwise
        """
        row, col = pos
        return 1 <= row <= self._size and 1 <= col <= self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self._board == other._board

class Go(GoBase):
    """
    This is the Go Class, inheriting from GoBase 
    """
    _board: Board #the game board
    _game_over: bool #holds whether the game is over or not
    _past_states: list[Board] #holds all past states of the game board
    _consecutive_passes: int #the number of consecutive passes
    _turn: int #the current player whose turn it is

    def __init__(self, side: int, players: int, superko: bool = False):
        super().__init__(side, players, superko)
        self._board = Board(side)
        self._game_over = False
        self._past_states = []
        self._consecutive_passes = 0
        self._turn = 1

    @property
    def grid(self) -> BoardGridType:
        return self._board.board

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        if self._game_over:
            return []

        moves = []
        for x in range(1, self._side + 1):
            for y in range(1, self._side + 1):
                if self._board.get_player_at((x,y)) is None:
                    moves.append((x,y))
        return moves

    @property
    def done(self) -> bool:
        if self._consecutive_passes >= self._players:
            return True
        return False

    @property
    def outcome(self) -> list[int]:
        if not self.done:
            return []

        scores = self.scores()
        max_score = max(scores.values())
        winners = [player for player, score in scores.items() if score == max_score]

        return winners

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        if not self._board.valid_pos(pos):
            raise ValueError("Position is outside bounds of board")
        return self._board.get_player_at(pos)

    def legal_move(self, pos: tuple[int, int]) -> bool:
        if not self._board.valid_pos(pos):
            raise ValueError(f"Position {pos} is out of bounds")
        
        if self._game_over:
            return False

        if self._superko:
            return self._board.valid_pos(pos) and \
                self._board.get_player_at(pos) is None and \
                not self.would_violate_superko(pos)

        return self._board.valid_pos(pos) and \
            self._board.get_player_at(pos) is None and \
            not self.would_violate_ko(pos)
        
    def would_violate_ko(self, pos: tuple[int, int]) -> bool:
        """
        Describes whether or not a move violates the ko rule.
        """
        simulated_board = self.simulate_move(pos)

        if len(self._past_states) > 1:
            return simulated_board._board == self._past_states[-2]
        return False

    def would_violate_superko(self, pos: tuple[int, int]) -> bool:
        """
        Describes whether or not a move violates the superko rule.
        """
        simulated_board = self.simulate_move(pos)

        for past_state in self._past_states:
            if simulated_board == past_state:
                return True
        return False

    def apply_move(self, pos: tuple[int, int]) -> None:
        if not self._board.valid_pos(pos):
            raise ValueError("Position is outside the bounds of game board")

        if self.legal_move(pos):
            self._board.set_piece(self._turn, pos)
            self.capture_pieces(pos)
            self._consecutive_passes = 0
            self.switch_turn()

            self._past_states.append(deepcopy(self._board))

    def pass_turn(self) -> None:
        self._turn = (self._turn % self._players) + 1
        self._consecutive_passes += 1

        if self._consecutive_passes >= self._players:
            self._game_over = True

    def scores(self) -> dict[int, int]:
        scores = {player:0 for player in range(1, self._players + 1)}
        for row in range(self._board.size):
            for col in range(self._board.size):
                player = self._board.get_player_at((row + 1, col + 1))
                if player is not None:
                    scores[player] += 1
        for player in range(1, self._players + 1):
            territory = self.calculate_territory(player)
            scores[player] += territory
        return scores

    def load_game(self, turn: int, grid: BoardGridType) -> None:

        self._turn = turn

        for x in range(1, self._board.size +1):
            for y in range(1, self._board.size +1):
                player = grid[x-1][y-1]
                self._board.set_piece(player, (x,y))

        self._game_over = False
        self._consecutive_passes = 0
        self._past_states = [deepcopy(self._board)]

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        simulated_game = deepcopy(self)

        if pos is not None:
            if not simulated_game._board.valid_pos(pos):
                raise ValueError("Position is outside bounds of the board.")

            simulated_game._board.set_piece(simulated_game.turn, pos)
            simulated_game.capture_pieces(pos)
            simulated_game._consecutive_passes = 0
            simulated_game.switch_turn()

            simulated_game._past_states.append(self._board)
        else:
            simulated_game.pass_turn()

        return simulated_game

    def switch_turn(self) -> None:
        """
        Switch to the next player's turn in a cyclic manner.
        """
        self._turn = (self._turn % self._players) + 1

    def adjacent_positions(self, pos: tuple[int,int]) -> ListMovesType:
        """
        Returns the indeces (row, col) of all the squares a adjacent to a 
        given position

        Inputs:
            pos: a given position on the board
        
        Returns: a list of all the adjacent square posiitons, an empty list if 
            the input position is not valid
        """
        row, col = pos
        surrounding = [(row - 1, col), (row, col + 1),
                       (row + 1, col), (row, col - 1)]
        adjacent = []

        for square in surrounding:
            if self._board.valid_pos(square):
                adjacent.append(square)

        return adjacent

    def connection(self, pos: tuple[int,int]) -> ListMovesType | None:
        """
        Returns a list of all the square posiitons (row, col) in a connected
        block at a given position

        Inputs:
            pos: a board position (row, col)

        Returns: a list of all the square positions that comprise of block of
            the same player's pieces at pos, None if there is not a piece at pos
        """
        player = self._board.get_player_at(pos)
        group = []
        queue = []
        queue.append(pos)

        while queue:
            square = queue.pop()
            group.append(square)
            for adjacent in self.adjacent_positions(square):
                if not adjacent in group and \
                    self._board.get_player_at(adjacent) == player:
                    queue.append(adjacent)
        return group

    def reset_squares(self, squares: ListMovesType):
        """
        Removes all the pieces in a given a list of squares

        Inputs:
            squares: a list of squares on the board (row, col)
        """
        for square in squares:
            if self._board.valid_pos(square):
                self._board.set_piece(None, square)

    def is_surrounded_block(self, block: ListMovesType) -> bool:
        """
        Determines if a block of a player's pieces are surrounded by other
        players' pieces (has no liberties)

        Inputs:
            block: a list of square positions that comprise a block

        Returns: True if the block has no liberties, False otherwise
        """
        if block is not None:
            for square in block:
                for adjacent in self.adjacent_positions(square):
                    if self._board.get_player_at(adjacent) is None:
                        return False
        return True

    def capture_pieces(self, pos: tuple[int, int]) -> None:
        """
        Removes all pieces/blocks that are surrounded once a move is played

        Inputs:
            pos: the position at which the most recent move was played
        """
        check_squares = [square for square in self.adjacent_positions(pos)] + [pos]

        for square in check_squares:
            block = self.connection(square)
            if block is not None and self.is_surrounded_block(block):
                self.reset_squares(block)

    def calculate_territory(self, player: int) -> int:
        """
        Calculates the amount of empty board positions within a given \
        player's territory

        Input:
            player: the integer value assigned to a player

        Returns:
            int: number of empty board positions within the players territory
        """
        count = 0
        # iterate through the board
        for row in range(1, self._side + 1):
            for col in range(1, self._side + 1):
                square = self._board.get_player_at((row,col))
                # find empty, unvisited squares
                if square is None and (row, col):
                    # bfs
                    visited = set()
                    queue = [(row, col)]
                    territory = []
                    while queue:
                        c_square = queue.pop()
                        visited.add(c_square)
                        territory.append(c_square)
                        for adjacent in self.adjacent_positions(c_square):
                            if adjacent in visited:
                                continue
                            if self._board.get_player_at(adjacent) is None:
                                queue.append(adjacent)
                            # this is not player's territory, terminate search
                            elif self._board.get_player_at(adjacent) != player:
                                queue = []
                                territory = []
                                visited = set()
                                break

                    count += len(territory)

        return count
    