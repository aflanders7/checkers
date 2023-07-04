import pygame
from .constants import rows, cols, red, black, white, width, height, square_size

class Board:
    def __init__(self):
        self.board = []
        self.create_board()
        self.white = 12
        self.red = 12

    def get_piece(self, row, col):
        return self.board[row][col]

    def winner(self):
        if self.white == 0:
            return red
        if self.red == 0:
            return white
        else:
            return None

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece is not None:
                if piece.color == red:
                    self.red -= 1
                elif piece.color == white:
                    self.white -= 1

    def draw_board(self, win):
        win.fill(black)
        for row in range(rows):
            for col in range(row % 2, rows, 2): # every other box is red
                pygame.draw.rect(win, red, (row*square_size, col*square_size, square_size, square_size))

    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == (row+1)%2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, white))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, red))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == red or piece.king:
            moves.update(self.traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row-1, max(row-3, -1), -1, piece.color, right))

        if piece.color == white or piece.king:
            moves.update(self.traverse_left(row+1, min(row+3, rows), 1, piece.color, left))
            moves.update(self.traverse_right(row+1, min(row+3, rows), 1, piece.color, right))

        return moves

    def traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for index in range(start, stop, step):
            if left < 0:  # not in range of board
                break

            current = self.board[index][left]
            if current is None:  # found an empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(index, left)] = last + skipped
                else:
                    moves[(index, left)] = last

                if last:    # recalculate position if you skipped over something
                    if step == -1:
                        row = max(index-3, 0)
                    else:
                        row = min(index+3, rows)

                    moves.update(self.traverse_left(index+step, row, step, color, left-1, skipped=last))
                    moves.update(self.traverse_right(index+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color: # can't jump your own piece
                break

            else:
                last = [current]

            left -= 1

        return moves

    def traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for index in range(start, stop, step):
            if right >= cols:  # not in range of board
                break

            current = self.board[index][right]
            if current is None:  # found an empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(index, right)] = last + skipped
                else:
                    moves[(index, right)] = last

                if last:  # recalculate position if you skipped over something
                    if step == -1:
                        row = max(index - 3, 0)
                    else:
                        row = min(index + 3, rows)

                    moves.update(self.traverse_left(index + step, row, step, color, right - 1, skipped=last))
                    moves.update(self.traverse_right(index + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:  # can't jump your own piece
                break

            else:
                last = [current]

            right += 1

        return moves

    def draw(self, win):
        self.draw_board(win)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw_piece(win)

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if piece.color == white and row == 7:
            piece.king = True
        if piece.color == red and row == 0:
            piece.king = True


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = (square_size * self.col) + square_size//2
        self.y = (square_size * self.row) + square_size//2

    def make_king(self):
        self.king = True
        self.color = (171, 141, 63)

    def draw_piece(self, win):
        radius = square_size//2 - 15
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
