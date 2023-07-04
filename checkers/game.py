import pygame
from .board import Board
from .constants import red, white, square_size, black


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.turn = red
        self.valid_moves = {}
        self.win = win

    def winner(self):
        return self.board.winner()

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        if piece is not None and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece is None and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()

        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = []
        if self.turn == red:
            self.turn = white
        else:
            self.turn = red

    def draw_valid_moves(self, moves):
        radius = square_size//2 - 15
        inner_radius = square_size//2 - 18

        for move in moves:
            row, col = move
            x = (square_size * col) + square_size // 2
            y = (square_size * row) + square_size // 2
            pygame.draw.circle(self.win, self.turn, (x, y), radius)
            pygame.draw.circle(self.win, black, (x, y), inner_radius)


