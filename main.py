from evaluation import *


# game class

class Game:

    def __init__(self):
        # initialize game window
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Chess Game")
        self.clock = pg.time.Clock()
        self.running = True # controls if game is running
        self.piecesClicked = [] # tracks the pieces the player clicks
        self.clickCoords = [] # tracks the cells the player clicks
        self.numMoves = 0
        #  booleans to track castling ability
        self.wKingRookMoved = False
        self.wQueenRookMoved = False
        self.wKingMoved = False
        self.pieceSelected = None
        self.moveSelected = None
        self.wKingInCheck = False
        self.bKingInCheck = False


    def new(self):
        # start a new game
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            # making the game loop run at the fps
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # game loop update
        pass


    def events(self):
        # game loop events
        for event in pg.event.get():
            # check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False    
            elif event.type == pg.MOUSEBUTTONUP:
                # find the piece and coords the player clicked
                self.pos = pg.mouse.get_pos()
                resultx = self.pos[0] // TILESIZE
                resulty = self.pos[1] // TILESIZE
                self.piecesClicked.append(board[resulty][resultx])
                self.clickCoords.append([resulty, resultx])
                # check if player clicked on piece, if so highlight it
                if self.piecesClicked != '' and self.piecesClicked[-1].islower():
                    self.pieceSelected = [resultx, resulty]
                    self.moveSelected = None
                # check if the player clicks the same piece twice
                if len(self.clickCoords) > 1 and self.clickCoords[-1] == self.clickCoords[-2]:
                    self.clickCoords.clear()
                    self.piecesClicked.clear()
                    self.pieceSelected = None
                    self.moveSelected = None
                # check if a move was attempted and that the first click was on a piece, and that piece is white
                if len(self.clickCoords) > 1 and self.piecesClicked[-2] != '' and self.piecesClicked[-2].islower():
                    # check if the move is part of the pieces legal moves
                    pieceMoves =  getPieceMoves(self.piecesClicked[-2], self.clickCoords[-2][0], self.clickCoords[-2][1], self.wKingMoved, self.wKingRookMoved, self.wQueenRookMoved)
                    if self.clickCoords[-1] in pieceMoves:
                        self.numMoves += 1
                        self.moveSelected = [resultx, resulty]
                        # perform the move
                        board[(self.clickCoords[-1])[0]][(self.clickCoords[-1])[1]] = self.piecesClicked[-2]
                        board[(self.clickCoords[- 2])[0]][(self.clickCoords[-2])[1]] = ''
                        # pawn promotions
                        for x in range(8):
                            if board[0][x] == 'p':
                                board[0][x] = 'q'
                        # update castling bools 
                        if self.piecesClicked[-2] == 'k':
                            self.wKingMoved = True
                        elif self.piecesClicked[-2] == 'r':
                            if [(self.clickCoords[- 2])[0], (self.clickCoords[-2])[1]] == [7, 7]:
                                self.wKingRookMoved = True
                            else:
                                self.wQueenRookMoved = True
                        # castle if the king has moved 2 squares, and if so perfrom castling
                        if self.piecesClicked[-2] == 'k':
                            if board[7][6] == 'k':
                                board[7][7] = ''
                                board[7][5] = 'r'
                            elif board[7][2] == 'k':
                                board[7][0] = ''
                                board[7][3] = 'r'
                        # highlight square if black king in check
                        bKingPos = findKing(board, 'black')
                        if checkSquaresAttacked(board, bKingPos[0], bKingPos[1]):
                            self.bKingInCheck = True
                        else:
                            self.bKingInCheck = False
                        # check if player has checkmated black
                        if checkmate(board):
                            print('Checkmate!')
                            for e in board:
                                print(e)
                            self.playing = False
                            self.running = False
                            break
                        # clear lists of pieces clicked for next cycle
                        self.clickCoords.clear()
                        self.piecesClicked.clear()
                        self.draw()
                        self.pieceSelected = None
                        self.moveSelected = None
                        # find the bots move using minimax
                        x = minimax(board, 3, float('-inf'), float('inf'), False, openingTable, self.numMoves)
                        print('The best move is:', x)
                        bestMove = x[1]
                        board[bestMove[1][0]][bestMove[1][1]] = board[bestMove[0][0]][bestMove[0][1]]
                        board[bestMove[0][0]][bestMove[0][1]] = ''
                        # pawn promotions
                        for x in range(8):
                            if board[7][x] == 'P':
                                board[7][x] = 'Q'
                        # check if white king is in check
                        wKingPos = findKing(board, 'white')
                        if checkSquaresAttacked(board, wKingPos[0], wKingPos[1]):
                            self.wKingInCheck = True
                        else:
                            self.wKingInCheck = False
                        # check if bot has checkmated the player
                        if checkmate(board):
                            print('Checkmate!')
                            for e in board:
                                print(e)
                            self.playing = False
                            self.running = False
                            break

                    else:
                        print('It is an illegal move!')
                        self.pieceSelected = None


    def draw(self):
        # game loop draw
        # draw background chess board pattern by filling back green and place a light square every alternate square
        self.screen.blit(darkSquare, (0, 0))
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    self.screen.blit(lightSquare, (x * TILESIZE, y * TILESIZE))
        # draw on highlighted squares
        if self.pieceSelected != None:
            self.screen.blit(highlightSquare, (self.pieceSelected[0] * TILESIZE, self.pieceSelected[1] * TILESIZE))
        if self.moveSelected != None:
            self.screen.blit(highlightSquare2, (self.moveSelected[0] * TILESIZE, self.moveSelected[1] * TILESIZE))
        if self.wKingInCheck:
            wKingPos = findKing(board, 'white')
            if checkSquaresAttacked(board, wKingPos[0], wKingPos[1]):
                self.screen.blit(check, (wKingPos[1] * TILESIZE, wKingPos[0] * TILESIZE))
        if self.bKingInCheck:
            bKingPos = findKing(board, 'black')
            if checkSquaresAttacked(board, bKingPos[0], bKingPos[1]):
                self.screen.blit(check, (bKingPos[1] * TILESIZE, bKingPos[0] * TILESIZE))
        # draw pieces on board
        self.a = 0 
        self.b = 0
        for rowx in board:
            for piece in rowx:
                if piece != '':
                    if piece == 'B':
                        self.screen.blit(bB, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'K':
                        self.screen.blit(bK, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'N':
                        self.screen.blit(bN, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'P':
                        self.screen.blit(bP, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'Q':
                        self.screen.blit(bQ, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'R':
                        self.screen.blit(bR, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'b':
                        self.screen.blit(wB, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'k':
                        self.screen.blit(wK, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'n':
                        self.screen.blit(wN, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'p':
                        self.screen.blit(wP, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'q':
                        self.screen.blit(wQ, (self.b * TILESIZE, self.a * TILESIZE))
                    elif piece == 'r':
                        self.screen.blit(wR, (self.b * TILESIZE, self.a * TILESIZE))
                self.b += 1
            self.a += 1
            self.b = 0
                              
        # after drawing, flip
        pg.display.flip()
       

g = Game()

while g.running:
    g.new()


pg.quit()