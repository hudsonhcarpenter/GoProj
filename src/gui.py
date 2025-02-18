
"""
This is the GUI Class.
"""
import os
import sys
from typing import Tuple
import pygame
import click
from pygame import QUIT, MOUSEBUTTONDOWN
from go import Go

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

class Gui:
    """
    This is the GUI Class.
    """
    def __init__(self, game: Go):
        self.game = game
        self.board_size = self.game.size
        self.grid_size = 600
        self.margin = self.grid_size / (self.board_size + 1)
        self.piece_radius = self.margin * 0.4
        self.width = (self.board_size + 1) * self.margin
        self.height = (self.board_size + 1) * self.margin
        self.window = pygame.display.set_mode((self.width + 200, self.height))
        pygame.display.set_caption("Go Game")
        self.clock = pygame.time.Clock()
        self.selected = None
        self.player_colors = [BLACK, WHITE, RED, BLUE, \
                              YELLOW, CYAN, MAGENTA, ORANGE]
        self.current_player = self.game.turn

    def get_mouse_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Get the row and column of the board corresponding to the mouse \
        position, if the mouse is near a piece.

        Inputs:
            pos (Tuple[int, int]): The position of the mouse on the window.

        Returns Optional(Tuple[int, int]): The row and column of the board
        """
        x, y = pos
        row = int((y - (0.5*self.margin)) // self.margin)
        col = int((x - (0.5*self.margin)) // self.margin)
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.game.legal_move((row+1, col+1)):
                return (row, col)
        return None

    def draw_piece(self, row: int, col: int, color: Tuple[int, int, int]) -> None:
        """
        Draw a piece on the board at a speicified location \
            with a specified color.

        Inputs:
            row (int): The row of the piece.
            col (int): The column of the piece.
            color (Tuple[int, int, int]): The color of the piece.

        Returns None
        """
        x = (col + 1) * self.margin
        y = (row + 1) * self.margin
        pygame.draw.circle(self.window, color, (x, y), self.piece_radius)

    def draw_board(self) -> None:
        """
        Draw the board, the pieces, a potential temperary piece pass button, \
            and turn indicator on the window.
        """
        self.window.fill(BROWN)

        # Draw grid lines
        for i in range(self.board_size):
            pygame.draw.line(self.window, BLACK, \
                             (self.margin + i * self.margin, self.margin),
                             (self.margin + i * self.margin, \
                              self.grid_size - self.margin), 2)
            pygame.draw.line(self.window, BLACK, (self.margin, \
                                self.margin + i * self.margin),
                             (self.grid_size - self.margin, \
                              self.margin + i * self.margin), 2)

        # Draw pieces
        for row in range(self.game.size):
            for col in range(self.game.size):
                piece = self.game.piece_at((row+1, col+1))
                if piece is not None:
                    color = self.player_colors[piece - 1]
                    self.draw_piece(row, col, color)

        # Display turn
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Turn: Player {self.current_player}", True, BLACK)
        text_rect = text.get_rect(center=(self.grid_size + 100, \
                                          self.grid_size // 2))
        self.window.blit(text, text_rect)

        # Draw pass button
        pygame.draw.rect(self.window, BROWN, (self.grid_size + 50, \
                                              self.grid_size // 4, 100, 50))
        pass_text = font.render("Pass Turn", True, BLACK)
        pass_rect = pass_text.get_rect(center=(self.grid_size + 100, \
                                               self.grid_size // 4 + 25))
        self.window.blit(pass_text, pass_rect)
        pygame.display.update()

        # Draw ghost piece if selected position is a legal move
        if self.selected:
            row, col = self.selected
            if self.game.legal_move((row+1, col+1)):
                x = (col + 1) * self.margin
                y = (row + 1) * self.margin
                pygame.draw.circle(self.window, GREEN, \
                                   (x, y), self.piece_radius)

        pygame.display.update()

    def passing_turn(self, pos: Tuple[int, int]) -> bool:
        """
        Check if the mouse position is on the pass button.

        Inputs:
            pos (Tuple[int, int]): The position of the mouse on the window.

        """
        pass_button_rect = pygame.Rect(self.grid_size + 50, \
                                       self.grid_size // 4, 100, 50)
        if pass_button_rect.collidepoint(pos):
            return True
        return False

    def display_winner(self) -> None:
        """
        Display the winner and scores on the window.
        """
        self.window.fill(WHITE)

        # Get game outcome and scores
        winners = self.game.outcome
        scores = self.game.scores()

        # Display outcome text
        font = pygame.font.SysFont(None, 36)
        if len(winners) == 1:
            outcome_text = f"Player {winners[0]} wins!"
        else:
            outcome_text = "It's a tie!"
        outcome_surface = font.render(outcome_text, True, BLACK)
        outcome_rect = outcome_surface.get_rect(center=(self.grid_size // 2, \
                                                        self.grid_size // 4))
        self.window.blit(outcome_surface, outcome_rect)

        # Display player scores
        y_offset = self.grid_size // 4 + 50
        for i, (player, score) in enumerate(scores.items()):
            score_text = f"Player {player}: {score}"
            score_surface = font.render(score_text, True, BLACK)
            score_rect = score_surface.get_rect(center=(self.grid_size // 2, \
                                                        y_offset + i * 30))
            self.window.blit(score_surface, score_rect)

        pygame.display.update()

    def run(self) -> None:
        """
        Run the game loop.
        """
        running = True
        while running and not self.game.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                #move
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.get_mouse_position(pos):
                        row, col = self.get_mouse_position(pos)
                        self.selected = (row +1, col +1)
                        self.game.apply_move(self.selected)
                        self.current_player = self.game.turn
                #pass turn
                    elif self.passing_turn(pos):
                        self.game.pass_turn()
                        self.current_player = self.game.turn


            # Highlight selected position if it's a legal move
            pos = pygame.mouse.get_pos()
            self.selected = self.get_mouse_position(pos)
            self.draw_board()
            self.clock.tick(30)

        # enter final phase
        pygame.mixer.music.stop()
        if self.game.done:
            self.display_winner()
            pygame.display.update()
            pygame.time.wait(10000)
        # pylint: disable=no-member
        pygame.quit()

# command line interface
@click.command()
@click.option('-n', '--num-players', default=2, type=int, \
              help='Number of players')
@click.option('-s', '--size', default=19, type=int, help='Board size')
@click.option('--super-ko', 'super_ko', is_flag=True, flag_value=True, default=False, \
              help='Use super ko rule')
@click.option('--simple-ko', 'simple_ko', is_flag=True, flag_value=False, \
              help='Use simple ko rule')

def main(num_players: int, size: int, super_ko: bool, simple_ko: bool) -> None:
    """
    Run the game with the specified number of players, board size, and ko rule.

    Inputs:
        num_players (int): The number of players.
        size (int): The size of the board.
        super_ko (bool): Whether to use the super ko rule.
        simple_ko (bool): Whether to use the simple ko rule.

    Returns None
    """
    try:
        if size < 6 or size > 30:
            raise ValueError("Board size must be between 6 and 30")
        if num_players < 2 or num_players > 8:
            raise ValueError("Number of players must be between 2 and 8")
        
        ko_rule = super_ko
        game = Go(size, num_players, ko_rule)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("src/gui_music.mp3")
        gui = Gui(game)
        pygame.mixer.music.play(-1)
        gui.run()

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
