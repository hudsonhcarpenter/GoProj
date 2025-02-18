"""
Fake implementations of GoBase.

We provide a GoStub implementation, and you must
implement a GoFake implementation.
"""
from typing import List, Optional
from copy import deepcopy
from base import GoBase, BoardGridType, ListMovesType

class GoStub(GoBase):
    """
    Stub implementation of GoBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.

    - The board is always initialized with four pieces in the four
      corners of the board. Player 1 has pieces in the northeast and
      southwest corners of the board, and Player 2 has pieces in the
      southeast and northwest corners of the board.
    - Players are allowed to place pieces in any position of the board
      they want, even if there is already a piece in that position
      (placing a piece in such a position replaces the previous piece
      with the new one). The ko and superko rule do not apply.
    - The game ends after four moves. Whatever player has a piece in
      position (0,1) wins. If there is no piece in that position,
      the game ends in a tie.
    - The scores are always reported as 100 for Player 1 and 200 for
      Player 2. Note how the scores do not play a role in determining
      the outcome of the game.
    - It does not validate board positions. If a method is called with
      a position outside the board, the method will likely cause an exception.
    - It does not implement the load_game or simulate_moves method.
    """

    BoardGridType = List[List[Optional[int]]]
    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        if players != 2:
            raise ValueError(
                "The stub implementation only supports two players")

        super().__init__(side, players, superko)

        self._grid = [[None] * side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return self._num_moves == 4

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        return [self._grid[0][1]]

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        r, c = pos
        self._grid[r][c] = self._turn
        self.pass_turn()

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        return {1: 100, 2: 200}

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: Optional[tuple[int, int]]) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        raise NotImplementedError

class GoFake(GoBase):
    """
    GoFake Class, inheriting from GoBase.
    """

    _current_board: BoardGridType
    _past_states: List[BoardGridType] = []

    def __init__(self, side: int, players: int, superko: bool = False):
        super().__init__(side, players, superko)
        self._current_board = [[None] * side for _ in range(side)]
        self._game_over = False
        self._past_states = []
        self._consecutive_passes = 0
        self._turn = 1

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return deepcopy(self._current_board)

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        if self._game_over:
            return []

        moves = []
        for x in range(self._side):
            for y in range(self._side):
                if self._current_board[x][y] is None:
                    moves.append((x,y))
        return moves

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        if self._consecutive_passes >= self._players or \
            self._current_board[0][0] is not None:
            return True
        return False

    @property
    def outcome(self) -> list[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """

        winner: List[int] = []

        if not self._game_over:
            return winner

        for player, count in self.count_pieces().items():
            if count == max(self.count_pieces().values()):
                winner.append(player)

        return winner

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        row, col = pos
        if 0 <= row < self._side and 0 <= col < self._side:
            return self._current_board[row][col]
        raise ValueError

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        if self._game_over:
            return False

        x, y = pos
        if not (0 <= x < self._side and 0 <= y < self._side):
            raise ValueError("Position is outside the bounds of game board")
        if self._superko:
            return self._current_board[x][y] is None and \
                not self.would_violate_ko(pos) and \
                not self.would_violate_superko(pos)

        return self._current_board[x][y] is None and \
            not self.would_violate_ko(pos)

    def would_violate_ko(self, pos: tuple[int, int]) -> bool:
        """
        Determines if placing a stone at the specified position would violate the ko rule.

        Args:
            pos (tuple[int, int]): The position where the player intends to 
            place a stone, specified as a tuple containing the row and 
            column indices (x, y).

        Returns:
            bool: True if making the move at the specified position would 
            violate the ko rule, otherwise False.
        """
        simulated_board = self.simulate_move(pos)

        if len(self._past_states) > 1:
            assert len(self._past_states) >= 2
            if simulated_board.grid == self._past_states[-2]:
                return True
        return False

    def would_violate_superko(self, pos: tuple[int, int]) -> bool:
        """
        Checks if a move would violate the superko rule

        Inputs:
            pos: a position on the board

        Returns: True of the current player placing a piece at pos would violate
            superko, False otherwise
        """
        simulated_board = self.simulate_move(pos)

        for board in self._past_states:
            if board == simulated_board.grid:
                return True
        return False

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """

        x, y = pos
        if not (0 <= x < self._side and 0 <= y < self._side):
            raise ValueError("Position is outside the bounds of game board")

        self._current_board[x][y] = self._turn
        if x == 0 and y == 0:
            for row in range(self._side):
                for col in range(self._side):
                    if self._current_board[row][col] is None:
                        self._current_board[row][col] = self._turn
            return None

        if 0 <= x-1:
            if not self._current_board[x-1][y] == self._turn:
                self._current_board[x-1][y] = None
        if x+1 < self._side:
            if not self._current_board[x+1][y] == self._turn:
                self._current_board[x+1][y] = None
        if 0 <= y-1:
            if not self._current_board[x][y-1] == self._turn:
                self._current_board[x][y-1] = None
        if y+1 < self._side:
            if not self._current_board[x][y+1] == self._turn:
                self._current_board[x][y+1] = None

        self._past_states.append(deepcopy(self._current_board))
        self._consecutive_passes = 0
        self.switch_turn()

    def pass_turn(self) -> None:
        """
        Causes the current player to pass their turn.

        If all players pass consecutively (with no
        moves between the passes), the game will be
        over.

        Returns: Nothing
        """

        self._turn = (self._turn % self._players) + 1
        self._consecutive_passes += 1

        if self._consecutive_passes >= self._players:
            self._game_over = True

    def switch_turn(self) -> None:
        """
        Switch to the next player's turn in a cyclic manner.
        """
        self._turn = (self._turn % self._players) + 1

    def count_pieces(self) -> dict[int,int]:
        """
        Counts the number of pieces each player has on the board

        Returns: a dict containing each player and the number of pieces they 
        have on the board
        """
        piece_count = {player:0 for player in range(1, self._players +1)}

        for row in self._current_board:
            for piece in row:
                if piece is not None and piece in piece_count:
                    piece_count[piece] += 1
                elif piece is not None and piece not in piece_count:
                    piece_count[piece] = 1

        return piece_count

    def scores(self) -> dict[int, int]:
        """
        Computes the current score for each player
        (the number of intersections in their area)

        Returns: Dictionary mapping player numbers to scores
        """
        return self.count_pieces()

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads a new board into the game.

        Note: This will wipe the history of prior board states,
              so violations of the ko rule may not be detected
              after loading a game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        Simulates the effect of making a move,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided move).

        The provided position is not required to be a legal
        move, as this method could be used to check whether
        making a move results in a board that violates the
        ko rule.

        Args:
            pos: Position on the board, or None for a pass

        Raises:
            ValueError: If any of the specified position
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided move.
        """
        simulated_game = deepcopy(self)

        if pos is not None:
            x, y = pos
            if not (0 <= x < simulated_game._side and 0 <= y < simulated_game._side):
                raise ValueError("Position is outside bounds of the board.")
            simulated_game.apply_move(pos)
        else:
            simulated_game.pass_turn()

        return simulated_game