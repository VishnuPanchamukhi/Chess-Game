from evaluation import *

# function to generate capture moves
def generateCaptures(board, maximisingPlayer):
    captures = []
    if maximisingPlayer == True:
        colour = 'white'
    else:
        colour = 'black'
    colourMoves = getColourMoves(board, colour)
    for pieceMoves in colourMoves:
        for destination in pieceMoves[1]:
            targetPiece = board[destination[0]][destination[1]]
            if targetPiece != '':
                captures.append((pieceMoves[0], destination))
    return captures

# stable position checker
def boardIsQuiet(board, maximisingPlayer):
    # return true if no captures
    for move in generateCaptures(board, maximisingPlayer):
        return False
    return True

# quiescence search
def quiescenceSearch(board, alpha, beta, maximisingPlayer, quiescenceDepth):
    bestMove = None
    eval = evaluateBoard(board, 10000000000000000)

    # return eval if stable position or depth limit reached
    if boardIsQuiet(board, maximisingPlayer) or quiescenceDepth == 0:
        return eval, bestMove

    if maximisingPlayer:
        maxEval = float('-inf')

        for move in generateCaptures(board, maximisingPlayer):
            # make move
            originalPiece = board[move[0][0]][move[0][1]]
            targetPiece = board[move[1][0]][move[1][1]]
            board[move[1][0]][move[1][1]] = originalPiece
            board[move[0][0]][move[0][1]] = ''

            # recursive call
            eval, x = quiescenceSearch(board, alpha, beta, False, quiescenceDepth - 1)

            # undo move
            board[move[0][0]][move[0][1]] = originalPiece
            board[move[1][0]][move[1][1]] = targetPiece

            # update best eval and move
            if eval > maxEval:
                maxEval = eval
                bestMove = move

            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break

        return maxEval, bestMove

    else:
        minEval = float('inf')

        for move in generateCaptures(board, maximisingPlayer):
            # make move
            originalPiece = board[move[0][0]][move[0][1]]
            targetPiece = board[move[1][0]][move[1][1]]
            board[move[1][0]][move[1][1]] = originalPiece
            board[move[0][0]][move[0][1]] = ''

            # recrusive call
            eval, x = quiescenceSearch(board, alpha, beta, True, quiescenceDepth - 1)

            # undo move
            board[move[0][0]][move[0][1]] = originalPiece
            board[move[1][0]][move[1][1]] = targetPiece

            # update best eval and move
            if eval < minEval:
                minEval = eval
                bestMove = move

            beta = min(beta, minEval)
            if beta <= alpha:
                break

        return minEval, bestMove
