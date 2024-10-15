from findMoves import *

centralValues = [[0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 7, 7, 7, 7, 0, 0], 
                 [0, 0, 7, 9, 9, 7, 0, 0], 
                 [0, 0, 7, 9, 9, 7, 0, 0], 
                 [0, 0, 7, 7, 7, 7, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0]]

kingPositionalValues = [[0, 0, 0, 0, 7, 7, 7, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 7, 7, 7, 0]]


def evaluateBoard(board, numMoves):
    score = 0

    numWBishop = 0
    numBBishop = 0

    # give a material count
    for row in board:
        for piece in row:
            if piece != '':
                val = pieceValues[(piece.lower())]
                if piece.isupper():
                    score -= val
                else:
                    score += val

    # doubled pawns penalty
    for col in range(8):
        for row in range(8):
            if board[row][col] == 'p':
                for x in range(row - 1, 0, -1):
                    if board[x][col] == 'p':
                        score -= 7
            elif board[row][col] == 'P':
                for x in range(row + 1, 7):
                    if board[x][col] == 'P':
                        score += 7

    # pawns being diagonal to each other and pawns and kights being in central boards
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'p':
                score += centralValues[row][col]
                if col - 1 >= 0 and row >= 0:
                    if board[row + 1][col - 1] == 'p':
                        score += 3
                if col + 1 <= 7 and row >= 0:
                    if board[row + 1][col + 1] == 'p':
                        score += 3
                # passed pawns
                x = True
                for i in range(row - 1, -1, -1):
                    if board[i][col].isupper():
                        x = False
                if x:
                    score += 50
                # doubled pawns
                for i in range(row - 1, -1, -1):
                    if board[i][col] == 'p':
                        score -= 35
            elif board[row][col] == 'P':
                score -=  centralValues[::-1][row][col]
                if col - 1 >= 0 and row <= 7:
                    if board[row - 1][col - 1] == 'P':
                        score -= 3
                if col + 1 <= 7 and row <= 7:
                    if board[row - 1][col + 1] == 'P':
                        score -= 3
                # passed pawns
                x = True
                for i in range(row + 1, 8):
                    if board[i][col].islower():
                        x = False
                if x:
                    score -= 50
                # doubled pawns
                for i in range(row + 1, 8):
                    if board[i][col] == 'P':
                        score += 35
            elif board[row][col] == 'n':
                score += centralValues[row][col]
                # connected knights
                knightMoves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
                for move in knightMoves:
                    r = row + move[0]
                    c = col + move[1]
                    if 0 <= r < 8 and 0 <= c < 8: 
                        if board[r][c] == 'n':
                            score += 9 # score will get added twice as it each pair is counted twice
            elif board[row][col] == 'N':
                score -=  centralValues[::-1][row][col]
                # connected knights
                knightMoves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
                for move in knightMoves:
                    r = row + move[0]
                    c = col + move[1]
                    if 0 <= r < 8 and 0 <= c < 8: 
                        if board[r][c] == 'N':
                            score -= 9 # score will get added twice as it each pair is counted twice
            # kings positional values
            elif board[row][col] == 'k':
                score += kingPositionalValues[row][col]
            elif board[row][col] == 'K':
                score -= kingPositionalValues[row][col]
            # checking for bishop pairs
            elif board[row][col] == 'b':
                numWBishop += 1
            elif board[row][col] == 'B':
                numBBishop += 1

    # penalty for queen moving in opening stage
    if numMoves < 10:
        if board[0][3] != 'Q':
            score += 100

    # bishop pair
    if numBBishop == 2:
        score -= 15
    if numWBishop == 2:
        score += 15

    # isolated pawns

    # open files for rooks

    # open files for bishops

    # piece mobility

    return score


def scoreMove(board, move, colour):
    # score move depending on how good it might be, for move ordering for minimax alpha beta cutoffs
    score = 0

    endPos = move[1]
    capturedPiece = board[endPos[0]][endPos[1]]

    # prioritise captures
    if capturedPiece != '':
        score += pieceValues[capturedPiece.lower()]

    # prioritise checks
    if colour == 'black':
        x = 'white'
    else:
        x = 'black'

    kingPos = findKing(board, x)
    if checkSquaresAttacked(board, kingPos[0], kingPos[1]):
        score += 50

    return score


def getScore(x):
    return x[0]

    
def orderMoves(board, colourMoves, colour):
    allMoves = []
    moves = []
    
    # iterate through moves, find score then append
    for pieceMoves in colourMoves:
        for move in pieceMoves[1]:
            if move != []:
                score = scoreMove(board, [pieceMoves[0], move], colour)
                allMoves.append([score, pieceMoves[0], move])


    # sort the moves
    allMoves.sort(key=getScore, reverse=True)

    # return sorted moves
    for i in allMoves:
        moves.append([i[1], i[2]])

    return moves


def minimax(board, depth, alpha, beta, maximisingPlayer, openingTable, numMoves):
    # check if the board is in the opening book, if so return the move for that opening
    posKey = str(board)

    if posKey in openingTable:
        return openingTable[posKey]
    
    if depth == 0:
        return evaluateBoard(board, numMoves), None

    bestMove = None

    # white is maximising its eval
    if maximisingPlayer:
        maxEval = float('-inf')
        colourMoves = getColourMoves(board, 'white')
        colourMoves = orderMoves(board, colourMoves, 'white')
        # check if it is checkmate
        y = True
        for x in colourMoves:
            if x[1] != []:
                y = False
        if y:
            return float('-inf'), None
        for pieceMoves in colourMoves:
            # keep track of origininal board to restore board later
            originalPiece = board[pieceMoves[0][0]][pieceMoves[0][1]]
            otherOriginalPiece = board[pieceMoves[1][0]][pieceMoves[1][1]]

            # make the move
            board[pieceMoves[1][0]][pieceMoves[1][1]] = originalPiece
            board[pieceMoves[0][0]][pieceMoves[0][1]] = ''
            # update promoted pawns
            for x in range(8):
                if board[0][x] == 'p':
                    board[0][x] = 'q'

            # call minimax on board
            evaluation, move = minimax(board, depth - 1, alpha, beta, False, openingTable, numMoves)

            # undo move
            board[pieceMoves[0][0]][pieceMoves[0][1]] = originalPiece
            board[pieceMoves[1][0]][pieceMoves[1][1]] = otherOriginalPiece

            # uodate best evaluation and move
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = pieceMoves

            # update alpha
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break  # beta cut off

        return maxEval, bestMove

    # black is trying to minimise the eval
    else:
        minEval = float('inf')
        colourMoves = getColourMoves(board, 'black')
        colourMoves = orderMoves(board, colourMoves, 'black')
        # check if it is checkmate
        y = True
        for x in colourMoves:
            if x[1] != []:
                y = False
        if y:
            # forced checkmate
            return float('inf'), None
        for pieceMoves in colourMoves:
            # keep track of origininal board to restore board later
            originalPiece = board[pieceMoves[0][0]][pieceMoves[0][1]]
            otherOriginalPiece = board[pieceMoves[1][0]][pieceMoves[1][1]]

            # make the move
            board[pieceMoves[1][0]][pieceMoves[1][1]] = originalPiece
            board[pieceMoves[0][0]][pieceMoves[0][1]] = ''
            # update promote pawns'
            for x in range(8):
                if board[7][x] == 'P':
                    board[7][x] = 'Q'
            
            # call minimax on board
            evaluation, move = minimax(board, depth - 1, alpha, beta, True, openingTable, numMoves)

            # undo move
            board[pieceMoves[0][0]][pieceMoves[0][1]] = originalPiece
            board[pieceMoves[1][0]][pieceMoves[1][1]] = otherOriginalPiece

            # update best evaluation and move
            if evaluation < minEval:
                minEval = evaluation
                bestMove = pieceMoves

            # update beta 
            beta = min(beta, minEval)
            if beta <= alpha:
                break  # alpha cut off

        return minEval, bestMove
