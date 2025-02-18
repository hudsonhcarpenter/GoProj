"""
This is the TUI Class
"""
import click
from base import GoBase
from go import Go
from bot import smart_strategy


def print_board(board: GoBase) -> None:
    """
    Prints the board 
    """
    grid = board.grid
    size = len(grid)

    print()
    for r, row in enumerate(grid):
        crow = ""
        for c, square in enumerate(row):
            if r == 0:
                if c == 0 and square is None:
                    crow += " ┌-"
                elif c == size - 1 and square is None:
                    crow += "-┐ "
                elif square is None:
                    crow += "---"
                elif c != 0 and c != size -1:
                    crow += f"-{square}-"
            elif r < size - 1:
                if c == 0 and square is None:
                    crow += " ├-"
                elif c == size - 1 and square is None:
                    crow += "-┤ "
                elif square is None:
                    crow += "-+-"
                elif c != 0 and c != size -1:
                    crow += f"-{square}-"
            else:
                if c == 0 and square is None:
                    crow += " └-"
                elif c == size - 1 and square is None:
                    crow += "-┘ "
                elif square is None:
                    crow += "---"
                elif c != 0 and c != size -1:
                    crow += f"-{square}-"
            if c == 0 and square is not None:
                    crow += f" {square}-"
            if c == size - 1 and square is not None:
                    crow += f"-{square} "
        print(crow)
        if r != size -1:
            print(" | " * size)  

@click.command()
@click.option('-n', '--num-players', default=2, type=int, help='Number of players')
@click.option('-s', '--size', default=19, type=int, help='Board size')
@click.option('--simple-ko', 'ko_rule', type=bool, default=True, is_flag=True, help='Use simple ko rule')
@click.option('--super-ko', 'ko_rule', type=bool, is_flag=True, help='Use super ko rule')
def create_game(num_players, size, ko_rule) -> None:
    go = Go(size, num_players, ko_rule)

    print_board(go)
    
    while not go.done:
        user_input = input(f"It is player {go.turn}'s turn. "
                           "Please enter a move [Press Enter to pass, "
                           "type \"hint\" to receive a recommended move]:\n> ")
        
        if user_input.lower() == "hint":
            print("Recommended move:", smart_strategy(go))
        else:
            try:
                move = tuple(int(num) for num in user_input.split())

                if move == ():
                    print(f"Player {go.turn} has passed their turn.\n")
                    go.pass_turn()
                elif not go.legal_move(move):
                    print("That move is not legal, try again.")
                else:
                    go.apply_move(move)
                    print_board(go)
            except ValueError:
                print("Invalid input.")

    print("Game Over\nThe winners are:")
    for player in go.outcome:
        print("Player ", player)
    

if __name__ == '__main__':
    create_game()

 