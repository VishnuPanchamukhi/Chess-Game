from findMoves import *

centralValues = [[0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 4, 4, 4, 4, 0, 0], 
                 [0, 0, 4, 6, 6, 4, 0, 0], 
                 [0, 0, 4, 6, 6, 4, 0, 0], 
                 [0, 0, 4, 4, 4, 4, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0]]


def evaluateBoard(board, numMoves):
    pieceValues = {'p':100, 'n':324, 'b':340, 'r':500, 'q':900, 'k':0}
    score = 0

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

    # pawns being diagonal to each other and pawns and kights being in central positions
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
            elif board[row][col] == 'P':
                score -=  (centralValues[::-1])[row][col]
                if col - 1 >= 0 and row <= 7:
                    if board[row - 1][col - 1] == 'P':
                        score -= 3
                if col + 1 <= 7 and row <= 7:
                    if board[row - 1][col + 1] == 'P':
                        score -= 3
            elif board[row][col] == 'n':
                score += centralValues[row][col]
            elif board[row][col] == 'N':
                score -=  (centralValues[::-1])[row][col]

    #penalty for queen moving in opening stage
    if numMoves < 10:
        if board[0][3] != 'Q':
            score += 100

    return score

#print(evaluateBoard(board))



def minimax(position, depth, alpha, beta, maximisingPlayer, openingTable, numMoves):
    # check if the position is in the opening book, if so return the move for that opening
    posKey = str(position)

    if posKey in openingTable:
        return openingTable[posKey]
    
    if depth == 0:
        return evaluateBoard(position, numMoves), None

    bestMove = None

    # white is maximising its eval
    if maximisingPlayer:
        maxEval = float('-inf')
        colourMoves = getColourMoves(position, 'white')
        # check if it is checkmate
        y = True
        for x in colourMoves:
            if x[1] != []:
                y = False
        if y:
            return float('-inf'), None
        for pieceMoves in colourMoves:
            for moves in pieceMoves[1]:
                # keep track of origininal position to restore board later
                originalPiece = position[moves[0]][moves[1]]
                originalPos = position[pieceMoves[0][0]][pieceMoves[0][1]]

                # make move
                position[moves[0]][moves[1]] = originalPos
                position[pieceMoves[0][0]][pieceMoves[0][1]] = ''
                # update promoted pawns
                for x in range(8):
                    if board[0][x] == 'p':
                        board[0][x] = 'q'

                # call minimax on position
                evaluation, move = minimax(position, depth - 1, alpha, beta, False, openingTable, numMoves)

                # undo move
                position[moves[0]][moves[1]] = originalPiece
                position[pieceMoves[0][0]][pieceMoves[0][1]] = originalPos

                # uodate best evaluation and move
                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = [pieceMoves[0], moves]

                # update alpha
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break  # beta cut off

        return maxEval, bestMove

    # black is trying to minimise the eval
    else:
        minEval = float('inf')
        colourMoves = getColourMoves(position, 'black')
        # check if it is checkmate
        y = True
        for x in colourMoves:
            if x[1] != []:
                y = False
        if y:
            return float('inf'), None
        for pieceMoves in colourMoves:
            for moves in pieceMoves[1]:
                # keep track of origininal position to restore board later
                originalPiece = position[moves[0]][moves[1]]
                originalPos = position[pieceMoves[0][0]][pieceMoves[0][1]]

                # make the move
                position[moves[0]][moves[1]] = originalPos
                position[pieceMoves[0][0]][pieceMoves[0][1]] = ''
                # update promote pawns'
                for x in range(8):
                    if board[7][x] == 'P':
                        board[7][x] = 'Q'
                
                # call minimax on position
                evaluation, move = minimax(position, depth - 1, alpha, beta, True, openingTable, numMoves)

                # undo move
                position[moves[0]][moves[1]] = originalPiece
                position[pieceMoves[0][0]][pieceMoves[0][1]] = originalPos

                # update best evaluation and move
                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = [pieceMoves[0], moves]

                # update beta 
                beta = min(beta, minEval)
                if beta <= alpha:
                    break  # alpha cut off

        return minEval, bestMove
