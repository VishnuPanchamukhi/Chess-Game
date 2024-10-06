# importing everything

import pygame as pg
import copy
import random
import numpy as np
from openingBook import *

# sceen dimensions

TILESIZE = 64
WIDTH = TILESIZE * 8
HEIGHT = TILESIZE * 8
FPS = 60

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 60, 210)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (30, 30, 30)

# board array

board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
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
darkSquare = pg.transform.scale(pg.image.load('img/darkSquare.png'), (WIDTH, HEIGHT))
highlightSquare = pg.transform.scale(pg.image.load('img/highlight.png'), (TILESIZE, TILESIZE))
highlightSquare2 = pg.transform.scale(pg.image.load('img/highlight2.png'), (TILESIZE, TILESIZE))
check = pg.transform.scale(pg.image.load('img/check.png'), (TILESIZE, TILESIZE))
