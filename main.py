from evaluation import *


# game class

class Game:

    def __init__(self):
        # initialize game window
        pg.init()
        self.font = pg.font.Font('freesansbold.ttf', 20)
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
        # time trackers
        self.playerTime = PLAYERTIME
        self.botTime = BOTTIME
        self.currentTurn = 'player'
        self.startOfTurnTime = None
        

    def new(self):
        # start a new game
        self.run()


    def run(self):
        # game loop
        self.playing = True
        self.startOfTurnTime = time.time()
        while self.playing:
            # making the game loop run at the fps
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # game loop update
        # find time taken since the start of the go
        currentTime = time.time()
        timeTaken = currentTime - self.startOfTurnTime
        if self.currentTurn == 'player':
            self.playerTime -= timeTaken
        else:
            self.botTime -= timeTaken
        self.startOfTurnTime = currentTime
        # check if time has ran out
        if self.playerTime <= 0:
            print('The bot won on time!')
            self.playing = False
            self.running = False
        if self.botTime <= 0:
            print('The player won on time')
            self.playing = False
            self.running = False


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
                # check the board is being clicked
                if (excessWidth < self.pos[0] < WIDTH - excessWidth) and (excessHeight < self.pos[1] < HEIGHT - excessHeight):
                    resultx = ((self.pos[0]) // TILESIZE) - int(excessWidth / TILESIZE)
                    resulty = ((self.pos[1]) // TILESIZE) - int(excessHeight / TILESIZE)
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
                            # track start of turn for bot
                            self.startOfTurnTime = time.time()
                            self.currentTurn = 'bot'
                            botStartTime = time.time()
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
                                if [self.clickCoords[-1][0], self.clickCoords[-1][1]] == [self.clickCoords[-2][0], self.clickCoords[-2][1] + 2]:
                                    # check rook is actually there
                                    if board[7][7] == 'r':
                                        if board[7][6] == 'k':
                                            board[7][7] = ''
                                            board[7][5] = 'r'
                                if [self.clickCoords[-1][0], self.clickCoords[-1][1]] == [self.clickCoords[-2][0], self.clickCoords[-2][1] - 2]:
                                    if board[7][0] == 'r':
                                        if board[7][2] == 'k':
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
                            # minimax returned checkmate
                            if bestMove == None:
                                print('There is forced Checkamate')
                                self.playing = False
                                self.running = False
                                break
                            board[bestMove[1][0]][bestMove[1][1]] = board[bestMove[0][0]][bestMove[0][1]]
                            board[bestMove[0][0]][bestMove[0][1]] = ''
                            currentEval = evaluateBoard(board, self.numMoves)
                            print('Current Eval:', currentEval)
                            # handle time
                            botEndTime = time.time()
                            botTimeTaken = botEndTime - botStartTime
                            self.botTime -= botTimeTaken
                            self.startOfTurnTime = time.time()
                            self.currentTurn = 'player'
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
                            print()
                            print('It is an illegal move!')
                            print()
                            self.pieceSelected = None


    def draw(self):
        # game loop draw
        # draw bg colour
        self.screen.blit(bgColour, (0, 0))
        # draw background chess board pattern by filling back green and place a light square every alternate square
        self.screen.blit(darkSquare, (excessWidth, excessHeight))
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    self.screen.blit(lightSquare, ((x * TILESIZE) + excessWidth, (y * TILESIZE) + excessHeight))
        # draw on highlighted squares
        if self.pieceSelected != None:
            self.screen.blit(highlightSquare, ((self.pieceSelected[0] * TILESIZE) + excessWidth, (self.pieceSelected[1] * TILESIZE) + excessHeight))
        if self.moveSelected != None:
            self.screen.blit(highlightSquare2, ((self.moveSelected[0] * TILESIZE) + excessWidth, (self.moveSelected[1] * TILESIZE) + excessHeight))
        if self.wKingInCheck:
            wKingPos = findKing(board, 'white')
            if checkSquaresAttacked(board, wKingPos[0], wKingPos[1]):
                self.screen.blit(check, ((wKingPos[1] * TILESIZE) + excessWidth, (wKingPos[0] * TILESIZE) + excessHeight))
        if self.bKingInCheck:
            bKingPos = findKing(board, 'black')
            if checkSquaresAttacked(board, bKingPos[0], bKingPos[1]):
                self.screen.blit(check, ((bKingPos[1] * TILESIZE) + excessWidth, (bKingPos[0] * TILESIZE) + excessHeight))
        # draw pieces on board
        self.a = 0 
        self.b = 0
        for rowx in board:
            for piece in rowx:
                if piece != '':
                    if piece == 'B':
                        self.screen.blit(bB, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'K':
                        self.screen.blit(bK, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'N':
                        self.screen.blit(bN, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'P':
                        self.screen.blit(bP, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'Q':
                        self.screen.blit(bQ, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'R':
                        self.screen.blit(bR, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'b':
                        self.screen.blit(wB, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'k':
                        self.screen.blit(wK, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'n':
                        self.screen.blit(wN, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'p':
                        self.screen.blit(wP, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'q':
                        self.screen.blit(wQ, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                    elif piece == 'r':
                        self.screen.blit(wR, ((self.b * TILESIZE) + excessWidth, (self.a * TILESIZE) + excessHeight))
                self.b += 1
            self.a += 1
            self.b = 0

        # drawing plyer names
        text = self.font.render('Computer', True, WHITE, BG)
        text2 = self.font.render('Player', True, WHITE, BG)
        textRect = text.get_rect()
        textRect2 = text.get_rect()
        textRect.topleft = (excessWidth, excessWidth // 3)
        textRect2.topleft = (excessWidth, HEIGHT - ((3 * excessWidth) // 5))    
        self.screen.blit(text, textRect)
        self.screen.blit(text2, textRect2)
    
        # drawing timer boxes
        botTimerRect = pg.Rect(0, 0, 80, (4 * excessHeight) // 7)
        botTimerRect.topright = (WIDTH - excessWidth, excessHeight // 5) 
        pg.draw.rect(self.screen, TIMERCOLOUR, botTimerRect)

        playerTimerRect = pg.Rect(0, 0, 80, (4 * excessHeight) // 7)
        playerTimerRect.bottomright = (WIDTH - excessWidth, HEIGHT - (excessHeight // 5))
        pg.draw.rect(self.screen, TIMERCOLOUR, playerTimerRect)

        # find time
        playerMins = str(int(self.playerTime // 60))
        playerSecs = str(int(self.playerTime % 60))
        botMins = str(int(self.botTime // 60))
        botSecs = str(int(self.botTime % 60))
        if len(playerSecs) == 1:
            playerSecs += '0'
            playerSecs = playerSecs[::-1]
        if len(botSecs) == 1:
            botSecs += '0'
            botSecs = botSecs[::-1]

        # drawing time in timer boxes
        botTimeText = self.font.render(botMins + ':' + botSecs, True, WHITE, TIMERCOLOUR)
        botTimeRect = botTimeText.get_rect()
        botTimeRect.center = (WIDTH - excessWidth - 40, excessHeight // 5 + ((2 * excessHeight) // 7))
        self.screen.blit(botTimeText, botTimeRect)

        playerTimeText = self.font.render(playerMins + ':' + playerSecs, True, WHITE, TIMERCOLOUR)
        playerTimeRect = playerTimeText.get_rect()
        playerTimeRect.center = (WIDTH - excessWidth - 40, HEIGHT - (excessHeight // 5) - ((2 * excessHeight) // 7))
        self.screen.blit(playerTimeText, playerTimeRect)
                              
        # after drawing, flip
        pg.display.flip()
       

g = Game()


while g.running:
    g.new()


pg.quit()
