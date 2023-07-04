import pygame
from checkers.constants import width, height, square_size, red
from checkers.game import Game

FPS = 60

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Checkers Game')


def get_pos_from_mouse(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(win)

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)

                game.select(row, col)

        game.update()

    pygame.quit()


main()

