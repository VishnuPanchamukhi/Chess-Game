# importing everything

import pygame as pg
import copy
import random
import numpy as np
from openingBook import *
import time

# sceen dimensions

TILESIZE = 73
WIDTH = TILESIZE * 10.5
HEIGHT = TILESIZE * 10.5
FPS = 60
excessWidth = (WIDTH - (TILESIZE * 8)) / 2
excessHeight = (HEIGHT - (TILESIZE * 8)) / 2

# time controls

PLAYERTIME = 3600
BOTTIME = 3600

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 60, 210)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (30, 30, 30)
BG = (49, 46, 43)
TIMERCOLOUR = (40, 41, 42)

# board array

board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # uppercase --> black and lowercase --> white
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         ['',  '',  '',  '',  '',  '',  '',  ''], 
         ['',  '',  '',  '',  '',  '',  '',  ''], 
         ['',  '',  '',  '',  '',  '',  '',  ''], 
         ['',  '',  '',  '',  '',  '',  '',  ''], 
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

# imgs for all the pieces

bB = pg.transform.scale(pg.image.load('img/bBishop.png'), (TILESIZE, TILESIZE))
bK = pg.transform.scale(pg.image.load('img/bKing.png'), (TILESIZE, TILESIZE))
bP = pg.transform.scale(pg.image.load('img/bPawn.png'), (TILESIZE, TILESIZE))
bQ = pg.transform.scale(pg.image.load('img/bQueen.png'), (TILESIZE, TILESIZE))
bR = pg.transform.scale(pg.image.load('img/bRook.png'), (TILESIZE, TILESIZE))
bN = pg.transform.scale(pg.image.load('img/bKnight.png'), (TILESIZE, TILESIZE))
wB = pg.transform.scale(pg.image.load('img/wBishop.png'), (TILESIZE, TILESIZE))
wK = pg.transform.scale(pg.image.load('img/wKing.png'), (TILESIZE, TILESIZE))
wP = pg.transform.scale(pg.image.load('img/wPawn.png'), (TILESIZE, TILESIZE))
wQ = pg.transform.scale(pg.image.load('img/wQueen.png'), (TILESIZE, TILESIZE))
wR = pg.transform.scale(pg.image.load('img/wRook.png'), (TILESIZE, TILESIZE))
wN = pg.transform.scale(pg.image.load('img/wKnight.png'), (TILESIZE, TILESIZE))

lightSquare = pg.transform.scale(pg.image.load('img/lightSquare.png'), (TILESIZE, TILESIZE))
darkSquare = pg.transform.scale(pg.image.load('img/darkSquare.png'), (TILESIZE * 8, TILESIZE * 8))
highlightSquare = pg.transform.scale(pg.image.load('img/highlight.png'), (TILESIZE, TILESIZE))
highlightSquare2 = pg.transform.scale(pg.image.load('img/highlight2.png'), (TILESIZE, TILESIZE))
check = pg.transform.scale(pg.image.load('img/check.png'), (TILESIZE, TILESIZE))
bgColour = pg.transform.scale(pg.image.load('img/bgColour.png'), (WIDTH, HEIGHT))


# dictionary to help with scoring

pieceValues = {'p':100, 'n':324, 'b':340, 'r':500, 'q':900, 'k':0}
