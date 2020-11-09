#Calebe Ferreira / T.I.A:32088116#
#Gustavo Alves / T.I.A:32081286#
#Mateus de Pasquali / T.I.A:32086997#
#Nicolas Pisndorf / T.I.A: 32036108#

import pygame
import sys
import os


def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def draw_board(surface):
    width = surface.get_width()
    height = surface.get_height()
    white = (255, 255, 255)

    # Draw border
    pygame.draw.line(surface, white, (0, 0), (width, 0))
    pygame.draw.line(surface, white, (0, 0), (0, height))
    pygame.draw.line(surface, white, (width - 1, 0), (width - 1, height))
    pygame.draw.line(surface, white, (0, height - 1), (width, height - 1))

    # Draw vertical lines
    pygame.draw.line(surface, white, (width / 3, 0), (width / 3, height))
    pygame.draw.line(surface, white, (2 * width / 3, 0), (2 * width / 3, height))

    # Draw horizontal lines
    pygame.draw.line(surface, white, (0, height / 3), (width, height / 3))
    pygame.draw.line(surface, white, (0, 2 * height / 3), (width, 2 * height / 3))

def draw_x(surface, row, col):
    width = surface.get_width()
    height = surface.get_height()
    posx = int((width / 3) * col + width / 6)
    posy = int((height / 3) * row + height / 6)

    white = (255, 255, 255)
    pygame.draw.line(surface, white, (posx - 5, posy - 5), (posx + 5, posy + 5))
    pygame.draw.line(surface, white, (posx + 5, posy - 5), (posx - 5, posy + 5))

def draw_o(surface, row, col):
    width = surface.get_width()
    height = surface.get_height()
    white = (255, 255, 255)
    posx = int((width/3) * col + width/6)
    posy = int((height / 3) * row + height/6)
    pygame.draw.circle(surface, white, [posx, posy], 7, 1)

def draw_symbol(surface, symbol, row, col):
    if symbol == 'x':
        draw_x(surface, row, col)
        effect.play()
    else:
        draw_o(surface, row, col)
        effect.play()


def check_victory_horizontal_lines(symbol, board):
    for line in board:
        if line.count(symbol) == 3:
            return True

def check_victory_vertical_lines(symbol, board):
    counter_by_line = 0
    for col in range(3):
        for line in board:
            if line[0] == symbol:
                counter_by_line += 1
                if counter_by_line == 3:
                    return True
            else:
                counter_by_line = 0
                break

def check_victory_diagonal_lines(symbol, board):
    index = 0
    counter = 0

    for line in board:
        if line[index] == symbol:
            counter += 1
            index += 1
            if counter == 3:
                return True
        else:
            counter = 0
            index = 2
            break

    for line in board:
        if line[index] == symbol:
            counter += 1
            index -= 1
            if counter == 3:
                return True
        else:
            break

    return False

def check_victory(xturn, board):
    symbol = 'x' if xturn else 'o'
    return check_victory_horizontal_lines(symbol, board) or \
           check_victory_vertical_lines(symbol, board) or \
           check_victory_diagonal_lines(symbol, board)

def check_tie(board):
    for line in board:
        if 0 in line:
            return False
    return True

if __name__ == "__main__":
    pygame.init()

    board = [[0,0,0],[0,0,0],[0,0,0]]

    xturn = True;

    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    victory = False

    pygame.mixer.music.load("data/music/happy.mp3")
    pygame.mixer.music.play(-1)

    effect = pygame.mixer.Sound('data/soundEffects/effect.wav')
    vic = pygame.mixer.Sound('data/soundEffects/victory.mp3')
    fail = pygame.mixer.Sound('data/soundEffects/fail.mp3')

    trophy = pygame.image.load('data/image/trophy.jpg')

    while True:


        draw_board(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:

                if not victory:

                    pos = pygame.mouse.get_pos()
                    col = int(pos[0] / (width / 3))
                    row = int(pos[1] / (height / 3))

                    if board[row][col] == 0:
                        if xturn:
                            draw_symbol(screen, 'x', row, col)
                            board[row][col] = 'x'
                        else:
                            draw_symbol(screen, 'o', row, col)
                            board[row][col] = 'o'

                        if check_victory(xturn, board):
                            print("VITÓRIA!!!")
                            vic.play()
                            pygame.time.wait(2000)                            
                            restart_program()

                        if check_tie(board):
                            print("VELHA!!!")
                            fail.play()
                            pygame.time.wait(4000)  
                            restart_program()
                            
                        xturn = not xturn