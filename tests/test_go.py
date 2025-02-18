import pytest

from go import Go
from base import GoBase
from fakes import GoFake


@pytest.mark.parametrize("size", list(range(4,20)))
def test_constructing_go_game(size: int) -> None:
    """Test initializing boards of various sizes."""
    game = Go(side=size, players=2)
    assert game.size == size, f"Expected board size to be {size}"
    assert game.num_players == 2, "Expected number of players to be 2"
    assert game.turn == 1, "Expected first turn to be player 1"

    expected_empty_board = [[None] * size for _ in range(size)]
    assert game.grid == expected_empty_board, "Expected the game board to be initially empty"


@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_9x9_game_properties(players_count: int) -> None:
    """Test properties of a 9x9 Go Game"""
    game = Go(side=9, players=players_count)
    assert game.size == 9, "Expected board size to be 9"
    assert game.num_players == players_count, "Expected number of players to be 2"
    assert game.turn == 1, "Expected the first turn to be player 1"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_9x9_piece_at(players_count: int) -> None:
    game = Go(side=9, players=players_count)
    move = (1,1)
    
    assert game.piece_at(move) is None, "Expected no piece at (1, 1) initially"
    game.apply_move(move)
    assert game.piece_at(move) == 1, "Expected player 1's piece at (1, 1) after move"
    
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_9x9_legal_move(players_count: int) -> None:
    game = Go(side=9, players=players_count)
    move = (1,1)
    
    assert game.legal_move(move) is True, "Expected (1, 1) to be a legal move initially"
    game.apply_move(move)

    assert game.legal_move(move) is False, "Expected (1,1) to no longer be a legal move"

    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_9x9_available_moves(players_count: int) -> None:
    game = Go(side=9, players=players_count)
    move = (1,1)
    
    initial_moves = {(x, y) for x in range(1, 10) for y in range(1, 10)}
    assert set(game.available_moves) == initial_moves, "Expected all positions to be available moves initially"
    
    game.apply_move(move)
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

    updated_moves = initial_moves - {move}
    assert set(game.available_moves) == updated_moves, "Move (1, 1) should no longer be available"

    assert isinstance(game.available_moves, list), "Expected available_moves to return a list"


@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_13x13_game_properties(players_count: int) -> None:
    """Test properties of a 13x13 Go Game"""
    game = Go(side=13, players=players_count)
    assert game.size == 13, "Expected board size to be 9"
    assert game.num_players == players_count, "Expected number of players to be 2"
    assert game.turn == 1, "Expected the first turn to be player 1"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_13x13_piece_at(players_count: int) -> None:
    game = Go(side=13, players=players_count)
    move = (1,1)

    assert game.piece_at(move) is None, "Expected no piece at (1, 1) initially"
    game.apply_move(move)
    assert game.piece_at(move) == 1, "Expected player 1's piece at (1, 1) after move"
    
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_13x13_legal_move(players_count: int) -> None:
    game = Go(side=13, players=players_count)
    move = (1,1)
    
    assert game.legal_move(move) is True, "Expected (1, 1) to be a legal move initially"
    game.apply_move(move)

    assert game.legal_move(move) is False, "Expected (1,1) to no longer be a legal move"

    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_13x13_available_moves(players_count: int) -> None:
    game = Go(side=13, players=players_count)
    move = (1,1)
    
    initial_moves = {(x, y) for x in range(1, 14) for y in range(1, 14)}
    assert set(game.available_moves) == initial_moves, "Expected all positions to be available moves initially"
    
    game.apply_move(move)
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

    updated_moves = initial_moves - {move}
    assert set(game.available_moves) == updated_moves, "Move (1, 1) should no longer be available"

    assert isinstance(game.available_moves, list), "Expected available_moves to return a list"


@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_19x19_game_properties(players_count: int) -> None:
    """Test properties of a 13x13 Go Game"""
    game = Go(side=19, players=players_count)
    assert game.size == 19, "Expected board size to be 9"
    assert game.num_players == players_count, "Expected number of players to be 2"
    assert game.turn == 1, "Expected the first turn to be player 1"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_19x19_piece_at(players_count: int) -> None:
    game = Go(side=19, players=players_count)
    move = (1,1)

    assert game.piece_at(move) is None, "Expected no piece at (1, 1) initially"
    game.apply_move(move)
    assert game.piece_at(move) == 1, "Expected player 1's piece at (1, 1) after move"
    
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_19x19_legal_move(players_count: int) -> None:
    game = Go(side=19, players=players_count)
    move = (1,1)
    
    assert game.legal_move(move) is True, "Expected (1, 1) to be a legal move initially"
    game.apply_move(move)

    assert game.legal_move(move) is False, "Expected (1,1) to no longer be a legal move"

    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

@pytest.mark.parametrize("players_count", list(range(2,11))) #random number of players up to 10
def test_19x19_available_moves(players_count: int) -> None:
    game = Go(side=19, players=players_count)
    move = (1,1)
    
    initial_moves = {(x, y) for x in range(1, 20) for y in range(1, 20)}
    assert set(game.available_moves) == initial_moves, "Expected all positions to be available moves initially"
    
    game.apply_move(move)
    expected_next_turn = 2 if players_count > 1 else 1
    assert game.turn == expected_next_turn, f"Expected turn to be player {expected_next_turn} after a move"

    updated_moves = initial_moves - {move}
    assert set(game.available_moves) == updated_moves, "Move (1, 1) should no longer be available"

    assert isinstance(game.available_moves, list), "Expected available_moves to return a list"


@pytest.fixture
def game_19x19() -> Go:
    """Fixture to create a 19x19 Go game with two players."""
    return Go(side=19, players=2)

def test_initial_state(game_19x19: Go) -> None:
    """Test initial state of a 19x19 Go game just as a reference."""
    assert game_19x19.size == 19
    assert game_19x19.num_players == 2
    assert game_19x19.turn == 1
    assert len(game_19x19.available_moves) == 19 * 19
    assert game_19x19.done is False
    assert game_19x19.outcome == []

def test_legal_move_and_available_moves(game_19x19: Go) -> None:
    """Test that verifies legal_move and available_moves and checks they work
    for any position in the board."""
    all_positions = [(x, y) for x in range(1, 20) for y in range(1, 20)]
    for position in all_positions:
        assert game_19x19.legal_move(position), f"Move should be legal at {position}"
    
    available_moves = game_19x19.available_moves
    assert len(available_moves) == 19*19, "Should have 361 available moves initially"
    for position in all_positions:
        assert position in available_moves, f"Position {position} should be an available move"

def test_legal_move_and_placement(game_19x19: Go) -> None:
    """Test placing a piece on the board and verifying a piece is placed
    correctly at the specified position and that the turn is correctly updated
    after each move."""
    initial_move_1 = (1, 1)
    initial_move_2 = (2, 1)
    assert game_19x19.legal_move(initial_move_1) is True
    assert game_19x19.legal_move(initial_move_2) is True
    
    game_19x19.apply_move(initial_move_1)
    assert game_19x19.piece_at(initial_move_1) == 1
    assert game_19x19.turn == 2
    
    game_19x19.apply_move(initial_move_2)
    assert game_19x19.piece_at(initial_move_2) == 2
    assert game_19x19.turn == 1
    
    assert initial_move_1 and initial_move_2 not in game_19x19.available_moves

def test_move_makes_position_illegal(game_19x19: Go) -> None:
    """Tests that after making a move on the board, the position of that move
    is no longer considered a legal move."""
    move_position = (1, 1)
    game_19x19.apply_move(move_position)
    assert not game_19x19.legal_move(move_position), "The position of the made move should no longer be legal"

def test_move_then_pass_updates_turn(game_19x19: Go) -> None:
    """Test that after making a move and then passing, the turn is updated 
    correctly."""
    initial_move_position = (1, 1)  #The position where Player 1 will make their move

    game_19x19.apply_move(initial_move_position)
    game_19x19.pass_turn()  #Player 2 passes their turn

    assert game_19x19.turn == 1, "After Player 1 makes a move and then P2 passes, it should be Player 1's turn"

def test_game_ends_after_consecutive_passes(game_19x19: Go) -> None:
    """Test passing turns updates the game state correctly."""
    game_19x19.apply_move((1,1))   #Player 1 makes a move

    game_19x19.pass_turn() #Player 2 passes their turn
    assert game_19x19.turn == 1
    
    game_19x19.pass_turn() #Player 1 passes their turn
    assert game_19x19.turn == 2

    assert game_19x19.done, "The game should be done after both players pass turns consecutively"

def test_single_piece_capture(game_19x19: Go) -> None:
    """Test capturing a single piece on a 19x19 board. Verifies that the game
    logic correctly captures a piece when it is fully surrounded by the opponent's
    piece."""
    game_state_before_capture = [[None] * 19 for _ in range(1, 20)]

    game_state_before_capture[9][9] = 1 
    game_state_before_capture[9][11] = 1
    game_state_before_capture[10][8] = 1
    game_state_before_capture[8][8] = 1
    
    game_state_before_capture[9][8] = 2 
    game_state_before_capture[9][10] = 2
    game_state_before_capture[10][9] = 2
    
    game_19x19.load_game(turn=2, grid=game_state_before_capture)  # It's Player 2's turn
    
    game_19x19.apply_move((9, 10))  # Player 2 captures (10, 10)

    assert game_19x19.piece_at((10, 10)) is None, "The piece at (10, 10) should have been captured"
    assert game_19x19.turn == 1, "It should be Player 1's turn after Player 2 captures a piece"

def test_multiple_piece_capture(game_19x19: Go) -> None:
    """Test capturing multiple pieces on a 19x19 board. Verifies that the game
    logic correctly captures a set of piece when it is fully surrounded by the 
    opponent's piece."""
    game_state_before_capture = [[None] * 19 for _ in range(1, 20)]

    game_state_before_capture[9][9] = 1
    game_state_before_capture[9][10] = 1
    game_state_before_capture[11][9] = 1
    game_state_before_capture[11][10] = 1
    game_state_before_capture[10][11] = 1

    game_state_before_capture[10][9] = 2
    game_state_before_capture[10][10] = 2
    game_state_before_capture[9][11] = 2
    game_state_before_capture[8][10] = 2
    game_state_before_capture[8][18] = 2

    game_19x19.load_game(turn=1, grid=game_state_before_capture)
    game_19x19.apply_move((11, 9))  # Player 1 captures (10, 10) and (10, 11)

    assert game_19x19.piece_at((11, 10)) is None, "The piece at (10, 10) should have been captured"
    assert game_19x19.piece_at((11, 11)) is None, "The piece at (10, 11) should have been captured"

    assert game_19x19.turn == 2, "It should be Player 1's turn after Player 2 captures a piece"

def test_ko_rule_violation(game_19x19: Go) -> None:
    """Test the enforcement of the ko rule for a series of moves."""
    game_state_before_ko = [[None] * 19 for _ in range(1, 20)]

    game_state_before_ko[1][1] = 1
    game_state_before_ko[0][2] = 1
    game_state_before_ko[2][2] = 1
    game_state_before_ko[1][3] = 1
    
    game_state_before_ko[1][4] = 2
    game_state_before_ko[0][3] = 2
    game_state_before_ko[2][3] = 2
    
    game_19x19.load_game(turn=2, grid=game_state_before_ko)
    
    game_19x19.apply_move((2, 3))
    assert game_19x19.piece_at((2, 4)) is None, "The piece at (2, 4) should have been captured"

    # Player 1 attempts to recapture at (2, 3), which would violate the ko rule
    is_legal = game_19x19.legal_move((2, 4))
    assert not is_legal, "The move at (2, 4) should be illegal due to the ko rule"

def test_superko_rule_violation(game_19x19: Go) -> None:
    """Test the enforcement of the superko rule for a series of moves."""
    game_state_before_superko = [[None] * 19 for _ in range(1, 20)]

    game_state_before_superko[1][1] = 1
    game_state_before_superko[2][2] = 1
    game_state_before_superko[0][2] = 1
    game_state_before_superko[1][3] = 1
    game_state_before_superko[6][7] = 1
    game_state_before_superko[5][8] = 1
    game_state_before_superko[4][7] = 1
    game_state_before_superko[9][9] = 1
    game_state_before_superko[10][10] = 1
    game_state_before_superko[8][10] = 1
    game_state_before_superko[9][11] = 1

    game_state_before_superko[2][3] = 2
    game_state_before_superko[1][4] = 2
    game_state_before_superko[0][3] = 2
    game_state_before_superko[5][5] = 2
    game_state_before_superko[6][6] = 2
    game_state_before_superko[4][6] = 2
    game_state_before_superko[5][7] = 2
    game_state_before_superko[10][11] = 2
    game_state_before_superko[9][12] = 2
    game_state_before_superko[8][11] = 2
    
    # this is the game state of board to be compared with after captures.
    
    game_19x19.load_game(turn=2, grid=game_state_before_superko)

    game_19x19.apply_move((2, 3))  # Player 2
    assert game_19x19.piece_at((2, 4)) is None, "The piece at (2, 4) should have been captured"

    game_19x19.apply_move((6,7))   # Player 1
    assert game_19x19.piece_at((6, 8)) is None, "The piece at (6, 8) should have been captured"
    
    game_19x19.apply_move((10,11))   # Player 2
    assert game_19x19.piece_at((10, 12)) is None, "The piece at (10, 12) should have been captured"

    game_19x19.apply_move((2,4))   # Player 1
    assert game_19x19.piece_at((2, 3)) is None, "The piece at (2, 3) should have been captured"

    game_19x19.apply_move((6,8))   # Player 1
    assert game_19x19.piece_at((6, 7)) is None, "The piece at (6, 7) should have been captured"

    game_19x19.apply_move((10,12))   # Player 1
    assert game_19x19.piece_at((10, 11)) is None, "The piece at (10, 11) should have been captured"

    # Player 1 attempts to recapture at (2, 3), which would violate the ko rule
    is_legal = game_19x19.legal_move((10, 11))
    assert not is_legal, "The move at (10, 11) should be illegal due to superko, preventing past board states"

def test_scoring_without_territories(game_19x19: Go) -> None:
    """Test the scoring in a scenario where no territories are created."""
    game_state = [[None] * 19 for _ in range(1, 20)]
    
    game_state[2][2] = 1
    game_state[15][15] = 2
    game_state[3][3] = 1 
    game_state[15][16] = 2
    game_state[4][4] = 1
    game_state[16][15] = 2
    game_state[7][7] = 1

    game_19x19.load_game(turn=2, grid=game_state)

    # Assuming 4 stones placed by P1, 3 by P2, with no enclosed territories
    expected_scores = {1: 4, 2: 3}
    actual_scores = game_19x19.scores()
    assert actual_scores == expected_scores, f"Expected scores to be {expected_scores}, but got {actual_scores}"

def test_scoring_with_territories(game_19x19: Go) -> None:
    """Test the scoring in a scenarior where territories are created."""
    game_state = [[None] * 19 for _ in range(1, 20)]

    game_state[2][2] = 1
    game_state[15][15] = 2
    game_state[2][4] = 1
    game_state[15][17] = 2
    game_state[3][3] = 1
    game_state[16][16] = 2
    game_state[1][3] = 1  # Player 1 at (2, 4), completes a territory

    # Additional moves that do not create new territories
    game_state[9][9] = 2
    game_state[9][10] = 1
    game_state[10][9] = 2

    game_19x19.load_game(turn=1, grid=game_state)

    expected_scores = {1: 5 + 1, 2: 5}  # Player 1's stones + territory vs Player 2's stones
    actual_scores = game_19x19.scores()
    assert actual_scores == expected_scores, f"Expected scores to be {expected_scores}, but got {actual_scores}"
    #Player 1 should be leading 6:5 after these moves due to territory creation

def test_outcome_after_scoring_without_territories(game_19x19: Go) -> None:
    """Test the scoring in a scenario where no territories are created."""
    game_state = [[None] * 19 for _ in range(1, 20)]

    game_state[2][2] = 1
    game_state[15][15] = 2
    game_state[3][3] = 1 
    game_state[15][16] = 2 
    game_state[4][4] = 1 
    game_state[16][15] = 2 
    game_state[7][7] = 1 

    game_19x19.load_game(turn=2, grid=game_state)

    # Assuming 4 stones placed by P1, 3 by P2, with no enclosed territories
    game_19x19.pass_turn()  # Player 2 passes
    game_19x19.pass_turn()  # Player 1 passes
    
    expected_scores = {1: 4, 2: 3}
    actual_scores = game_19x19.scores()
    outcome = game_19x19.outcome
    assert actual_scores == expected_scores, f"Expected scores to be {expected_scores}, but got {actual_scores}"
    
    winning_player = max(expected_scores, key=expected_scores.get)
    assert outcome == [winning_player], f"Expected the winning player to be {winning_player}, but got {outcome}"

def test_outcome_after_scoring_with_territories(game_19x19: Go) -> None:
    """Test the scoring in a scenarior where territories are created."""
    game_state = [[None] * 19 for _ in range(1, 20)]
        
    game_state[2][2] = 1
    game_state[15][15] = 2 
    game_state[2][4] = 1 
    game_state[15][17] = 2
    game_state[3][3] = 1 
    game_state[16][16] = 2  
    game_state[1][3] = 1  
    # More moves without creating new territories
    game_state[9][9] = 2
    game_state[9][10] = 1
    game_state[10][9] = 2

    # Load the game state right before passing turns
    game_19x19.load_game(turn=1, grid=game_state)

    game_19x19.pass_turn()  # Player 1 passes
    game_19x19.pass_turn()  # Player 2 passes

    expected_scores = {1: 5 + 1, 2: 5}  # Player 1's stones + territory vs Player 2's stones
    actual_scores = game_19x19.scores()
    outcome = game_19x19.outcome
    assert actual_scores == expected_scores, f"Expected scores to be {expected_scores}, but got {actual_scores}"

    winning_player = max(expected_scores, key=expected_scores.get)
    assert outcome == [winning_player], f"Expected the winning player to be {winning_player}, but got {outcome}"
    #Player 1 should win 6:5, outcome should return [1]


@pytest.fixture
def game_19x19_three_players() -> Go:
    """Fixture to create a standard 19x19 Go game with three players."""
    return Go(side=19, players=3)

def test_three_player_moves_and_turns(game_19x19_three_players: Go) -> None:
    """Test placing stones and turn rotation in a 19x19 Go game with three players."""
    game_19x19_three_players.apply_move((3, 3))
    assert game_19x19_three_players.piece_at((3, 3)) == 1, "Expected Player 1's stone at (3, 3)"
    assert game_19x19_three_players.turn == 2, "Expected next turn to be Player 2"

    # Player 2 places a stone
    game_19x19_three_players.apply_move((16, 16))
    assert game_19x19_three_players.piece_at((16, 16)) == 2, "Expected Player 2's stone at (16, 16)"
    assert game_19x19_three_players.turn == 3, "Expected next turn to be Player 3"

    # Player 3 places a stone
    game_19x19_three_players.apply_move((4, 4))
    assert game_19x19_three_players.piece_at((4, 4)) == 3, "Expected Player 3's stone at (4, 4)"
    assert game_19x19_three_players.turn == 1, "Expected next turn to be Player 1"

def test_move_then_pass_three_times_ends_game(game_19x19_three_players: Go) -> None:
    """Test examining that after a move and three passes that the game should
    end."""
    game_19x19_three_players.apply_move((10, 10)) # Player 1 makes a move
    assert game_19x19_three_players.turn == 2, "Expected next turn to be Player 2"

    # Players 1, 2, and 3 pass in sequence
    game_19x19_three_players.pass_turn() # Player 2 passes
    game_19x19_three_players.pass_turn() # Player 3 passes
    game_19x19_three_players.pass_turn() # Player 1 passes

    assert game_19x19_three_players.done, "The game should end after all players have passed."


def test_grid_1_Go() -> None:
    """Check that grid for an empty game is exported correctly"""

    go = Go(19, 2)

    grid = go.grid

    for row in range(go.size):
        for col in range(go.size):
            assert grid[row][col] is None

def test_grid_2_Go() -> None:
    """
    Check that grid returns a deep copy of the board's grid,
    and that modifying grid's return value doesn't modify
    the game's board
    """

    go = Go(19, 2)

    grid = go.grid

    grid[5][5] = 1

    assert go.piece_at((5, 5)) is None, (
        "grid() returned a shallow copy of the game's board. "
        "Modifying the return value of grid() should not "
        "affect the game's board."
    )

def test_grid_3_Go() -> None:
    """
    Check that grid returns a correct copy of the board after making
    a few moves (none of the moves will result in a capture)
    """

    game_state = [[None] * 19 for _ in range(1, 20)]
    
    moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 1),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 1),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (12, 2),
    ]

    player_number = 1
    for move in moves:
        x, y = move
        game_state[x-1][y-1] = player_number
        player_number = 2 if player_number == 1 else 1  # Switch between Player 1 and 2

    go = Go(19, 2)

    go.load_game(turn=player_number, grid=game_state)

    grid = go.grid
    for row in range(1, go.size + 1):
        for col in range(1, go.size + 1):
            assert grid[row - 1][col - 1] == go.piece_at((row, col))

def test_simulate_move_1() -> None:
    """
    Test that simulating a move creates a new game
    """

    go = Go(19, 2)

    new_go = go.simulate_move((5, 5))

    # Check that the original Go object has not been modified
    assert go.piece_at((5, 5)) is None
    assert go.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 5)) == 1
    assert new_go.turn == 2


def test_simulate_move_2() -> None:
    """
    After making a few moves, check that simulating a move
    correctly creates a new game.
    """
    initial_moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 1),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 1),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (13, 2),
    ]

    go = Go(19, 2)

    for move in initial_moves:
        go.apply_move(move)

    new_go = go.simulate_move((5, 5))

    # Check that the original Go object has not been modified
    assert go.piece_at((5, 5)) is None
    for move in initial_moves:
        assert go.piece_at(move) is not None
    assert go.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 5)) == 1
    for move in initial_moves:
        assert new_go.piece_at(move) is not None
    assert new_go.turn == 2

def test_simulate_move_3() -> None:
    """
    We place one piece in position (5, 6) and then
    simulate placing a piece in position (5, 7).
    The piece in position (5, 6) should be captured
    (but only in the new game created by simulate_move)
    """
    go = Go(19, 2)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    new_go = go.simulate_move((5, 7))

    # Check that the original Go object has not been modified
    assert go.piece_at((5, 6)) == 1
    assert go.piece_at((5, 7)) is None
    assert go.turn == 2

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 6)) is 1
    assert new_go.piece_at((5, 7)) == 2
    assert new_go.turn == 1

def test_simulate_move_4() -> None:
    """
    Check that simulating a pass works correctly.
    """
    go = Go(19, 2)

    new_go = go.simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1

    # Check that the pass was applied in the new Go object
    assert new_go.turn == 2

def test_simulate_move_5() -> None:
    """
    Check that simulating two consecutive passes works correctly.
    """
    go = Go(19, 2)

    new_go = go.simulate_move(None).simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1
    assert not go.done

    # Check that the passes were applied in the new Go object
    assert new_go.done


def test_apply_move_and_verify_state() -> None:
    """Test applying a move and verifying the game state."""
    game = Go(side=19, players=2)
    game.apply_move((3, 3))
    assert game.piece_at((3, 3)) == 1, "Expected player 1's piece at (3, 3)"
    assert game.turn == 2, "Expected next turn to be player 2"
    assert not game.done, "Expected game to be in progress"
    assert game.outcome == [], "Expected no outcome yet"


def test_game_end_by_passing() -> None:
    """Test ending a game by passing."""
    game = Go(side=19, players=2)

    board_state = [[None] * 19 for _ in range(1, 20)]
    board_state[15][15] = 1
    board_state[15][16] = 2

    game.load_game(turn=1, grid=board_state)
    game.pass_turn()
    game.pass_turn()  # Player 2 passes, ending the game
    
    assert game.done, "Expected game to be done after both players pass consecutively"
    assert game.outcome != [], "Expected an outcome at the end of the game"

def test_capture_of_large_group() -> None:
    """Test the capture of 10 or more pieces in one move using load_game."""
    game = Go(side=19, players=2)

    board_state = [[None] * 19 for _ in range(1, 20)]
    
    for x in range(4, 15):
        board_state[10][x] = 1 
    for x in range(4, 15):
        board_state[11][x] = 1 

    # Surrounding player 1's group with player 2's stones, except for one liberty
    for x in range(4, 15):
        board_state[9][x] = 2
        board_state[12][x] = 2
    for y in range(10, 12):
        board_state[y][15] = 2
    for y in range(10, 11):
        board_state[y][3] = 2

    game.load_game(turn=2, grid=board_state)
    game.apply_move((12, 4))
    
    for x in range(5, 14):
        assert game.piece_at((11, x)) is None, f"Expected the piece at (12, {x}) to be captured"
    for x in range(5, 14):
        assert game.piece_at((12, x)) is None, f"Expected the piece at (9, {x}) to be captured"
    
    assert game.turn == 1, "It should be player 1's turn after player 2 captures the group"


def test_game_end_territories_and_neutral_zone() -> None:
    """Test a game ending with each player having at least one territory and one
    neutral zone, verifying final scores."""
    game = Go(side=19, players=2)

    board_state = [[None for _ in range(1, 20)] for _ in range(1, 20)]

    board_state[6][6] = 1
    board_state[7][7] = 1
    board_state[5][7] = 1
    board_state[6][8] = 1

    board_state[4][4] = 2
    board_state[3][5] = 2
    board_state[5][5] = 2
    board_state[4][6] = 2
    
    board_state[2][3] = 1
    board_state[3][2] = 2
    # (1, 1) is a neutral territory in this game
    
    game.load_game(turn=1, grid=board_state)
    
    game.pass_turn()
    game.pass_turn()

    expected_scores = {1: 6, 2: 6}
    assert game.scores() == expected_scores
    assert game.done, "Game should be marked as done"
    assert set(game.outcome) == {1, 2}, "Both players should be marked as having same score"


def test_three_player_game_with_territories_and_neutral_zone() -> None:
    """
    Test a three-player game ending with each player having at least one territory 
    and one neutral territory on a board of variable size.
    """
    game = Go(side=19, players=3)

    board_state = [[None for _ in range(1, 20)] for _ in range(1, 20)]

    board_state[6][6] = 1
    board_state[7][7] = 1
    board_state[5][7] = 1
    board_state[6][8] = 1

    board_state[4][4] = 2
    board_state[3][5] = 2
    board_state[5][5] = 2
    board_state[4][6] = 2
    
    board_state[11][11] = 3
    board_state[12][12] = 3
    board_state[10][12] = 3
    board_state[11][13] = 3
    
    board_state[2][3] = 1
    board_state[3][2] = 2
    board_state[2][2] = 3

    game.load_game(turn=1, grid=board_state)
    for _ in range(3):
        game.pass_turn()

    expected_scores = {1: 6, 2: 6, 3: 6}

    assert game.scores() == expected_scores, f"Scores mismatch. Expected: {expected_scores}, Actual: {game.scores()}"
    assert game.done, "Game should be marked as done."

    assert len(game.outcome) == 3, "All players should have scores in this setup."


