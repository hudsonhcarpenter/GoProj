"""
This represents the bot
"""

import random
import argparse
from go import Go


def add_line_parameters() -> argparse.Namespace:
    """
    Adds command-line parameters to the Bot
    
    I used the following source to understand how to create the parser
    https://docs.python.org/3/library/argparse.html
    """
    parser = argparse.ArgumentParser(description='Parser')

    parser.add_argument('-n', '--num-games', type=int, default=20)
    parser.add_argument('-s', '--size', type=int, default=6)
    parser.add_argument('-1', '--player1', type=str, default='random',
    choices=['random', 'smart', 'heuristic'])
    parser.add_argument('-2', '--player2', type=str, default='random',
    choices=['random', 'smart', 'heuristic'])

    args = parser.parse_args()

    return args

def heuristic(game: Go) -> tuple[int, int]:
    """
    Employs a strategy based on trying to control the corners or edges.
    Resorts to smart strategy if edges and corners are full. 

    Returns (tuple): the location of the move
    """
    size = game.size
    poss_edges = []
    poss_corners = []
    board_corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    board_edges = [(0, i) for i in range(1, size-1)] + \
            [(i, 0) for i in range(1, size-1)] + \
            [(size-1, i) for i in range(1, size-1)] + \
            [(i, size-1) for i in range(1, size-1)]

    for corner in board_corners:
        if corner in game.available_moves:
            poss_corners.append(corner)

    for edge in board_edges:
        if edge in game.available_moves:
            poss_edges.append(edge)

    if poss_corners:
        return random.choice(poss_corners)

    if poss_edges:
        poss_edges.sort(key=lambda x: min(abs(x[0]), abs(x[1]-size+1),
        abs(x[0]-size+1), abs(x[1])))
        return poss_edges[0]

    return smart_strategy(game)

def smart_strategy(game: Go) -> tuple[int,int]:
    """
    Identifies the best move for the more intelligent player by analyzing the 
    propsective implications of a selected move

    Returns (tuple): the location of the move
    """
    current_player = game.turn
    top_val = float('-inf')
    best_move = None

    for move in game.available_moves:
        simulate_game = game.simulate_move(move)
        next_moves = simulate_game.available_moves
        piece_counts = []

        for next_move in next_moves:
            simulate_game_two = simulate_game.simulate_move(next_move)
            scores = simulate_game_two.scores()
            piece_counts.append(scores.get(current_player, 0))

        value_m = sum(piece_counts) / len(piece_counts) if piece_counts else 0

        if value_m > top_val:
            top_val = value_m
            best_move = move

    return best_move if best_move else random.choice(game.available_moves)

def simulated_game(side:int, p1_strat: str, p2_strat: str) -> tuple[Go, int]:
    """
    Simulates a game using a 6x6 board and 2 players.

    Returns (tuple): simulated game and the move count
    """
    game = Go(side=side, players=2)
    move_count = 0
    max_count = 256

    while not game.done and move_count < max_count:
        if game.turn == 1:
            current_strat = p1_strat
        else:
            current_strat = p2_strat
        if current_strat == 'random':
            poss_moves = [move for move in game.available_moves if move !=
                          (0, 0)]
            if poss_moves:
                selected_move = random.choice(poss_moves)
            else:
                selected_move = (0, 0)
        elif current_strat == 'smart':
            selected_move = smart_strategy(game)
        else:
            selected_move = heuristic(game)
        if selected_move == (0, 0):
            game.pass_turn()
        else:
            game.apply_move(selected_move)
        move_count += 1

    return game, move_count

def statistics_games(total_games: int, side: int, p1_strat: str, p2_strat: str) -> None:
    """
    Calculates percentage of wins for each player, ties, and the move count.

    Returns: Nothing
    """

    win_dict: dict = {1: 0, 2: 0}
    tie_count = 0
    avg_count = []

    for _ in range(total_games):
        game, move_count = simulated_game(side, p1_strat, p2_strat)
        game_outcome = game.outcome
        avg_count.append(move_count)
        if len(game_outcome) == 1:
            winner = game_outcome[0]
            if winner in win_dict:
                win_dict[winner] += 1
            else:
                win_dict[winner] = 1
        else:
            scores = game.scores()
            if scores[1] > scores[2]:
                win_dict[1] += 1
            elif scores[2] > scores[1]:
                win_dict[2] += 1
            else:
                tie_count += 1

    one_win_percent = f"{win_dict[1] / total_games * 100:.2f}"
    two_wins_percent = f"{win_dict[2] / total_games * 100:.2f}"
    ties_percent = f"{tie_count / total_games * 100:.2f}"
    moves_calc = sum(avg_count) / total_games
    average_moves = f"{moves_calc:.1f}"

    print(f"Player 1 wins: {one_win_percent}%")
    print(f"Player 2 wins: {two_wins_percent}%")
    print(f"Ties: {ties_percent}%")
    print(f"Average moves: {average_moves}")

def main():
    args = add_line_parameters()
    statistics_games(args.num_games, args.size, args.player1, args.player2)

if __name__ == '__main__':
    main()
